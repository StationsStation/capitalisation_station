# ------------------------------------------------------------------------------
#
#   Copyright 2023
#   Copyright 2023 valory-xyz
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a simple arbitrage strategy."""

import json
from dataclasses import field, dataclass

from more_itertools import partition

from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeRequest


BRIDGE_TRIGGER = 0.05
BRIDGE_RATIO = 0.2


@dataclass
class ArbitrageOpportunity:
    """An arbitrage opportunity."""

    market: str
    delta: float
    percent: float
    best_bid: float
    best_ask: float
    best_bid_exchange: str
    best_ask_exchange: str
    best_bid_ledger: str
    best_ask_ledger: str
    required_asset_a: float = None
    required_asset_b: float = None
    balance_a: float = None
    balance_b: float = None


@dataclass
class ArbitrageStrategy:
    """A simple arbitrage strategy."""

    base_asset: str
    quote_asset: str
    min_profit: float
    order_size: float
    max_open_orders: int
    unaffordable: list[ArbitrageOpportunity] = field(default_factory=list)

    target_orderbook_exchange: str = "derive"

    def get_orders(
        self,
        portfolio: dict[str, dict[str, dict[str, float]]],
        prices: dict[str, dict[str, dict[str, float]]],
        orders: dict[str, dict[str, dict[str, Order]]],
    ) -> list[Order]:
        """Get orders give a set of prices and balances.

        Args:
        ----
        portfolio: dict[str, dict[str, dict[str, float]]]: the portfolio
        prices: dict[str, dict[str, dict[str, float]]]: the prices
        **kwargs: dict: the keyword arguments

        Returns:
        -------
        [Order]: the orders

        """

        orders = orders or {}

        exchange_orders: list[Order] = list(
            orders.get(self.target_orderbook_exchange, {}).get(self.target_orderbook_exchange, [])
        )

        open_orders: list[Order] = [o for o in exchange_orders if o.status == OrderStatus.OPEN]

        sell_orders, buy_orders = (
            list(i)
            for i in partition(
                lambda o: o.side == OrderSide.BUY,
                open_orders,
            )
        )
        if len(sell_orders) + len(buy_orders) >= self.max_open_orders:
            return []

        index_prices = {
            market.get("symbol"): json.loads(market.get("info", "{}"))
            for market in prices.get(self.target_orderbook_exchange, {}).get(self.target_orderbook_exchange, [])
        }

        num_buy_orders = 5
        num_sell_orders = 10

        remaining_buy_orders = num_buy_orders - len(buy_orders)
        remaining_sell_orders = num_sell_orders - len(sell_orders)

        orders = []
        buy_asset = self.quote_asset.upper()

        self.base_asset.upper()

        asset_balances = portfolio.get(self.target_orderbook_exchange, {}).get(self.target_orderbook_exchange, [])

        asset_balances = {asset["asset_id"].upper(): asset for asset in asset_balances}

        # free buy_balance
        buy_balance = asset_balances.get(buy_asset, {}).get("free", 0)
        if not buy_balance:
            return []
        if remaining_buy_orders <= 0 and remaining_sell_orders <= 0:
            return []

        return self.get_all_orders(
            index_prices,
            buy_balance,
            remaining_buy_orders,
            remaining_sell_orders,
            open_orders,
            num_buy_orders=num_buy_orders,
            num_sell_orders=num_sell_orders,
        )

    def get_all_orders(
        self,
        index_prices: dict[str, dict[str, float]],
        buy_balance: float,
        remaining_buy_orders: int,
        remaining_sell_orders: int,
        open_orders: list[Order],
        num_buy_orders: int = 5,
        num_sell_orders: int = 10,
    ) -> list[Order]:
        """Get buy orders."""

        lower_bound_percentage = 0.9  # lower bound is from the index price
        upper_bound_percentage = 2.0  # upper bound is from the index price

        orders = []
        for market, data in index_prices.items():
            index_price = data.get("index_price", 0)
            if not index_price:
                continue

            if remaining_buy_orders:
                # we create a range of orders starting from the index price
                min_price = index_price * (lower_bound_percentage)
                max_price = index_price * (1 - self.min_profit)
                step = (max_price - min_price) / remaining_buy_orders

                amount = (buy_balance / 3) / num_buy_orders if remaining_buy_orders else 0
                if not amount:
                    continue

                for i in range(1, remaining_buy_orders + 1):
                    price = min_price + (i * step)

                    order_amount = amount / price

                    buy_order = Order(
                        price=price,
                        exchange_id=self.target_orderbook_exchange,
                        ledger_id=self.target_orderbook_exchange,
                        symbol=market,
                        side=OrderSide.BUY,
                        status=OrderStatus.NEW,
                        amount=order_amount,
                        type=OrderType.LIMIT,
                        immediate_or_cancel=False,
                    )
                    orders.append(buy_order)

            if remaining_sell_orders:
                # we create a range of orders starting from the index price
                min_price = index_price * (1 + self.min_profit)
                max_price = index_price * (upper_bound_percentage)
                step = (max_price - min_price) / remaining_sell_orders

                amount = buy_balance / num_sell_orders if remaining_sell_orders else 0

                for i in range(remaining_sell_orders):
                    price = min_price + (i * step)
                    order_amount = amount / price

                    sell_order = Order(
                        price=price,
                        exchange_id=self.target_orderbook_exchange,
                        ledger_id=self.target_orderbook_exchange,
                        symbol=market,
                        side=OrderSide.SELL,
                        status=OrderStatus.NEW,
                        amount=order_amount,
                        type=OrderType.LIMIT,
                        immediate_or_cancel=False,
                    )
                    orders.append(sell_order)
        # we return the orders
        # we filter the orders to only include the ones that are not already open
        orders = [o for o in orders if o not in open_orders]

        orders.sort(key=lambda o: o.price)
        return orders

    def get_opportunities(self, prices, overlaps, all_ledger_exchanges):
        """Get opportunities."""
        opportunities = []
        best_bid, best_ask, best_ask_exchange, best_bid_exchange, best_ask_ledger, best_bid_ledger = [None] * 6
        for market in overlaps:
            # we calculate the best bids and asks
            for ledger, exchange in all_ledger_exchanges:
                price = [f for f in prices[ledger][exchange] if f["symbol"].replace("-", "/").upper() == market].pop()
                if best_bid is None or price["bid"] > best_bid:
                    best_bid = price["bid"]
                    best_bid_exchange = exchange
                    best_bid_ledger = ledger

                if (best_ask is None or price["ask"] < best_ask) and price["ask"] > 0:
                    best_ask = price["ask"]
                    best_ask_exchange = exchange
                    best_ask_ledger = ledger
            delta = best_bid - best_ask
            percent = delta / best_ask
            if percent > self.min_profit:
                opportunities.append(
                    ArbitrageOpportunity(
                        market=market,
                        delta=delta,
                        percent=percent,
                        best_bid=best_bid,
                        best_ask=best_ask,
                        best_bid_exchange=best_bid_exchange,
                        best_bid_ledger=best_bid_ledger,
                        best_ask_exchange=best_ask_exchange,
                        best_ask_ledger=best_ask_ledger,
                    )
                )
        return [o for o in opportunities if self.valid_opportunity(o)]

    def valid_opportunity(self, opportunity):
        """Check if an opportunity is valid."""
        # sense checks as we will get eaten by mev if we try to do on one exchange
        # - we are not buying and selling on the same exchange
        # - we are not buying and selling on the same ledger
        return not any(
            [
                opportunity.best_ask_exchange == opportunity.best_bid_exchange,
                opportunity.best_ask_ledger == opportunity.best_bid_ledger,
            ]
        )

    def has_balance_for_opportunity(self, opportunity, portfolio, amount):
        """Check if we have the balance for an opportunity."""
        # we get the buy balances, i.e. the balances of the asset we SELLING to buy the asset we are BUYING
        asset_a, asset_b = opportunity.market.split("/")
        sell_balances = portfolio[opportunity.best_ask_ledger][opportunity.best_ask_exchange]
        buy_balances = portfolio[opportunity.best_bid_ledger][opportunity.best_bid_exchange]
        buy_balance = {asset["asset_id"].upper(): asset for asset in buy_balances}.get(asset_a)
        sell_balance = {asset["asset_id"].upper(): asset for asset in sell_balances}.get(asset_b)
        # asset_a required to buy asset_b
        opportunity.required_asset_a = amount
        opportunity.required_asset_b = amount * opportunity.best_ask
        if not all([buy_balance, sell_balance]):
            return False
        opportunity.balance_a = buy_balance["free"]
        opportunity.balance_b = sell_balance["free"]
        return not any(
            [
                opportunity.required_asset_a > opportunity.balance_buy,
                opportunity.required_asset_b > opportunity.balance_sell,
            ]
        )

    def get_orders_for_opportunity(self, opportunity, portfolio, prices):
        """Get orders for an opportunity."""
        buy_prices = {
            price["symbol"].replace("-", "/").upper(): price
            for price in prices[opportunity.best_ask_ledger][opportunity.best_ask_exchange]
        }
        sell_prices = {
            price["symbol"].replace("-", "/").upper(): price
            for price in prices[opportunity.best_bid_ledger][opportunity.best_bid_exchange]
        }
        asset_a, asset_b = opportunity.market.split("/")
        portfolio_a = {
            p["asset_id"].upper(): p for p in portfolio[opportunity.best_ask_ledger][opportunity.best_ask_exchange]
        }
        portfolio_b = {
            p["asset_id"].upper(): p for p in portfolio[opportunity.best_bid_ledger][opportunity.best_bid_exchange]
        }
        buy_order = Order(
            price=buy_prices[opportunity.market]["ask"],
            exchange_id=opportunity.best_ask_exchange,
            ledger_id=opportunity.best_ask_ledger,
            symbol=buy_prices[opportunity.market]["symbol"],
            side=OrderSide.BUY,
            status=OrderStatus.NEW,
            amount=self.order_size * (1 + opportunity.percent),
            type=OrderType.LIMIT,
            asset_a=portfolio_a[asset_a]["contract_address"] if opportunity.best_ask_exchange != "derive" else None,
            asset_b=portfolio_a[asset_b]["contract_address"] if opportunity.best_ask_exchange != "derive" else None,
        )
        sell_order = Order(
            price=sell_prices[opportunity.market]["bid"],
            exchange_id=opportunity.best_bid_exchange,
            ledger_id=opportunity.best_bid_ledger,
            symbol=sell_prices[opportunity.market]["symbol"],
            side=OrderSide.SELL,
            status=OrderStatus.NEW,
            amount=self.order_size,
            type=OrderType.LIMIT,
            asset_a=portfolio_b[asset_a]["contract_address"] if opportunity.best_bid_exchange != "derive" else None,
            asset_b=portfolio_b[asset_b]["contract_address"] if opportunity.best_bid_exchange != "derive" else None,
        )
        # we set the dervive order to be the first order
        if sell_order.exchange_id == "derive":
            return [sell_order, buy_order]
        return [buy_order, sell_order]

    def get_bridge_requests(  # noqa: C901
        self,
        portfolio: dict[str, dict[str, dict[str, float]]],
        **kwargs,  # noqa
    ) -> list[Order]:
        """Get bridge requests based on basic portfolio management strategy."""

        asset_a, asset_b = self.base_asset.upper(), self.quote_asset.upper()

        asset_to_max_balance_exchange, asset_to_min_balance_exchange = {}, {}

        def _process_balance(ledger, exchange, balance):
            """Process a single balance."""
            if asset not in asset_to_max_balance_exchange:
                asset_to_max_balance_exchange[asset] = (ledger, exchange, balance["free"])
            if balance["free"] > asset_to_max_balance_exchange[asset][2]:
                asset_to_max_balance_exchange[asset] = (ledger, exchange, balance["free"])

            if asset not in asset_to_min_balance_exchange:
                asset_to_min_balance_exchange[asset] = (ledger, exchange, balance["free"])
            if balance["free"] < asset_to_min_balance_exchange[asset][2]:
                asset_to_min_balance_exchange[asset] = (ledger, exchange, balance["free"])

        for asset in [asset_a, asset_b]:
            for ledger, exchanges in portfolio.items():
                for exchange in exchanges:
                    balances = portfolio[ledger][exchange]
                    for balance in [b for b in balances if b["asset_id"].upper() == asset]:
                        _process_balance(ledger, exchange, balance)

        totals = {
            asset: sum(
                balance["free"]
                for ledger in portfolio
                for exchange in portfolio[ledger]
                for balance in portfolio[ledger][exchange]
                if balance["asset_id"].upper() == asset
            )
            for asset in [asset_a, asset_b]
        }
        min_ratios = {asset: asset_to_min_balance_exchange[asset][2] / totals[asset] for asset in [asset_a, asset_b]}

        bridge_requests = []
        for asset in [asset_a, asset_b]:
            if min_ratios[asset] < BRIDGE_TRIGGER:
                # we need to bridge the asset
                from_ledger, from_exchange, from_balance = asset_to_max_balance_exchange[asset]
                to_ledger, to_exchange, _ = asset_to_min_balance_exchange[asset]
                if from_ledger == to_ledger and from_exchange == to_exchange:
                    continue
                amount_to_bridge = from_balance - (totals[asset] * BRIDGE_RATIO)
                if amount_to_bridge <= 0:
                    continue
                bridge_requests.append(
                    BridgeRequest(
                        source_ledger_id=from_ledger,
                        target_ledger_id=to_ledger,
                        amount=amount_to_bridge,
                        source_token=asset,
                        bridge="derive",
                    )
                )
        return bridge_requests
