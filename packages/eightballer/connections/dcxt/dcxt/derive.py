"""An interface for the Derive API."""

import json
import asyncio
import datetime
import traceback
from typing import Any
from pathlib import Path
from itertools import starmap

from derive_client import AsyncHTTPClient as DeriveAsyncClient
from derive_client.data_types import (
    Currency,
    AssetType,
    OrderType as DeriveOrderType,
)
from derive_client.exceptions import ApiException
from derive_client.data_types.generated_models import (
    Direction as DeriveOrderSide,
    OrderStatus as DeriveOrderStatus,
    TimeInForce as DeriveTimeInForce,
    TickerSlimSchema,
    OrderResponseSchema,
    CollateralResponseSchema,
)

from packages.eightballer.protocols.orders.custom_types import Order, Orders, OrderSide, OrderType, OrderStatus
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.connections.dcxt.dcxt.exceptions import ExchangeError
from packages.eightballer.protocols.positions.custom_types import Position
from packages.eightballer.protocols.order_book.custom_types import OrderBook


TZ = datetime.datetime.now().astimezone().tzinfo


def to_market(api_result):
    """Convert to a market object.
        raw_resulot = {'instrument_type': 'perp',
        'instrument_name': 'BTC-PERP',
        'scheduled_activation': 1699035945,
        'scheduled_deactivation': 9223372036854775807,
    'is_active': True,
    'tick_size': '0.1',
    'minimum_amount': '0.01',
    'maximum_amount': '10000',
    'amount_step': '0.001',
    'mark_price_fee_rate_cap': '0',
    'maker_fee_rate': '0.0005',
    'taker_fee_rate': '0.001',
    'base_fee': '1.5',
    'base_currency': 'BTC',
    'quote_currency': 'USD',
    'option_details': None,
    'perp_details': {'index': 'BTC-USD',
    'max_rate_per_hour': '0.1',
    'min_rate_per_hour': '-0.1',
    'static_interest_rate': '0',
    'aggregate_funding': '244.249950785486024857',
    'funding_rate': '-0.0000125'},
    'base_asset_address': '0xAFB6Bb95cd70D5367e2C39e9dbEb422B9815339D',
    'base_asset_sub_id': '0'}.

    """

    return Market(
        id=api_result["instrument_name"],
        lowercaseId=api_result["instrument_name"].lower(),
        symbol=api_result["instrument_name"],
        base=api_result["base_currency"],
        quote=api_result["quote_currency"],
        settle=api_result["quote_currency"],
        baseId=api_result["base_currency"],
        quoteId=api_result["quote_currency"],
        settleId=api_result["quote_currency"],
        type=api_result["instrument_type"],
        future=api_result["instrument_type"] == AssetType.PERP,
        option=api_result["instrument_type"] == AssetType.OPTION,
        active=api_result["is_active"],
        taker=api_result["taker_fee_rate"],
        maker=api_result["maker_fee_rate"],
    )


def to_ticker(symbol: str, api_result: TickerSlimSchema) -> Ticker:
    """Convert to a ticker object."""
    return Ticker(
        symbol=symbol,
        timestamp=api_result.t,
        datetime=datetime.datetime.fromtimestamp(api_result.t / 1000, tz=TZ).isoformat(),
        high=float(api_result.stats.h),
        low=float(api_result.stats.l),
        bid=float(api_result.b),
        bidVolume=float(api_result.B),
        ask=float(api_result.a),
        askVolume=float(api_result.A),
        close=float(api_result.M),
        last=float(api_result.M),
        change=float(api_result.stats.c),
        percentage=float(api_result.stats.p),
        baseVolume=float(api_result.stats.v),
        info=json.dumps({"index_price": float(api_result.I), "mark_price": float(api_result.M)}),
    )


def to_balance(api_result: CollateralResponseSchema):
    """Convert to a balance object."""
    return Balance(
        asset_id=api_result.currency,
        free=float(api_result.amount),
        used=0,
        total=float(api_result.amount),
        is_native=False,
    )


def to_position(api_result):
    """Convert to a position object."""
    return Position(
        id=api_result["instrument_name"],
        symbol=api_result["instrument_name"],
        size=float(api_result["amount"]),
        entry_price=float(api_result["average_price"]),
        realized_pnl=float(api_result["realized_pnl"]),
        unrealized_pnl=float(api_result["unrealized_pnl"]),
        initial_margin=float(api_result["initial_margin"]),
        maintenance_margin=float(api_result["maintenance_margin"]),
        notional=float(api_result["mark_value"]),
        leverage=float(api_result["leverage"]),
        liquidation_price=float(api_result["liquidation_price"]),
        mark_price=float(api_result["mark_price"]),
        exchange_id="derive",
    )


