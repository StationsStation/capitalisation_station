"""Custom types for the protocol."""

from enum import Enum
from typing import Any

from pydantic import BaseModel


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNKNOWN_MARKET = 0
    INSUFFICIENT_FUNDS = 1
    UNKNOWN_ORDER = 2
    API_ERROR = 3

    @staticmethod
    def encode(error_code_protobuf_object, error_code_object: "ErrorCode") -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the error_code_protobuf_object argument is matched with the instance of this class
        in the 'error_code_object' argument.



        Args:
        ----
               error_code_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               error_code_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        error_code_protobuf_object.error_code = error_code_object.value

    @classmethod
    def decode(cls, error_code_protobuf_object) -> "ErrorCode":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'error_code_protobuf_object' argument.

        'error_code_protobuf_object' argument.


        Args:
        ----
               error_code_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        return ErrorCode(error_code_protobuf_object.error_code)


class OrderSide(Enum):
    """This class represents an instance of OrderSide."""

    BUY = 0
    SELL = 1

    @staticmethod
    def encode(order_side_protobuf_object, order_side_object: "OrderSide") -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the order_side_protobuf_object argument is matched with the instance of this class
        in the 'order_side_object' argument.



        Args:
        ----
               order_side_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               order_side_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        order_side_protobuf_object.order_side = order_side_object.value

    @classmethod
    def decode(cls, order_side_protobuf_object) -> "OrderSide":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'order_side_protobuf_object' argument.

        'order_side_protobuf_object' argument.


        Args:
        ----
               order_side_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        return OrderSide(order_side_protobuf_object.order_side)


class OrderStatus(Enum):
    """This class represents an instance of OrderStatus."""

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
    def encode(order_status_protobuf_object, order_status_object: "OrderStatus") -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the order_status_protobuf_object argument is matched with the instance of this
        class in the 'order_status_object' argument.



        Args:
        ----
               order_status_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               order_status_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        order_status_protobuf_object.order_status = order_status_object.value

    @classmethod
    def decode(cls, order_status_protobuf_object) -> "OrderStatus":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'order_status_protobuf_object' argument.

        'order_status_protobuf_object' argument.


        Args:
        ----
               order_status_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        return OrderStatus(order_status_protobuf_object.order_status)


class OrderType(Enum):
    """This class represents an instance of OrderType."""

    LIMIT = 0
    MARKET = 1

    @staticmethod
    def encode(order_type_protobuf_object, order_type_object: "OrderType") -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the order_type_protobuf_object argument is matched with the instance of this class
        in the 'order_type_object' argument.



        Args:
        ----
               order_type_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               order_type_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        order_type_protobuf_object.order_type = order_type_object.value

    @classmethod
    def decode(cls, order_type_protobuf_object) -> "OrderType":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'order_type_protobuf_object' argument.

        'order_type_protobuf_object' argument.


        Args:
        ----
               order_type_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        return OrderType(order_type_protobuf_object.order_type)


class BaseCustomEncoder(BaseModel):
    """This class is a base class for encoding and decoding protocol buffer objects."""

    @staticmethod
    def encode(ps_response_protobuf_object: Any, ps_response_object: Any) -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the ps_response_protobuf_object argument is matched with the instance of this
        class in the 'ps_response_object' argument.



        Args:
        ----
               ps_response_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               ps_response_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        for key, value in ps_response_object.__dict__.items():
            current_attr = getattr(ps_response_protobuf_object, key)
            if isinstance(value, Enum):
                type(value).encode(current_attr, value)
                continue
            if isinstance(value, dict):
                current_attr.update(value)
                continue
            if isinstance(value, list):
                current_attr.extend(value)
                continue
            setattr(ps_response_protobuf_object, key, value)

    @classmethod
    def decode(cls, ps_response_protobuf_object: Any) -> "Any":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'ps_response_protobuf_object' argument.

        'ps_response_protobuf_object' argument.


        Args:
        ----
               ps_response_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        keywords = list(cls.__annotations__.keys())
        kwargs = {}
        for keyword in keywords:
            proto_attr = getattr(ps_response_protobuf_object, keyword)
            if isinstance(proto_attr, Enum):
                kwargs[keyword] = type(proto_attr).decode(proto_attr)
                continue
            if isinstance(proto_attr, list):
                kwargs[keyword] = [type(proto_attr[0]).decode(item) for item in proto_attr]
                continue
            if isinstance(proto_attr, dict):
                kwargs[keyword] = dict(proto_attr.items())
                continue
            if str(type(proto_attr)) in CUSTOM_ENUM_MAP:
                kwargs[keyword] = CUSTOM_ENUM_MAP[str(type(proto_attr))].decode(proto_attr).value
                continue
            kwargs[keyword] = proto_attr
        return cls(**kwargs)

    def __eq__(self, other):
        """Check if two instances of this class are equal."""
        return self.dict() == other.dict()

    def __hash__(self):
        """Return the hash value of this instance."""
        return hash(self.dict())


class Order(BaseCustomEncoder):
    """This class represents an instance of Order."""

    symbol: str
    status: OrderStatus
    side: OrderSide
    type: OrderType
    price: float | None = None
    exchange_id: str | None = None
    id: str | None = None
    client_order_id: str | None = None
    info: str | None = None
    ledger_id: str | None = None
    asset_a: str | None = None
    asset_b: str | None = None
    timestamp: float | None = None
    datetime: str | None = None
    time_in_force: str | None = None
    post_only: bool | None = None
    last_trade_timestamp: float | None = None
    stop_price: float | None = None
    trigger_price: float | None = None
    cost: float | None = None
    amount: float | None = None
    filled: float | None = None
    remaining: float | None = None
    fee: float | None = None
    average: float | None = None
    trades: str | None = None
    fees: str | None = None
    last_update_timestamp: float | None = None
    reduce_only: bool | None = None
    take_profit_price: float | None = None
    stop_loss_price: float | None = None
    immediate_or_cancel: float | None = None


class Orders(BaseCustomEncoder):
    """This class represents an instance of Orders."""

    orders: list[Order] = []


CUSTOM_ENUM_MAP = {
    "<class 'orders_pb2.ErrorCode'>": ErrorCode,
    "<class 'orders_pb2.OrderStatus'>": OrderStatus,
    "<class 'orders_pb2.OrderType'>": OrderType,
    "<class 'orders_pb2.OrderSide'>": OrderSide,
}
