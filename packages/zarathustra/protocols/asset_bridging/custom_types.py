"""Custom types for the protocol."""

from enum import Enum
from typing import Any

from pydantic import BaseModel


class BridgeResult(Enum):
    """This class represents an instance of BridgeResult."""

    FAILED = 0
    COMPLETED = 1
    PENDING_TX_RECEIPT = 2
    AWAITING_TARGET_FINALITY = 3
    CLAIMABLE = 4

    @staticmethod
    def encode(bridge_result_protobuf_object, bridge_result_object: "BridgeResult") -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the bridge_result_protobuf_object argument is matched with the instance of this
        class in the 'bridge_result_object' argument.



        Args:
        ----
               bridge_result_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               bridge_result_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        bridge_result_protobuf_object.bridge_result = bridge_result_object.value

    @classmethod
    def decode(cls, bridge_result_protobuf_object) -> "BridgeResult":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'bridge_result_protobuf_object' argument.

        'bridge_result_protobuf_object' argument.


        Args:
        ----
               bridge_result_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        return BridgeResult(bridge_result_protobuf_object.bridge_result)


class ErrorInfo(Enum):
    """This class represents an instance of ErrorInfo."""

    INVALID_PERFORMATIVE = 0
    CONNECTION_ERROR = 1
    INVALID_ROUTE = 2
    INVALID_PARAMETERS = 3
    ALREADY_FINALIZED = 4
    OTHER_EXCEPTION = 5

    @staticmethod
    def encode(error_info_protobuf_object, error_info_object: "ErrorInfo") -> None:
        """Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the error_info_protobuf_object argument is matched with the instance of this class
        in the 'error_info_object' argument.



        Args:
        ----
               error_info_protobuf_object:  the protocol buffer object whose type corresponds with this class.
               error_info_object:  an instance of this class to be encoded in the protocol buffer object.

        """
        error_info_protobuf_object.error_info = error_info_object.value

    @classmethod
    def decode(cls, error_info_protobuf_object) -> "ErrorInfo":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'error_info_protobuf_object' argument.

        'error_info_protobuf_object' argument.


        Args:
        ----
               error_info_protobuf_object:  the protocol buffer object whose type corresponds with this class.

        """
        return ErrorInfo(error_info_protobuf_object.error_info)


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


class BridgeRequest(BaseCustomEncoder):
    """This class represents an instance of BridgeRequest."""

    source_chain: str
    target_chain: str
    source_token: str
    target_token: str | None = None
    amount: float
    bridge: str
    receiver: str | None = None


CUSTOM_ENUM_MAP = {
    "<class 'asset_bridging_pb2.BridgeResult'>": BridgeResult,
    "<class 'asset_bridging_pb2.ErrorInfo'>": ErrorInfo,
}
