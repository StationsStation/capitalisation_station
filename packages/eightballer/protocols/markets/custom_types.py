"""Custom types for the protocol."""

from enum import Enum
from typing import Any

from pydantic import BaseModel


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNSUPPORTED_PROTOCOL = 0
    DECODING_ERROR = 1
    INVALID_MESSAGE = 2
    UNSUPPORTED_SKILL = 3
    INVALID_DIALOGUE = 4

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


class Market(BaseCustomEncoder):
    """This class represents an instance of Market."""

    id: str
    lowercase_id: str | None = None
    exchange_id: str | None = None
    symbol: str | None = None
    base: str | None = None
    quote: str | None = None
    settle: str | None = None
    base_id: str | None = None
    quote_id: str | None = None
    settle_id: str | None = None
    type: str | None = None
    spot: bool | None = None
    margin: bool | None = None
    swap: bool | None = None
    future: bool | None = None
    option: bool | None = None
    active: bool | None = None
    contract: bool | None = None
    linear: bool | None = None
    inverse: bool | None = None
    taker: float | None = None
    maker: float | None = None
    contract_size: float | None = None
    expiry: float | None = None
    expiry_datetime: str | None = None
    strike: float | None = None
    option_type: str | None = None
    precision: float | None = None
    limits: str | None = None
    info: str | None = None


class Markets(BaseCustomEncoder):
    """This class represents an instance of Markets."""

    markets: list[Market] = []


CUSTOM_ENUM_MAP = {"<class 'markets_pb2.ErrorCode'>": ErrorCode}
