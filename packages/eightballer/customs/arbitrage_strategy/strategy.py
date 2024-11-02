from typing import Dict

from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus


CEX_MARKET = "OLAS/USDT"
DEX_MARKET = "OLAS/USDC"
DEX_ADDRESSES = "0x54330d28ca3357f294334bdc454a032e7f353416/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"

CEX_LEDGER = "cex"
CEX_EXCHANGE = "mexc"
DEX_EXCHANGE = "balancer"
DEFAULT_LEDGER = "base"
DEFAULT_AMOUNT = 1.0


class ArbitrageStrategy:
    def get_orders(self, portfolio: Dict[str, float], prices: Dict[str, float]) -> Dict[str, float]:
        """
        Get orders give a set of prices and balances.

        :param prices: the prices
        :param balances: the balances
        :return: the orders
        """
        cex_balances = {asset["asset_id"]: asset for asset in portfolio[CEX_LEDGER][CEX_EXCHANGE]}
        dex_balances = {asset["asset_id"]: asset for asset in portfolio[DEFAULT_LEDGER][DEX_EXCHANGE]}
        asset_a, asset_b = CEX_MARKET.split("/")
        token_a, token_b = DEX_MARKET.split("/")
        token_a_address, token_b_address = DEX_ADDRESSES.split("/")

        asset_a_balance, asset_b_balance = cex_balances[asset_a], cex_balances[asset_b]
        token_a_balance, token_b_balance = dex_balances[token_a], dex_balances[token_b]

        dex_prices = {price["symbol"]: price for price in prices[DEFAULT_LEDGER][DEX_EXCHANGE]}
        cex_price = {price["symbol"]: price for price in prices["cex"][CEX_EXCHANGE]}[CEX_MARKET]
        dex_price = dex_prices[DEX_ADDRESSES]

        # we calculate if there is an arbitrage opportunity
        best_bid = max(cex_price["bid"], dex_price["bid"])  # highest bid
        best_ask = min(cex_price["ask"], dex_price["ask"])  # lowest ask

        if best_bid > best_ask:
            # there is an arbitrage opportunity
            # we calculate the amount to trade based on a default order size.
            # We verify that we have enough balance on both exchanges
            # We calculate the profit

            if cex_price["bid"] > dex_price["ask"]:
                # buy on dex and sell on cex
                print(f"buy on dex for {dex_price['ask']} and sell on cex for {cex_price['bid']}")
                # We need to check we have enough of the asset we are using to buy on dex
                if token_b_balance["free"] < DEFAULT_AMOUNT * dex_price["ask"]:
                    print("Not enough balance on dex to buy")
                    return
                if asset_a_balance["free"] < DEFAULT_AMOUNT:
                    print("Not enough balance on cex to sell")
                    return

                buy_order = Order(
                    price=dex_price["ask"],
                    exchange_id=DEX_EXCHANGE,
                    ledger_id=DEFAULT_LEDGER,
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
                    exchange_id=CEX_EXCHANGE,
                    ledger_id=CEX_LEDGER,
                    symbol=CEX_MARKET,
                    side=OrderSide.SELL,
                    status=OrderStatus.NEW,
                    amount=DEFAULT_AMOUNT,
                    type=OrderType.MARKET,
                )
            else:
                print(f"buy on cex for {cex_price['ask']} and sell on dex for {dex_price['bid']}")
                # buy on cex and sell on dex
                # We need to check we have enough of the asset we are using to buy on cex
                if asset_b_balance["free"] < DEFAULT_AMOUNT * cex_price["ask"]:
                    print("Not enough balance on cex to buy")
                    return
                if token_a_balance["free"] < DEFAULT_AMOUNT:
                    print("Not enough balance on dex to sell")
                    return

                buy_order = Order(
                    price=cex_price["ask"],
                    ledger_id=CEX_LEDGER,
                    exchange_id=CEX_EXCHANGE,
                    symbol=CEX_MARKET,
                    side=OrderSide.BUY,
                    amount=DEFAULT_AMOUNT,
                    status=OrderStatus.NEW,
                    type=OrderType.MARKET,
                )

                sell_order = Order(
                    exchange_id=DEX_EXCHANGE,
                    market=DEX_MARKET,
                    side=OrderSide.SELL,
                    symbol=DEX_ADDRESSES,
                    price=dex_price["bid"],
                    amount=DEFAULT_AMOUNT,
                    ledger_id=DEFAULT_LEDGER,
                    asset_a=token_a_address,
                    asset_b=token_b_address,
                    status=OrderStatus.NEW,
                    type=OrderType.MARKET,
                )
            return [sell_order, buy_order]
        else:
            print("No arbitrage opportunity best bid is less than best ask")
            return []
