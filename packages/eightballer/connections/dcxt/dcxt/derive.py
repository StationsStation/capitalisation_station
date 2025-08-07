"""An interface for the Derive API."""

import json
import asyncio
import datetime
import traceback
from typing import Any
from decimal import Decimal
from pathlib import Path

from derive_client.data_types import (
    OrderSide as DeriveOrderSide,
    OrderType as DeriveOrderType,
    Environment,
    OrderStatus as DeriveOrderStatus,
    TimeInForce as DeriveTimeInForce,
    InstrumentType,
    UnderlyingCurrency,
)
from derive_client.exceptions import ApiException
from derive_client.clients.async_client import AsyncClient as DeriveAsyncClient

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
        future=api_result["instrument_type"] == InstrumentType.PERP,
        option=api_result["instrument_type"] == InstrumentType.OPTION,
        active=api_result["is_active"],
        taker=api_result["taker_fee_rate"],
        maker=api_result["maker_fee_rate"],
    )


def to_ticker(api_result):
    """Parse from the API result to a Ticker object.
    {
    'instrument_type': 'perp',
    'instrument_name': 'ETH-PERP',
    'scheduled_activation': 1701840228,
    'scheduled_deactivation': 9223372036854775807,
    'is_active': True,
    'tick_size': '0.01',
    'minimum_amount': '0.1',
    'maximum_amount': '10000',
    'amount_step': '0.01',
    'mark_price_fee_rate_cap': '0',
    'maker_fee_rate': '0.0001',
    'taker_fee_rate': '0.0006',
    'base_fee': '0.5',
    'base_currency': 'ETH',
    'quote_currency': 'USD',
    'option_details': None,
    'perp_details': {
        'index': 'ETH-USD',
        'max_rate_per_hour': '0.004',
        'min_rate_per_hour': '-0.004',
        'static_interest_rate': '0.0000125',
        'aggregate_funding': '162.946932236049674753',
        'funding_rate': '0.0000455805326227'
    },
    'base_asset_address': '0xAf65752C4643E25C02F693f9D4FE19cF23a095E3',
    'base_asset_sub_id': '0',
    'best_ask_amount': '19.53',
    'best_ask_price': '3584.14',
    'best_bid_amount': '19.53',
    'best_bid_price': '3582.35',
    'option_pricing': None,
    'index_price': '3582.84',
    'mark_price': '3584.458005555555834112',
    'stats': {
        'contract_volume': '550.16',
        'num_trades': '1504',
        'open_interest': '192.724138686180397137',
        'high': '3673.83',
        'low': '3530.19',
        'percent_change': '0.00942',
        'usd_change': '33.45'
    },
    'timestamp': 1710755194000,
    'min_price': '3413.85',
    'max_price': '3763.6'.
    """
    return Ticker(
        symbol=api_result["instrument_name"],
        timestamp=api_result["timestamp"],
        datetime=datetime.datetime.fromtimestamp(api_result["timestamp"] / 1000, tz=TZ).isoformat(),
        high=float(api_result["stats"]["high"]),
        low=float(api_result["stats"]["low"]),
        bid=float(api_result["best_bid_price"]),
        bidVolume=float(api_result["best_bid_amount"]),
        ask=float(api_result["best_ask_price"]),
        askVolume=float(api_result["best_ask_amount"]),
        close=float(api_result["mark_price"]),
        last=float(api_result["mark_price"]),
        change=float(api_result["stats"]["usd_change"]),
        percentage=float(api_result["stats"]["percent_change"]),
        baseVolume=float(api_result["stats"]["contract_volume"]),
        info=json.dumps(
            {"index_price": float(api_result["index_price"]), "mark_price": float(api_result["mark_price"])}
        ),
    )


def to_balance(api_result):
    """{
    'asset_type': 'erc20',
    'asset_name': 'USDC',
    'currency': 'USDC',
    'amount': '0.003987628553156971',
    'mark_price': '1',
    'mark_value': '0.0039877010299821909547479670266056928085163235664368',
    'cumulative_interest': '0.0039877010299821908952647395145769493641777913569316',
    'pending_interest': '7.24768252198952647395145769493641777913569316E-8',
    'initial_margin': '0.0039877010299821909547479670266056928085163235664368',
    'maintenance_margin': '0.0039877010299821909547479670266056928085163235664368'
    }.
    """
    return Balance(
        asset_id=api_result["currency"],
        free=float(api_result["amount"]),
        used=0,
        total=float(api_result["amount"]),
        is_native=False,
    )


