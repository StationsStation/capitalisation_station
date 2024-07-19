"""Order protocol handler."""
import traceback
from datetime import datetime
from typing import Any, Dict, Optional, cast

import ccxt.async_support as ccxt  # pylint: disable=E0401,E0611

from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface
from packages.eightballer.protocols.orders.custom_types import Order, Orders, OrderSide, OrderStatus, OrderType
from packages.eightballer.protocols.orders.dialogues import BaseOrdersDialogues, OrdersDialogue
from packages.eightballer.protocols.orders.message import OrdersMessage

INTERVAL = 10


def from_id_to_instrument_name(instrument_id):
    """
    Convert from the id to the instrument name.
    input:
        ETH-27OCT23-2000-C
        ETH-27OCT23-2000-P

    output:
        ETH/USD:ETH-231027-2000-C
        ETH/USD:ETH-231027-2000-P

    """
    parts = instrument_id.split("-")
    if len(parts) != 4:
        raise ValueError(f"Invalid instrument id: {instrument_id}")
    symbol = parts[0]

    date = parts[1]
    if len(date) == 7:
        year = date[5:]
        month = date[2:5]
        day = date[:2]
    elif len(date) == 6:
        year = date[4:]
        month = date[1:4]
        day = date[:1]

    else:
        raise ValueError(f"Invalid instrument id: {instrument_id}")
    # we need to pad the day with a  if it's a single digit
    date_obj = datetime.strptime(str(month), "%b")
    month = date_obj.strftime("%m").upper()
    if int(month) < 10:
        month = f"0{int(month)}"
    if int(day) < 10:
        day = f"0{day}"
    date = f"{year}{month}{day}"
    return f"{symbol}/USD:ETH-{date}-{parts[2]}-{parts[3]}"


def from_camelize(name: str) -> str:
    """Convert a camel case name to a snake case name."""
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")


def from_api_call(api_call: Dict[str, Any], exchange_id) -> Order:
    """Create an order from an api call."""
    kwargs = {from_camelize(key): value for key, value in api_call.items()}
    del kwargs["info"]

    if all(
        [
            kwargs["status"] == "closed",
            kwargs["remaining"] == 0,
            kwargs["filled"] == kwargs["amount"],
        ]
    ):
        kwargs["status"] = "filled"
    kwargs["status"] = map_status_to_enum(kwargs["status"])
    kwargs["type"] = map_order_type_to_enum(kwargs["type"])
    kwargs["side"] = OrderSide.BUY if kwargs["side"] == "buy" else OrderSide.SELL
    kwargs["exchange_id"] = exchange_id
    return Order(**kwargs)


def order_from_settlement(settlement: Dict[str, Any], exchange_id) -> Order:
    """Create an order from a settlement txn."""
    size = float(settlement["position"])
    timestamp = int(settlement["timestamp"])
    symbol = from_id_to_instrument_name(settlement["instrument_name"])
    price = float(settlement["mark_price"])
    order_params = {
        "id": f"{timestamp}-{symbol}-delivery",
        "exchange_id": exchange_id,
        "timestamp": timestamp,
        "datetime": datetime.fromtimestamp(timestamp / 1000),
        "symbol": symbol,
        "amount": size,
        "price": price,
        "side": OrderSide.BUY if size < 0 else OrderSide.SELL,
        "type": OrderType.MARKET,
        "status": OrderStatus.FILLED,
    }
    return Order(**order_params)


def map_order_type_to_enum(order_type: str) -> OrderType:
    """Map the order type to order protocol type."""
    mapping = {
        "limit": OrderType.LIMIT,
        "market": OrderType.MARKET,
    }
    if order_type not in mapping:
        raise ValueError(f"Unknown order type: {order_type}")
    return mapping[order_type]


class PollingError(Exception):
    """Polling error."""


