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

import operator
from functools import reduce
from dataclasses import dataclass

from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus


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
    _unaffordable = []

    def get_orders(
        self,
        portfolio: dict[str, dict[str, dict[str, float]]],
        prices: dict[str, dict[str, dict[str, float]]],
        **kwargs,  # noqa
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
        order_set = []

        # we check
        all_ledger_exchanges = reduce(
            lambda x, y: (x, y),
            [(ledger, exchange) for ledger in portfolio for exchange in portfolio[ledger]],
        )
        intersections = {}
        # we calculate where we have overlapping markets
        for ledger, exchange in all_ledger_exchanges:
            markets = {k.get("symbol").replace("-", "/").upper(): k for k in prices[ledger][exchange]}
            intersections[ledger] = set(markets.keys())
        overlaps = reduce(lambda x, y: x.intersection(y), intersections.values())
        opportunities = self.get_opportunities(prices, overlaps, all_ledger_exchanges)
        self.unaffordable = []
        for opp in opportunities:
            if self.has_balance_for_opportunity(opp, portfolio, self.order_size):
                orders = self.get_orders_for_opportunity(opp, portfolio, prices)
                order_set.append((opp.delta, orders))
            else:
                self.unaffordable.append(opp)
        if order_set:
            optimal_orders = max(order_set, key=operator.itemgetter(0))
            return optimal_orders[1]
        return []

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
        opportunity.balance_buy = buy_balance["free"]
        opportunity.balance_sell = sell_balance["free"]
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
            amount=self.order_size,
            type=OrderType.LIMIT,
            asset_a=portfolio_a[asset_a]["contract_address"],
            asset_b=portfolio_a[asset_b]["contract_address"],
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
            asset_a=portfolio_b[asset_a]["contract_address"],
            asset_b=portfolio_b[asset_b]["contract_address"],
        )
        return [sell_order, buy_order]