def to_position(api_result):
    """[
    {
        'instrument_type': 'option',
        'instrument_name': 'ETH-20240322-3900-C',
        'amount': '-6.3',
        'average_price': '38.251279999999999895079365079365079365079365079365',
        'realized_pnl': '0',
        'unrealized_pnl': '126.829653299999999339',
        'net_settlements': '0',
        'cumulative_funding': '0',
        'pending_funding': '0',
        'mark_price': '18.119589',
        'index_price': '3556.44999999999967232',
        'delta': '0.134193',
        'gamma': '0.000781',
        'vega': '0.7962',
        'theta': '-7.673138',
        'mark_value': '-114.1534124761641209033768973313271999359130859375',
        'maintenance_margin': '-485.58486746802691413904540240764617919921875',
        'initial_margin': '-578.442731215992580473539419472217559814453125',
        'open_orders_margin': '0',
        'leverage': None,
        'liquidation_price': '47440.491107822048240348605896518565714359283447266',
        'creation_timestamp': 1710616517260
    },
    {
        'instrument_type': 'perp',
        'instrument_name': 'ETH-PERP',
        'amount': '6.31',
        'average_price': '3890.8895947970557939901743264659270998415213946117',
        'realized_pnl': '-462.06600328057794275',
        'unrealized_pnl': '-2100.3656899749795800907999999999999999999999999998',
        'net_settlements': '16.882700747243587876',
        'cumulative_funding': '-108.82798341841185392297',
        'pending_funding': '-98.29803748694663830697',
        'mark_price': '3558.02656944444413312',
        'index_price': '3556.44999999999967232',
        'delta': '1',
        'gamma': '0',
        'vega': '0',
        'theta': '0',
        'mark_value': '-2215.54642820917069911956787109375',
        'maintenance_margin': '-7379.01194384805785375647246837615966796875',
        'initial_margin': '-8669.878322757780551910400390625',
        'open_orders_margin': '0',
        'leverage': '0.82999134418353139253671107432550912457164708970823',
        'liquidation_price': None,
        'creation_timestamp': 1710434366705
    }
    ].
    """
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
    DeriveOrderStatus.OPEN: OrderStatus.OPEN.name,
    DeriveOrderStatus.FILLED: OrderStatus.FILLED.name,
    DeriveOrderStatus.CANCELLED: OrderStatus.CANCELLED.name,
    DeriveOrderStatus.REJECTED: OrderStatus.FAILED.name,
    DeriveOrderStatus.EXPIRED: OrderStatus.EXPIRED.name,
}
DERIVE_ORDER_TYPE_MAP = {
    DeriveOrderType.LIMIT: OrderType.LIMIT.name,
    DeriveOrderType.MARKET: OrderType.MARKET.name,
}


