"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from packages.eightballer.protocols.orders.primitives import (
    Float,
)


# ruff: noqa: N806, C901, PLR0912, PLR0914, PLR0915, A001, UP007
# N806     - variable should be lowercase
# C901     - function is too complex
# PLR0912  - too many branches
# PLR0914  - too many local variables
# PLR0915  - too many statements
# A001     - shadowing builtin names like `id` and `type`
# UP007    - Use X | Y for type annotations  # NOTE: important edge case pydantic-hypothesis interaction!

MAX_PROTO_SIZE = 2 * 1024 * 1024 * 1024


class ErrorCode(IntEnum):
    """ErrorCode."""

    UNKNOWN_MARKET = 0
    INSUFFICIENT_FUNDS = 1
    UNKNOWN_ORDER = 2
    API_ERROR = 3

    @staticmethod
    def encode(pb_obj, error_code: ErrorCode) -> None:
        """Encode ErrorCode to protobuf."""
        pb_obj.error_code = error_code

    @classmethod
    def decode(cls, pb_obj) -> ErrorCode:
        """Decode protobuf to ErrorCode."""
        return cls(pb_obj.error_code)


class Order(BaseModel):
    """Order."""

    symbol: str
    status: OrderStatus
    side: OrderSide
    type: OrderType
    price: Optional[Float] = None
    exchange_id: Optional[str] = None
    id: Optional[str] = None
    client_order_id: Optional[str] = None
    info: Optional[str] = None
    ledger_id: Optional[str] = None
    asset_a: Optional[str] = None
    asset_b: Optional[str] = None
    timestamp: Optional[Float] = None
    datetime: Optional[str] = None
    time_in_force: Optional[str] = None
    post_only: Optional[bool] = None
    last_trade_timestamp: Optional[Float] = None
    stop_price: Optional[Float] = None
    trigger_price: Optional[Float] = None
    cost: Optional[Float] = None
    amount: Optional[Float] = None
    filled: Optional[Float] = None
    remaining: Optional[Float] = None
    fee: Optional[Float] = None
    average: Optional[Float] = None
    trades: Optional[str] = None
    fees: Optional[str] = None
    last_update_timestamp: Optional[Float] = None
    reduce_only: Optional[bool] = None
    take_profit_price: Optional[Float] = None
    stop_loss_price: Optional[Float] = None
    immediate_or_cancel: Optional[Float] = None

    @staticmethod
    def encode(proto_obj, order: Order) -> None:
        """Encode Order to protobuf."""
        proto_obj.symbol = order.symbol
        OrderStatus.encode(proto_obj.status, order.status)
        OrderSide.encode(proto_obj.side, order.side)
        OrderType.encode(proto_obj.type, order.type)
        if order.price is not None:
            proto_obj.price = order.price
        if order.exchange_id is not None:
            proto_obj.exchange_id = order.exchange_id
        if order.id is not None:
            proto_obj.id = order.id
        if order.client_order_id is not None:
            proto_obj.client_order_id = order.client_order_id
        if order.info is not None:
            proto_obj.info = order.info
        if order.ledger_id is not None:
            proto_obj.ledger_id = order.ledger_id
        if order.asset_a is not None:
            proto_obj.asset_a = order.asset_a
        if order.asset_b is not None:
            proto_obj.asset_b = order.asset_b
        if order.timestamp is not None:
            proto_obj.timestamp = order.timestamp
        if order.datetime is not None:
            proto_obj.datetime = order.datetime
        if order.time_in_force is not None:
            proto_obj.time_in_force = order.time_in_force
        if order.post_only is not None:
            proto_obj.post_only = order.post_only
        if order.last_trade_timestamp is not None:
            proto_obj.last_trade_timestamp = order.last_trade_timestamp
        if order.stop_price is not None:
            proto_obj.stop_price = order.stop_price
        if order.trigger_price is not None:
            proto_obj.trigger_price = order.trigger_price
        if order.cost is not None:
            proto_obj.cost = order.cost
        if order.amount is not None:
            proto_obj.amount = order.amount
        if order.filled is not None:
            proto_obj.filled = order.filled
        if order.remaining is not None:
            proto_obj.remaining = order.remaining
        if order.fee is not None:
            proto_obj.fee = order.fee
        if order.average is not None:
            proto_obj.average = order.average
        if order.trades is not None:
            proto_obj.trades = order.trades
        if order.fees is not None:
            proto_obj.fees = order.fees
        if order.last_update_timestamp is not None:
            proto_obj.last_update_timestamp = order.last_update_timestamp
        if order.reduce_only is not None:
            proto_obj.reduce_only = order.reduce_only
        if order.take_profit_price is not None:
            proto_obj.take_profit_price = order.take_profit_price
        if order.stop_loss_price is not None:
            proto_obj.stop_loss_price = order.stop_loss_price
        if order.immediate_or_cancel is not None:
            proto_obj.immediate_or_cancel = order.immediate_or_cancel

    @classmethod
    def decode(cls, proto_obj) -> Order:
        """Decode proto_obj to Order."""
        symbol = proto_obj.symbol
        status = OrderStatus.decode(proto_obj.status)
        side = OrderSide.decode(proto_obj.side)
        type = OrderType.decode(proto_obj.type)
        price = proto_obj.price if proto_obj.price is not None and proto_obj.HasField("price") else None
        exchange_id = (
            proto_obj.exchange_id if proto_obj.exchange_id is not None and proto_obj.HasField("exchange_id") else None
        )
        id = proto_obj.id if proto_obj.id is not None and proto_obj.HasField("id") else None
        client_order_id = (
            proto_obj.client_order_id
            if proto_obj.client_order_id is not None and proto_obj.HasField("client_order_id")
            else None
        )
        info = proto_obj.info if proto_obj.info is not None and proto_obj.HasField("info") else None
        ledger_id = proto_obj.ledger_id if proto_obj.ledger_id is not None and proto_obj.HasField("ledger_id") else None
        asset_a = proto_obj.asset_a if proto_obj.asset_a is not None and proto_obj.HasField("asset_a") else None
        asset_b = proto_obj.asset_b if proto_obj.asset_b is not None and proto_obj.HasField("asset_b") else None
        timestamp = proto_obj.timestamp if proto_obj.timestamp is not None and proto_obj.HasField("timestamp") else None
        datetime = proto_obj.datetime if proto_obj.datetime is not None and proto_obj.HasField("datetime") else None
        time_in_force = (
            proto_obj.time_in_force
            if proto_obj.time_in_force is not None and proto_obj.HasField("time_in_force")
            else None
        )
        post_only = proto_obj.post_only if proto_obj.post_only is not None and proto_obj.HasField("post_only") else None
        last_trade_timestamp = (
            proto_obj.last_trade_timestamp
            if proto_obj.last_trade_timestamp is not None and proto_obj.HasField("last_trade_timestamp")
            else None
        )
        stop_price = (
            proto_obj.stop_price if proto_obj.stop_price is not None and proto_obj.HasField("stop_price") else None
        )
        trigger_price = (
            proto_obj.trigger_price
            if proto_obj.trigger_price is not None and proto_obj.HasField("trigger_price")
            else None
        )
        cost = proto_obj.cost if proto_obj.cost is not None and proto_obj.HasField("cost") else None
        amount = proto_obj.amount if proto_obj.amount is not None and proto_obj.HasField("amount") else None
        filled = proto_obj.filled if proto_obj.filled is not None and proto_obj.HasField("filled") else None
        remaining = proto_obj.remaining if proto_obj.remaining is not None and proto_obj.HasField("remaining") else None
        fee = proto_obj.fee if proto_obj.fee is not None and proto_obj.HasField("fee") else None
        average = proto_obj.average if proto_obj.average is not None and proto_obj.HasField("average") else None
        trades = proto_obj.trades if proto_obj.trades is not None and proto_obj.HasField("trades") else None
        fees = proto_obj.fees if proto_obj.fees is not None and proto_obj.HasField("fees") else None
        last_update_timestamp = (
            proto_obj.last_update_timestamp
            if proto_obj.last_update_timestamp is not None and proto_obj.HasField("last_update_timestamp")
            else None
        )
        reduce_only = (
            proto_obj.reduce_only if proto_obj.reduce_only is not None and proto_obj.HasField("reduce_only") else None
        )
        take_profit_price = (
            proto_obj.take_profit_price
            if proto_obj.take_profit_price is not None and proto_obj.HasField("take_profit_price")
            else None
        )
        stop_loss_price = (
            proto_obj.stop_loss_price
            if proto_obj.stop_loss_price is not None and proto_obj.HasField("stop_loss_price")
            else None
        )
        immediate_or_cancel = (
            proto_obj.immediate_or_cancel
            if proto_obj.immediate_or_cancel is not None and proto_obj.HasField("immediate_or_cancel")
            else None
        )
        return cls(
            symbol=symbol,
            status=status,
            side=side,
            type=type,
            price=price,
            exchange_id=exchange_id,
            id=id,
            client_order_id=client_order_id,
            info=info,
            ledger_id=ledger_id,
            asset_a=asset_a,
            asset_b=asset_b,
            timestamp=timestamp,
            datetime=datetime,
            time_in_force=time_in_force,
            post_only=post_only,
            last_trade_timestamp=last_trade_timestamp,
            stop_price=stop_price,
            trigger_price=trigger_price,
            cost=cost,
            amount=amount,
            filled=filled,
            remaining=remaining,
            fee=fee,
            average=average,
            trades=trades,
            fees=fees,
            last_update_timestamp=last_update_timestamp,
            reduce_only=reduce_only,
            take_profit_price=take_profit_price,
            stop_loss_price=stop_loss_price,
            immediate_or_cancel=immediate_or_cancel,
        )


