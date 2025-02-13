"""Custom types for the protocol."""

from enum import Enum
from typing import Any

from pydantic import BaseModel


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNKNOWN_EXCHANGE = 0
    UNKNOWN_POSITION = 1
    API_ERROR = 2

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


class PositionSide(Enum):
    """This class represents an instance of PositionSide."""

    LONG = 0
    SHORT = 1

    @staticmethod
    def encode(position_side_protobuf_object, position_side_object: "PositionSide") -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the position_side_protobuf_object argument is matched with the instance of this
        class in the 'position_side_object' argument.



        Args:
        ----
               position_side_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               position_side_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        position_side_protobuf_object.position_side = position_side_object.value

    @classmethod
    def decode(cls, position_side_protobuf_object) -> "PositionSide":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'position_side_protobuf_object' argument.

        'position_side_protobuf_object' argument.


        Args:
        ----
               position_side_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        return PositionSide(position_side_protobuf_object.position_side)


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


class Position(BaseCustomEncoder):
    """This class represents an instance of Position."""

    id: str
    symbol: str
    timestamp: int
    datetime: str
    last_update_timestamp: int
    initial_margin: float
    initial_margin_percentage: float
    maintenance_margin: float
    maintenance_margin_percentage: float
    entry_price: float
    notional: float
    leverage: float
    unrealized_pnl: float
    contracts: float
    contract_size: float
    margin_ratio: float
    liquidation_price: float
    mark_price: float
    last_price: float
    collateral: float
    margin_mode: str
    side: PositionSide
    percentage: float
    info: str
    size: float
    exchange_id: str
    hedged: str
    stop_loss_price: float
    take_profit_price: float


class Positions(BaseCustomEncoder):
    """This class represents an instance of Positions."""

    positions: list[Position] = []


CUSTOM_ENUM_MAP = {"<class 'positions_pb2.ErrorCode'>": ErrorCode, "<class 'positions_pb2.PositionSide'>": PositionSide}
