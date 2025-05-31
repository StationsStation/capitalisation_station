from typing import Any
from decimal import Decimal
from datetime import datetime

from aea_ledger_ethereum import (
    HexBytes,
)

from packages.eightballer.protocols.orders.custom_types import (
    Order,
    OrderSide,
    OrderType,
    OrderStatus,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import BaseErc20Exchange


class KittyPunch(BaseErc20Exchange):
    """KittyPunch exchange class for DCXT."""

    def parse_order(self, api_call: dict[str, Any], exchange_id) -> Order:
        """Create an order from an api call."""
        order = api_call
        order.exchange_id = exchange_id
        self.logger.warning(f"Parsed order: {order}")
        return order

    async def fetch_open_orders(self, address: str) -> dict[str, Any]:
        """Fetch the open orders for the given address."""
        self.logger.warning("KittyPunch does not support fetch_open_orders.")
        return {}

    async def fetch_positions(self, *arg, **kwargs) -> dict[str, Any]:
        """Fetch the positions for the given address."""
        self.logger.warning("KittyPunch does not support fetch_positions.")
        return {}

    async def fetch_tickers(self, *args, **kwargs) -> dict[str, Any]:
        """Fetch the tickers."""
        self.logger.warning("KittyPunch does not support fetch_tickers.")
        return {}

    async def fetch_ticker(
        self,
        symbol: str | None = None,
        asset_a: str | None = None,
        asset_b: str | None = None,
        params: dict | None = None,
    ):
        """Fetches a ticker."""

        if all([symbol is None, asset_a is None or asset_b is None]):
            msg = "Either symbol or asset_a and asset_b must be provided"
            raise ValueError(msg)
        if symbol:
            asset_a, asset_b = symbol.split("/")
        if not asset_a or not asset_b:
            msg = "Asset A and Asset B must be provided"
            raise ValueError(msg)

        # look up the token addresses by key.
        input_token = self.get_token_by_name(asset_a)
        output_token = self.get_token_by_name(asset_b)

        if not input_token or not output_token:
            msg = f"Invalid token symbol provided: {asset_a} or {asset_b}"
            raise ValueError(msg)
        symbol = f"{input_token.symbol}/{output_token.symbol}"

        # We now calculate the price of the token.
        params["is_sell"] = True
        bid_price, amount = await self.get_price(input_token, output_token, **params)
        params["amount"] = amount
        inverse_ask_p, amount = await self.get_price(output_token, input_token, **params)

        ask_price = 1 / inverse_ask_p

        timestamp = datetime.now(tz=datetime.now().astimezone().tzinfo)
        self.logger.debug(f"Got ticker for {symbol} with ask: {ask_price} and bid: {bid_price}")
        return Ticker(
            symbol=symbol,
            asset_a=asset_a,
            asset_b=asset_b,
            high=ask_price,
            low=bid_price,
            ask=ask_price,
            bid=bid_price,
            timestamp=int(timestamp.timestamp()),
            datetime=timestamp.isoformat(),
        )

    async def create_order(
        self,
        side: OrderSide,
        asset_a: str,
        asset_b: str,
        amount: Decimal,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        """Create an order."""
        del args
        side = OrderSide.BUY if side == "buy" else OrderSide.SELL
        if side == OrderSide.BUY:
            src = asset_b
            dst = asset_a

        else:
            src = asset_a
            dst = asset_b

        input_token = self.get_token(src)
        output_token = self.get_token(dst)

        if side == OrderSide.BUY:
            _amount = int((amount * 10**input_token.decimals) * kwargs.get("price"))
        else:
            _amount = int(amount * 10**output_token.decimals)
        #
        # swap_params = OneInchSwapParams(
        #     src=src,
        #     dst=dst,
        #     amount=str(_amount),
        #     from_=self.account.address,
        #     disable_estimate=False,
        #     allow_partial_fill=False,
        #     slippage=str(1),
        # )
        #
        # res, txn_hash = await self.one_inch_api.swap_tokens(swap_params)
        #
        txn_hash = HexBytes("0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        self.logger("Using random txn hash for testing purposes: %s", txn_hash)
        return Order(
            id=txn_hash,
            symbol=f"{input_token.symbol}/{output_token.symbol}",
            side=side,
            asset_a=asset_a,
            asset_b=asset_b,
            amount=amount,
            price=kwargs.get("price"),
            status=OrderStatus.FILLED if res else OrderStatus.FAILED,
            type=OrderType.MARKET,
            timestamp=datetime.now(tz=datetime.timetz().tzinfo).timestamp(),
        )
