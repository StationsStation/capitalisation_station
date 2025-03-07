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
import operator
from typing import NamedTuple
from textwrap import dedent
from functools import reduce

from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus


CEX_LEDGER = "cex"
CEX_EXCHANGE = "mexc"
DEX_EXCHANGE = "balancer"

DEX_MARKET = "OLAS/USDC"
CEX_MARKET = "OLAS/USDT"


LEDGER_TO_MARKET = {"base": "OLAS/USDC", "mode": "OLAS/USDC", "gnosis": "OLAS/WXDAI"}

DEFAULT_AMOUNT = 10.0
min_profit = 0.00  # 0%


class ArbitrageOpportunity(NamedTuple):
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


class ArbitrageStrategy:
    """A simple arbitrage strategy."""

    unaffordable = []

    def get_orders(  # noqa
        self,
        portfolio: dict[str, dict[str, dict[str, float]]],
        prices: dict[str, dict[str, dict[str, float]]],
        **kwargs,
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
        del kwargs
        order_set = []

        # we check
        all_ledger_exchanges = reduce(
            lambda x, y: (x, y),
            [(ledger, exchange) for ledger in portfolio for exchange in portfolio[ledger]],
        )

        intersections = {}
        # we calculate where we have overlapping markets
        for ledger, exchange in all_ledger_exchanges:
            markets = {k.get("symbol"): k for k in prices[ledger][exchange]}
            intersections[ledger] = set(markets.keys())

        over_laps = reduce(lambda x, y: x.intersection(y), intersections.values())

        opportunities = []
        for market in over_laps:
            # we calculate the best bids and asks
            best_bid = None
            best_ask = None
            best_bid_exchange = None
            best_bid_ledger = None
            best_ask_exchange = None
            best_ask_ledger = None
            for ledger, exchange in all_ledger_exchanges:
                price = [f for f in prices[ledger][exchange] if f["symbol"] == market].pop()
                if best_bid is None or price["bid"] > best_bid:
                    best_bid = price["bid"]
                    best_bid_exchange = exchange
                    best_bid_ledger = ledger
                if best_ask is None or price["ask"] < best_ask:
                    best_ask = price["ask"]
                    best_ask_exchange = exchange
                    best_ask_ledger = ledger
            delta = best_bid - best_ask
            percent = delta / best_ask
            if percent > min_profit:
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

        self.unaffordable = []
        for opp in opportunities:
            if self.has_balance_for_opportunity(opp, portfolio):
                orders = self.get_orders_for_opportunity(opp, portfolio, prices)
                order_set.append((opp.delta, orders))
            else:
                self.unaffordable.append(opp)
        if order_set:
            optimal_orders = max(order_set, key=operator.itemgetter(0))
            return optimal_orders[1]
        return []

    def cex_to_dex(self, portfolio, prices):
        """Get orders for a cex to dex arbitrage."""
        order_set = []

        for cex_exchange in portfolio[CEX_LEDGER]:
            cex_balances = {asset["asset_id"]: asset for asset in portfolio[CEX_LEDGER][cex_exchange]}
            cex_price = {price["symbol"]: price for price in prices["cex"][cex_exchange]}[CEX_MARKET]
            asset_a, asset_b = CEX_MARKET.split("/")
            asset_a_balance, asset_b_balance = cex_balances[asset_a], cex_balances[asset_b]
            for ledger in prices:
                if ledger == "cex":
                    continue
                delta, orders = self.get_orders_for_ledger(
                    ledger,
                    cex_price,
                    asset_a_balance,
                    asset_b_balance,
                    cex_exchange,
                    portfolio,
                    prices,
                )
                order_set.append((delta, orders))
        opportunities = list(filter(lambda x: x[0] != -99, order_set))
        unaffordable = list(filter(lambda x: x[0] == -99, order_set))
        if unaffordable:
            self.unaffordable = unaffordable
        if opportunities:
            optimal_orders = max(opportunities, key=operator.itemgetter(0))
            return optimal_orders[1]
        return []

    def has_balance_for_opportunity(self, opportunity, portfolio):
        """Check if we have the balance for an opportunity."""
        buy_balance = portfolio[opportunity.best_ask_ledger][opportunity.best_ask_exchange]
        sell_balance = portfolio[opportunity.best_bid_ledger][opportunity.best_bid_exchange]
        buy_asset, sell_asset = opportunity.market.split("/")
        buy_balance = {asset["asset_id"]: asset for asset in buy_balance}
        sell_balance = {asset["asset_id"]: asset for asset in sell_balance}
        return not any(
            [
                buy_balance[buy_asset]["free"] < DEFAULT_AMOUNT * opportunity.best_ask,
                sell_balance[sell_asset]["free"] < DEFAULT_AMOUNT,
            ]
        )

    def get_orders_for_opportunity(self, opportunity, portfolio, prices):
        """Get orders for an opportunity."""
        buy_prices = {
            price["symbol"]: price for price in prices[opportunity.best_ask_ledger][opportunity.best_ask_exchange]
        }
        sell_prices = {
            price["symbol"]: price for price in prices[opportunity.best_bid_ledger][opportunity.best_bid_exchange]
        }
        asset_a, asset_b = opportunity.market.split("/")
        portfolio_a = {p["asset_id"]: p for p in portfolio[opportunity.best_ask_ledger][opportunity.best_ask_exchange]}
        portfolio_b = {p["asset_id"]: p for p in portfolio[opportunity.best_bid_ledger][opportunity.best_bid_exchange]}
        buy_order = Order(
            price=buy_prices[opportunity.market]["ask"],
            exchange_id=opportunity.best_ask_exchange,
            ledger_id=opportunity.best_ask_ledger,
            symbol=opportunity.market,
            side=OrderSide.BUY,
            status=OrderStatus.NEW,
            amount=DEFAULT_AMOUNT,
            type=OrderType.MARKET,
            asset_a=portfolio_a[asset_a]["contract_address"],
            asset_b=portfolio_a[asset_b]["contract_address"],
        )
        sell_order = Order(
            price=sell_prices[opportunity.market]["bid"],
            exchange_id=opportunity.best_bid_exchange,
            ledger_id=opportunity.best_bid_ledger,
            symbol=opportunity.market,
            side=OrderSide.SELL,
            status=OrderStatus.NEW,
            amount=DEFAULT_AMOUNT,
            type=OrderType.MARKET,
            asset_a=portfolio_b[asset_a]["contract_address"],
            asset_b=portfolio_b[asset_b]["contract_address"],
        )
        return [sell_order, buy_order]

    def get_orders_for_ledger(
        self,
        ledger: str,
        cex_price: dict[str, float],
        asset_a_balance: dict[str, float],
        asset_b_balance: dict[str, float],
        cex_exchange: str,
        portfolio: dict[str, dict[str, dict[str, float]]],
        prices: dict[str, dict[str, dict[str, float]]],
    ) -> tuple[float, list[Order]]:
        """Get orders for a ledger,
        based on the prices and balances of all ledgers.
        Effectively parse the candidates for arbitrage opportunities prior
        to calculcating exact orders.
        """

        token_a, token_b = LEDGER_TO_MARKET[ledger].split("/")
        dex_balances = {asset["asset_id"]: asset for asset in portfolio[ledger][DEX_EXCHANGE]}
        token_a_address, token_b_address = (
            dex_balances[token_a]["contract_address"],
            dex_balances[token_b]["contract_address"],
        )
        token_a_balance, token_b_balance = dex_balances[token_a], dex_balances[token_b]
        dex_prices = {price["symbol"]: price for price in prices[ledger][DEX_EXCHANGE]}
        dex_price = dex_prices[DEX_MARKET]
        return self._calculate_orders(
            cex_price,
            dex_price,
            token_a_address,
            token_b_address,
            asset_a_balance,
            asset_b_balance,
            token_a_balance,
            token_b_balance,
            ledger,
            cex_exchange,
        )

    def _calculate_orders(
        self,
        cex_price,
        dex_price,
        token_a_address,
        token_b_address,
        asset_a_balance,
        asset_b_balance,
        token_a_balance,
        token_b_balance,
        ledger,
        cex_exchange,
    ):
        """Calculate the orders to execute."""
        # we calculate if there is an arbitrage opportunity
        best_bid = max(cex_price["bid"], dex_price["bid"])  # highest bid
        best_ask = min(cex_price["ask"], dex_price["ask"])  # lowest ask
        delta = best_bid - best_ask
        percent = delta / best_ask

        if percent > min_profit:
            if cex_price["bid"] > dex_price["ask"]:
                # buy on dex and sell on cex
                # We need to check we have enough of the asset we are using to buy on dex
                if any(
                    [
                        (buy_avail := token_b_balance["free"]) < (buy_required := DEFAULT_AMOUNT * dex_price["ask"]),
                        (sell_avail := asset_a_balance["free"]) < (sell_required := DEFAULT_AMOUNT),
                    ]
                ):
                    return -99, [
                        dedent(f"""
                        Insufficient funds for {percent:5f}% arbitrage:
                            Buy on `{ledger}` `{DEX_EXCHANGE}` and Sell on `{cex_exchange}`
                            Sell Available: {sell_avail=} Required {sell_required=}
                            Buy Available: {buy_avail=} Required {buy_required=}
                        """)
                    ]

                buy_order = Order(
                    price=dex_price["ask"],
                    exchange_id=DEX_EXCHANGE,
                    ledger_id=ledger,
                    symbol=DEX_MARKET,
                    asset_a=token_a_address,
                    asset_b=token_b_address,
                    side=OrderSide.BUY,
                    status=OrderStatus.NEW,
                    amount=DEFAULT_AMOUNT,
                    type=OrderType.MARKET,
                )

                sell_order = Order(
                    price=cex_price["bid"],
                    exchange_id=cex_exchange,
                    ledger_id=CEX_LEDGER,
                    symbol=CEX_MARKET,
                    side=OrderSide.SELL,
                    status=OrderStatus.NEW,
                    amount=DEFAULT_AMOUNT,
                    type=OrderType.LIMIT,
                    info=json.dumps({"post_only": False}),
                )
            else:
                # buy on cex and sell on dex
                # We need to check we have enough of the asset we are using to buy on cex
                if any(
                    [
                        (sell_avail := token_a_balance["free"]) < (sell_required := DEFAULT_AMOUNT),
                        (buy_avail := asset_b_balance["free"]) < (buy_required := DEFAULT_AMOUNT * cex_price["ask"]),
                    ]
                ):
                    return -99, [
                        dedent(f"""
                        Insufficient funds for {percent:5f}% arbitrage:
                            Sell on `{ledger}` `{DEX_EXCHANGE}` and Buy on `{cex_exchange}`
                            Sell Available: {sell_avail=} Required {sell_required=}
                            Buy Available: {buy_avail=} Required {buy_required=}
                        """)
                    ]

                buy_order = Order(
                    price=cex_price["ask"],
                    ledger_id=CEX_LEDGER,
                    exchange_id=cex_exchange,
                    symbol=CEX_MARKET,
                    side=OrderSide.BUY,
                    amount=DEFAULT_AMOUNT,
                    status=OrderStatus.NEW,
                    type=OrderType.LIMIT,
                    info=json.dumps({"post_only": False}),
                )

                sell_order = Order(
                    exchange_id=DEX_EXCHANGE,
                    market=DEX_MARKET,
                    symbol=DEX_MARKET,
                    side=OrderSide.SELL,
                    price=dex_price["bid"],
                    amount=DEFAULT_AMOUNT,
                    ledger_id=ledger,
                    asset_a=token_a_address,
                    asset_b=token_b_address,
                    status=OrderStatus.NEW,
                    type=OrderType.MARKET,
                )
            return delta, [sell_order, buy_order]
        return delta, []