DERIVE_ORDER_STATUS_MAP = {
    DeriveOrderStatus.open: OrderStatus.OPEN.value,
    DeriveOrderStatus.filled: OrderStatus.FILLED.value,
    DeriveOrderStatus.cancelled: OrderStatus.CANCELLED.value,
    # DeriveOrderStatus.REJECTED: OrderStatus.FAILED.name,
    DeriveOrderStatus.expired: OrderStatus.EXPIRED.value,
}
DERIVE_ORDER_TYPE_MAP = {
    DeriveOrderType.limit: OrderType.LIMIT.value,
    DeriveOrderType.market: OrderType.MARKET.value,
}

DERIVE_DIRECTIO_To_SIDE_MAP = {
    DeriveOrderSide.buy: OrderSide.BUY,
    DeriveOrderSide.sell: OrderSide.SELL,
}


def to_order(api_result: OrderResponseSchema) -> Order:
    """Convert to an order object."""
    order_status = DERIVE_ORDER_STATUS_MAP[api_result.order_status]
    return Order(
        id=api_result.order_id,
        exchange_id="derive",
        client_order_id=api_result.order_id,
        timestamp=api_result.creation_timestamp,
        datetime=datetime.datetime.fromtimestamp(api_result.creation_timestamp / 1000, tz=TZ).isoformat(),
        last_trade_timestamp=api_result.creation_timestamp,
        status=order_status,
        symbol=api_result.instrument_name,
        type=DERIVE_ORDER_TYPE_MAP[api_result.order_type],
        time_in_force=api_result.time_in_force,
        side=DERIVE_DIRECTIO_To_SIDE_MAP[api_result.direction],
        filled=float(api_result.filled_amount),
        amount=float(api_result.amount),
        remaining=float(api_result.amount) - float(api_result.filled_amount),
        price=float(api_result.limit_price),
    )


def from_camelize(name: str) -> str:
    """Convert a camel case name to a snake case name."""
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")