def to_order(api_result):
    """{
        'subaccount_id': 305,
        'order_id': 'fff6bf6d-4fc2-42d3-be76-da209e7ca1eb',
        'instrument_name': 'ETH-20240322-3900-C',
        'direction': 'sell',
        'label': '',
        'quote_id': None,
        'creation_timestamp': 1710616517152,
        'last_update_timestamp': 1710616517152,
        'limit_price': '39.7',
        'amount': '6.3',
        'filled_amount': '6.3',
        'average_price': '39.7',
        'order_fee': '9.126936000000000661',
        'order_type': 'limit',
        'time_in_force': 'gtc',
        'order_status': 'filled',
        'max_fee': '53.19',
        'signature_expiry_sec': 1711094399,
        'nonce': 1710616516996107,
        'signer': '0x86535B713830B2CFc976799C95Ef799428b8661B',
        'signature':
    '0xf0cfcae8c6c32a0b1b692b83065df24873cd17cb4670495ba200aa777a5f
    0235680d91aeb9560520ceb4b91f2019cd4a14a16d82e9604b73d859b04a0afc10fa1c',
        'cancel_reason': '',
        'mmp': False,
        'is_transfer': False,
        'replaced_order_id': None,
        'trigger_type': None,
        'trigger_price_type': None,
        'trigger_price': None,
        'trigger_reject_message': None
        }.

        converts to;'
        @dataclass
        class Order:
            # This class represents an instance of Orders

            id: Optional[str] = None
            exchange_id: Optional[str] = None
            client_order_id: Optional[str] = None
            timestamp: Optional[float] = None
            datetime: Optional[str] = None
            last_trade_timestamp: Optional[float] = None
            status: Optional[OrderStatus] = None
            symbol: Optional[str] = None
            type: Optional[OrderType] = None
            time_in_force: Optional[str] = None
            post_only: Optional[bool] = None
            side: Optional[OrderSide] = None
            price: Optional[float] = None
            stop_price: Optional[float] = None
            trigger_price: Optional[float] = None
            cost: Optional[float] = None
            amount: Optional[float] = None
            filled: Optional[float] = None
            remaining: Optional[float] = None
            fee: Optional[float] = None
            average: Optional[float] = None
            trades: Optional[str] = None
            fees: Optional[str] = None
            last_update_timestamp: Optional[float] = None
            reduce_only: Optional[bool] = None
            take_profit_price: Optional[float] = None
            stop_loss_price: Optional[float] = None
    """

    return Order(
        id=api_result["order_id"],
        exchange_id="derive",
        client_order_id=api_result["order_id"],
        timestamp=api_result["creation_timestamp"],
        datetime=datetime.datetime.fromtimestamp(api_result["creation_timestamp"] / 1000, tz=TZ).isoformat(),
        last_trade_timestamp=api_result["creation_timestamp"],
        status=map_status_to_enum(api_result["order_status"]),
        symbol=api_result["instrument_name"],
        type=map_order_type_to_enum(api_result["order_type"]),
        time_in_force=api_result["time_in_force"],
        side=OrderSide.BUY if api_result["direction"] == "buy" else OrderSide.SELL,
    )


def from_camelize(name: str) -> str:
    """Convert a camel case name to a snake case name."""
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")


def map_status_to_enum(status):
    """Map the status to order protocol status."""
    mapping = {
        "open": OrderStatus.OPEN,
        "new": OrderStatus.OPEN,
        "Order queued for cancellation": OrderStatus.CANCELLED,
        "closed": OrderStatus.CLOSED,
        "cancelled": OrderStatus.CANCELLED,
        "filled": OrderStatus.FILLED,
        "partially_filled": OrderStatus.PARTIALLY_FILLED,
        "failed": OrderStatus.FAILED,
        "expired": OrderStatus.EXPIRED,
    }
    if status not in mapping:
        msg = f"Unknown status: {status}"
        raise ValueError(msg)
    return mapping[status]