def map_status_to_enum(status):
    """Map the status to order protocol status"""
    mapping = {
        "open": OrderStatus.OPEN,
        "new": OrderStatus.OPEN,
        "Order queued for cancellation": OrderStatus.CANCELLED,
        "closed": OrderStatus.CLOSED,
        "canceled": OrderStatus.CANCELLED,
        "filled": OrderStatus.FILLED,
    }
    if status not in mapping:
        raise ValueError(f"Unknown status: {status}")
    return mapping[status]


def get_error(message: OrdersMessage, dialogue: OrdersDialogue, error_msg: str) -> OrdersMessage:
    """Get the error message."""
    response_message = cast(
        Optional[OrdersMessage],
        dialogue.reply(
            performative=OrdersMessage.Performative.ERROR,
            target_message=message,
            error_code=OrdersMessage.ErrorCode(1),
            error_msg=str(error_msg),
            error_data={"msg": b"{error_msg}"},
        ),
    )
    return response_message


class OrderInterface(BaseInterface):
    """Interface for the order protocol."""

    protocol_id = OrdersMessage.protocol_id
    dialogue_class = OrdersDialogue
    dialogues_class = BaseOrdersDialogues
    exchange_to_orders: Dict[str, list] = {}
    open_orders: Dict[str, list] = {}

    def process_api_orders(self, exchange_id: str, api_orders: Dict[str, dict]):
        """Process orders from the api to internal hashmap"""
        orders = {order["id"]: from_api_call(order, exchange_id) for order in api_orders}
        if exchange_id not in self.open_orders:
            self.open_orders[exchange_id] = orders
        return orders

    async def create_order(
        self, message: OrdersMessage, dialogue: OrdersDialogue, connection
    ) -> Optional[OrdersMessage]:
        """Submit an order to the appropriate exchange."""
        order = message.order
        exchange = connection.exchanges[order.exchange_id]

        try:
            res = await exchange.create_order(
                symbol=order.symbol,
                amount=order.amount,
                price=order.price,
                type=order.type.name.lower(),
                side=order.side.name.lower(),
            )
            updated_order = from_api_call(res, order.exchange_id)
            updated_order.client_order_id = order.client_order_id

        except ccxt.InsufficientFunds as base_error:
            order.status = OrderStatus.CANCELLED
            updated_order = order
            connection.logger.error(f"FAILED TO CREATE ORDER -> insufficient funds! {str(base_error)}")
        except (ccxt.ExchangeNotAvailable, ccxt.InvalidOrder) as base_error:
            return get_error(message, dialogue, str(base_error))
        response_message = dialogue.reply(
            target_message=message,
            performative=OrdersMessage.Performative.ORDER_CREATED,
            order=updated_order,
        )
        if order.exchange_id not in self.open_orders:
            self.open_orders[order.exchange_id] = {}
        self.open_orders[order.exchange_id][order.id] = order
        return response_message

    async def get_orders(self, message: OrdersMessage, dialogue: OrdersDialogue, connection):
        """Retrieve the open orders from the exchange."""

        def _get_kwargs():
            possible_kwargs = ["currency"]
            kwargs = {}
            for key in possible_kwargs:
                if hasattr(message, key):
                    kwarg = getattr(message, key)
                    if kwarg is not None:
                        kwargs[key] = kwarg
            return kwargs

        exchange = connection.exchanges[message.exchange_id]
        exchange_id = message.exchange_id
        try:
            open_orders = await exchange.fetch_open_orders(params=_get_kwargs())
            self.open_orders[exchange_id] = open_orders
            response_message = dialogue.reply(
                target_message=message,
                performative=OrdersMessage.Performative.ORDERS,
                orders=open_orders,
            )
            response_envelope = connection.build_envelope(request=message, response_message=response_message)
            connection.queue.put_nowait(response_envelope)
        except Exception as error:  # pylint: disable=W0703
            connection.logger.warning(
                f"Couldn't fetch open orders from {exchange_id}."
                f"The following error was encountered, {type(error).__name__}: {traceback.format_exc()}."
            )
            return get_error(message, dialogue, str(error))

    async def get_order(self, message: OrdersMessage, dialogue: OrdersDialogue, connection):
        """Retrieve an order from the exchange."""
        order = message.order
        exchange = connection.exchanges[order.exchange_id]
        exchange_id = order.exchange_id
        try:
            api_order = await exchange.fetch_order(order.id)
            new_order = from_api_call(api_order, exchange_id)
            new_order.client_order_id = order.client_order_id
            if exchange_id not in self.open_orders:
                self.open_orders[exchange_id] = {}
            self.open_orders[exchange_id][order.id] = new_order
        except ccxt.OrderNotFound as error:
            order.status = OrderStatus.CANCELLED
            new_order = order
            if exchange_id not in self.open_orders:
                self.open_orders[exchange_id] = {}
            if order.id in self.open_orders[exchange_id]:
                del self.open_orders[exchange_id][order.id]
            connection.logger.warning(
                f"Couldn't fetch order {order.id} from {exchange_id}. Removed from open orders."
                + f"The following error was encountered, {type(error).__name__}: {traceback.format_exc()}."
            )
        except Exception as error:  # pylint: disable=W0703
            connection.logger.warning(
                f"Couldn't fetch order {order.id} from {exchange_id}."
                f"The following error was encountered, {type(error).__name__}: {traceback.format_exc()}."
            )
            return get_error(message, dialogue, str(error))
        response_message = dialogue.reply(
            target_message=message,
            performative=OrdersMessage.Performative.ORDER,
            order=new_order,
        )
        response_envelope = connection.build_envelope(request=message, response_message=response_message)
        connection.queue.put_nowait(response_envelope)

    async def cancel_order(
        self, message: OrdersMessage, dialogue: OrdersDialogue, connection
    ) -> Optional[OrdersMessage]:
        """Cancel the order."""
        if (order := self.get_order_from_message(message)) is None:
            connection.logger.error(
                "Trying to cancel an order which has already been cancelled: %s",
                message.order.id,
            )
            return

        exchange = connection.exchanges[message.order.exchange_id]
        try:
            res = await exchange.cancel_order(message.order.id)
            connection.logger.info("Cancel order request: %s", res)
            order.status = OrderStatus.CANCELLED
            response_message = cast(
                Optional[OrdersMessage],
                dialogue.reply(
                    target_message=message,
                    performative=OrdersMessage.Performative.ORDER_CANCELLED,
                    order=order,
                ),
            )
            del self.open_orders[message.order.exchange_id][message.order.id]
            return response_message
        except Exception as error:  # pylint: disable=W0703
            connection.logger.info("Unknown Issue: %s", error)
            connection.logger.error(traceback.format_exc())
            return get_error(message, dialogue, str(error))

    def get_order_from_message(self, message):
        """Get internal order from message."""
        return self.open_orders[message.order.exchange_id].get(message.order.id)

    async def get_settlements(self, message: OrdersMessage, dialogue, connection):
        """
        Implement the get settlements method.
        """
        exchange = connection.exchanges[message.exchange_id]

        params = {}
        if message.currency is not None:
            params["currency"] = message.currency
        if message.end_timestamp is not None:
            params["end_timestamp"] = message.end_timestamp
        if message.start_timestamp is not None:
            params["start_timestamp"] = message.start_timestamp
        try:
            settlements = await exchange.private_get_get_settlement_history_by_currency(params=params)
            response_message = cast(
                Optional[OrdersMessage],
                dialogue.reply(
                    target_message=message,
                    performative=OrdersMessage.Performative.ORDERS,
                    orders=Orders(
                        [
                            order_from_settlement(settlement, message.exchange_id)
                            for settlement in settlements["result"]["settlements"]
                        ]
                    ),
                ),
            )
            return response_message
        except Exception as error:  # pylint: disable=W0703
            connection.logger.error(
                f"Couldn't fetch settlements from {exchange.id}."
                f"The following error was encountered, {type(error).__name__}: {traceback.format_exc()}."
            )
            return get_error(message, dialogue, str(error))