class DeriveClient:
    """A class for interacting with the Derive API."""

    exchange_id = "derive"

    def __init__(self, *args, **kwargs):
        """Initialize the DeriveClient."""
        del args
        key_path = kwargs.get("key_path")
        keyfile = Path(key_path)
        if not keyfile.exists():
            msg = f"Key file not found: {key_path}"
            raise FileNotFoundError(msg)
        private_key = keyfile.read_text().strip()

        self.client: DeriveAsyncClient = DeriveAsyncClient(
            session_key=private_key,
            subaccount_id=kwargs["subaccount_id"],
            wallet=kwargs["wallet"],
            env=kwargs["environment"],
        )
        self.logger = kwargs["logger"]

    async def ensure_connected(self):
        """Ensure the client is connected."""
        if not self.client._subaccounts:  # noqa: SLF001
            await self.client.connect(True)

    async def fetch_markets(self, *args, **kwargs):
        """Fetch all markets."""
        msg = f"{self.__class__.__name__}.fetch_markets"
        raise NotImplementedError(msg)
        del args
        params = kwargs.get("params", {})
        if "currency" in params:
            params["currency"] = Currency(params["currency"].upper())
        if "type" in params:
            params["type"] = AssetType(params["type"].lower())
        result = await self.client.fetch_instruments(**params)
        markets = [to_market(market) for market in result]
        return Markets(
            markets=markets,
        )

    async def fetch_tickers(self, *args, **kwargs):
        """Fetch all tickers."""
        await self.ensure_connected()
        del args, kwargs  # should parse from name to instrument type?

        try:
            data = await self.client.markets.get_tickers(
                instrument_type=AssetType.erc20,
            )
        except Exception as error:
            self.logger.exception(traceback.print_exc())
            msg = f"Failed to fetch ticker: {error}"
            raise ExchangeError(msg) from error

        tickers = list(starmap(to_ticker, data.items()))
        return Tickers(
            tickers=tickers,
        )

    async def fetch_ticker(self, *args, symbol, asset_a, asset_b, **kwargs):
        """Fetch all tickers."""
        await self.ensure_connected()
        del args, kwargs  # should parse from name to instrument type?
        if (not asset_a and not asset_b) and (not symbol):
            msg = "Either asset_a, asset_b or symbol must be provided."
            raise ValueError(msg)

        instrument_name = f"{asset_a}/{asset_b}".upper() if not symbol else symbol.upper().replace("/", "-")
        try:
            result = await self.client.markets.get_tickers(
                instrument_type=AssetType.erc20,
                currency=asset_a,
            )
            return to_ticker(instrument_name, result[instrument_name.replace("/", "-")])
        except Exception as error:
            self.logger.exception(traceback.print_exc())
            msg = f"Failed to fetch ticker: {error}"
            raise ExchangeError(msg) from error

    async def fetch_balance(self, *args, **kwargs):
        """Fetch all balances."""
        await self.ensure_connected()
        del args, kwargs
        try:
            result = await self.client.collateral.get()
            balances = [to_balance(balance) for balance in result.collaterals]
        except Exception as error:
            traceback.print_exc()
            self.logger.exception(f"Failed to fetch balances: {error}")
            balances = []

        return Balances(
            balances=balances,
        )

    async def fetch_positions(self, *args, **kwargs):
        """Fetch all positions."""
        msg = f"{self.__class__.__name__}.fetch_positions"
        raise NotImplementedError(msg)
        del args
        params = kwargs.get("params", {})
        if "currency" in params:
            params["currency"] = Currency(params["currency"].upper())
        try:
            result = await self.client.get_positions(**params)
            data = result
        except Exception as error:  # noqa
            traceback.print_exc()
            data = []
        return data

    async def fetch_open_orders(self, *args, **kwargs):
        """Fetch all open orders."""
        await self.ensure_connected()
        del args, kwargs
        try:
            result = await self.client.orders.list_open()
        except Exception as error:  # noqa
            traceback.print_exc()
            result = []

        orders = [to_order(order) for order in result]
        return Orders(
            orders=orders,
        )

    async def watch_order_book(self, *args, **kwargs):
        """Watch the order book."""
        msg = f"{self.__class__.__name__}.watch_order_book"
        raise NotImplementedError(msg)
        params = kwargs.get("params", {})
        try:
            result = await self.client.watch_order_book(instrument_name=args[0], **params)
        except Exception:
            traceback.print_exc()
            raise
        return OrderBook(
            **result,
            exchange_id=self.exchange_id,
        )

    async def close(self):
        """Close the client."""
        return True

    async def create_order(self, *args, retries=0, **kwargs):
        """Create an order."""

        params = {
            "amount": kwargs["amount"],
            "direction": DeriveOrderSide(kwargs["side"]),
            "instrument_name": kwargs["symbol"].replace("/", "-"),
            "limit_price": kwargs["price"],
            "order_type": DeriveOrderType(kwargs["type"]),
            "time_in_force": DeriveTimeInForce.ioc if kwargs.get("immediate_or_cancel") else DeriveTimeInForce.gtc,
        }
        try:
            order_response = await self.client.orders.create(**params)
            return to_order(order_response)
        except ApiException as error:
            if "Zero liquidity for market or IOC/FOK order" in str(error):
                self.logger.exception(f"Failed to create order initially! retries: {retries}")
                if retries > 0:
                    await asyncio.sleep(1)
                    return await self.create_order(*args, **kwargs, retries=retries - 1)

                return self.get_failed_order_json(
                    error,
                    kwargs,
                )
            if "Self-crossing disallowed" in str(error):
                return self.get_failed_order_json(
                    error,
                    kwargs,
                )

            self.logger.exception(f"Failed to create order: {error} Retries: {retries}")
            msg = f"Failed to create order: {error} with unknown error"
            raise NotImplementedError(msg) from error

    def parse_order(self, api_call: dict[str, Any], exchange_id) -> Order:  # noqa: ARG002
        """Create an order from an api call."""
        return api_call

    def get_failed_order_json(self, error, kwargs):
        """Get a failed order json."""
        del error
        return {
            "order_status": "failed",
            "instrument_name": kwargs["symbol"],
            "order_type": kwargs["type"],
            "direction": kwargs["side"],
            "limit_price": kwargs.get("price"),
            "amount": kwargs["amount"],
            "filled_amount": 0,
            "average_price": 0,
            "creation_timestamp": datetime.datetime.now(tz=datetime.UTC).timestamp(),
        }

    def set_approval(self, *args, **kwargs):
        """Set approval for an asset."""
        del args, kwargs
        self.logger.info("Dummy method for derive")