def map_order_type_to_enum(order_type: str) -> OrderType:
    """Map the order type to order protocol type."""
    mapping = {
        "limit": OrderType.LIMIT,
        "market": OrderType.MARKET,
    }
    if order_type not in mapping:
        msg = f"Unknown order type: {order_type}"
        raise ValueError(msg)
    return mapping[order_type]


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
            private_key=private_key,
            subaccount_id=kwargs.get("subaccount_id"),
            wallet=kwargs["wallet"],
            env=Environment(kwargs.get("environment")),
            logger=kwargs.get("logger"),
        )
        self.logger = kwargs.get("logger")

    async def fetch_markets(self, *args, **kwargs):
        """Fetch all markets."""
        del args
        params = kwargs.get("params", {})
        if "currency" in params:
            params["currency"] = UnderlyingCurrency(params["currency"].lower())
        if "type" in params:
            params["type"] = InstrumentType(params["type"].lower())
        result = await self.client.fetch_instruments(**params)
        markets = [to_market(market) for market in result]
        return Markets(
            markets=markets,
        )

    async def fetch_tickers(self, *args, **kwargs):
        """Fetch all tickers."""
        del args
        params = kwargs.get("params", {})
        if "currency" in params:
            params["currency"] = UnderlyingCurrency(params["currency"].lower())
        if "type" in params:
            params["type"] = InstrumentType(params["type"].lower())

        try:
            result = await self.client.fetch_tickers(**params)
            data = result.values()
        except Exception as error:  # noqa
            traceback.print_exc()
            data = []

        tickers = [to_ticker(ticker) for ticker in data]
        return Tickers(
            tickers=tickers,
        )

    async def fetch_ticker(self, *args, symbol, asset_a, asset_b, **kwargs):
        """Fetch all tickers."""
        del args, kwargs  # should parse from name to instrument type?
        if (not asset_a and not asset_b) and (not symbol):
            msg = "Either asset_a, asset_b or symbol must be provided."
            raise ValueError(msg)

        instrument_name = f"{asset_a}-{asset_b}".upper() if not symbol else symbol.upper().replace("/", "-")
        try:
            result = await self.client.fetch_ticker(instrument_name=instrument_name)
            return to_ticker(result)
        except Exception as error:
            self.logger.exception(traceback.print_exc())
            msg = f"Failed to fetch ticker: {error}"
            raise ExchangeError(msg) from error

    async def fetch_balance(self, *args, **kwargs):
        """Fetch all balances."""
        del args, kwargs
        try:
            result = await self.client.get_collaterals()
            balances = [to_balance(balance) for balance in result]
        except Exception as error:
            traceback.print_exc()
            self.logger.exception(f"Failed to fetch balances: {error}")
            balances = []

        return Balances(
            balances=balances,
        )

    async def fetch_positions(self, *args, **kwargs):
        """Fetch all positions."""
        del args
        params = kwargs.get("params", {})
        if "currency" in params:
            params["currency"] = UnderlyingCurrency(params["currency"].lower())
        try:
            result = await self.client.get_positions(**params)
            data = result
        except Exception as error:  # noqa
            traceback.print_exc()
            data = []
        return data

    async def fetch_open_orders(self, *args, **kwargs):
        """Fetch all open orders."""
        del args
        params = kwargs.get("params", {})
        try:
            result = await self.client.get_open_orders(status=DeriveOrderStatus.OPEN.value, **params)
        except Exception as error:  # noqa
            traceback.print_exc()
            result = []

        orders = [to_order(order) for order in result]
        return Orders(
            orders=orders,
        )

    async def watch_order_book(self, *args, **kwargs):
        """Watch the order book."""
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

        # we make sure to re-login the client.
        await self.client.connect_ws()
        await self.client.login_client()

        def get_instrument_type(instrument_name):
            if "-" in instrument_name:
                return InstrumentType.ERC20
            msg = f"Unknown instrument type: {instrument_name}"
            raise ValueError(msg)

        def get_underlying_currency(currency):
            return UnderlyingCurrency(currency.lower())

        asset_a, _asset_b = kwargs["symbol"].split("-")

        params = {
            "instrument_name": kwargs["symbol"],
            "amount": kwargs["amount"],
            "price": kwargs.get("price"),
            "order_type": DeriveOrderType(kwargs["type"]),
            "side": DeriveOrderSide(kwargs["side"]),
            "instrument_type": get_instrument_type(kwargs["symbol"]),
            "underlying_currency": get_underlying_currency(asset_a),
            "time_in_force": DeriveTimeInForce.IOC if kwargs.get("immediate_or_cancel") else DeriveTimeInForce.GTC,
        }
        try:
            return await self.client.create_order(**params)
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

    def parse_order(self, api_call: dict[str, Any], exchange_id) -> Order:
        """Create an order from an api call."""
        kwargs = {from_camelize(key): value for key, value in api_call.items()}
        if all(
            [
                kwargs["order_status"] == "filled",
                Decimal(kwargs["filled_amount"])
                >= Decimal(
                    kwargs["amount"],
                ),
            ]
        ):
            kwargs["status"] = "filled"

        order_key = "order_status" if "order_status" in kwargs else "status"
        return Order(
            id=api_call.get("order_id"),
            symbol=kwargs["instrument_name"],
            status=map_status_to_enum(kwargs[order_key]),
            type=map_order_type_to_enum(kwargs["order_type"]),
            side=OrderSide.BUY if kwargs["direction"] == "buy" else OrderSide.SELL,
            price=float(kwargs["limit_price"]),
            amount=float(kwargs["amount"]),
            filled=float(kwargs["filled_amount"]),
            average=float(kwargs["average_price"]),
            timestamp=kwargs["creation_timestamp"],
            exchange_id=exchange_id,
            ledger_id=exchange_id,
        )

    def set_approval(self, *args, **kwargs):
        """Set approval for an asset."""
        del args, kwargs
        self.logger.info("Dummy method for derive")