class OrderSide(IntEnum):
    """OrderSide."""

    BUY = 0
    SELL = 1

    @staticmethod
    def encode(pb_obj, order_side: OrderSide) -> None:
        """Encode OrderSide to protobuf."""
        pb_obj.order_side = order_side

    @classmethod
    def decode(cls, pb_obj) -> OrderSide:
        """Decode protobuf to OrderSide."""
        return cls(pb_obj.order_side)


class OrderStatus(IntEnum):
    """OrderStatus."""

    NEW = 0
    SUBMITTED = 1
    OPEN = 2
    PARTIALLY_FILLED = 3
    CANCELLED = 4
    FILLED = 5
    CLOSED = 6
    EXPIRED = 7
    FAILED = 9

    @staticmethod
    def encode(pb_obj, order_status: OrderStatus) -> None:
        """Encode OrderStatus to protobuf."""
        pb_obj.order_status = order_status

    @classmethod
    def decode(cls, pb_obj) -> OrderStatus:
        """Decode protobuf to OrderStatus."""
        return cls(pb_obj.order_status)


class OrderType(IntEnum):
    """OrderType."""

    LIMIT = 0
    MARKET = 1

    @staticmethod
    def encode(pb_obj, order_type: OrderType) -> None:
        """Encode OrderType to protobuf."""
        pb_obj.order_type = order_type

    @classmethod
    def decode(cls, pb_obj) -> OrderType:
        """Decode protobuf to OrderType."""
        return cls(pb_obj.order_type)


class Orders(BaseModel):
    """Orders."""

    orders: list[Order]

    @staticmethod
    def encode(proto_obj, orders: Orders) -> None:
        """Encode Orders to protobuf."""
        for item in orders.orders:
            Order.encode(proto_obj.orders.add(), item)

    @classmethod
    def decode(cls, proto_obj) -> Orders:
        """Decode proto_obj to Orders."""
        orders = [Order.decode(item) for item in proto_obj.orders]
        return cls(orders=orders)


for cls in BaseModel.__subclasses__():
    if cls.__module__ == __name__:
        cls.model_rebuild()
