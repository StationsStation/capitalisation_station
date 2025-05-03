"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel
from packages.zarathustra.protocols.asset_bridging.primitives import (
    Int64,
)


# ruff: noqa: N806, C901, PLR0912, PLR0914, PLR0915, A001
# N806     - variable should be lowercase
# C901     - function is too complex
# PLR0912  - too many branches
# PLR0914  - too many local variables
# PLR0915  - too many statements
# A001     - shadowing builtin names like `id` and `type`

MAX_PROTO_SIZE = 2 * 1024 * 1024 * 1024  # 2 GiB in bytes


class BridgeRequest(BaseModel):
    """BridgeRequest."""

    source_chain: str
    target_chain: str
    source_token: str
    target_token: str | None
    amount: Int64
    bridge: str
    receiver: str | None

    @staticmethod
    def encode(proto_obj, bridgerequest: BridgeRequest) -> None:
        """Encode BridgeRequest to protobuf."""

        proto_obj.source_chain = bridgerequest.source_chain
        proto_obj.target_chain = bridgerequest.target_chain
        proto_obj.source_token = bridgerequest.source_token
        if bridgerequest.target_token is not None:
            proto_obj.target_token = bridgerequest.target_token
        proto_obj.amount = bridgerequest.amount
        proto_obj.bridge = bridgerequest.bridge
        if bridgerequest.receiver is not None:
            proto_obj.receiver = bridgerequest.receiver

    @classmethod
    def decode(cls, proto_obj) -> BridgeRequest:
        """Decode proto_obj to BridgeRequest."""

        source_chain = proto_obj.source_chain
        target_chain = proto_obj.target_chain
        source_token = proto_obj.source_token
        target_token = (
            proto_obj.target_token
            if proto_obj.target_token is not None and proto_obj.HasField("target_token")
            else None
        )
        amount = proto_obj.amount
        bridge = proto_obj.bridge
        receiver = proto_obj.receiver if proto_obj.receiver is not None and proto_obj.HasField("receiver") else None

        return cls(
            source_chain=source_chain,
            target_chain=target_chain,
            source_token=source_token,
            target_token=target_token,
            amount=amount,
            bridge=bridge,
            receiver=receiver,
        )


class BridgeResult(BaseModel):
    """BridgeResult."""

    class BridgeStatus(IntEnum):
        """BridgeStatus."""

        BRIDGE_STATUS_FAILED = 0
        BRIDGE_STATUS_COMPLETED = 1
        BRIDGE_STATUS_PENDING_TX_RECEIPT = 2
        BRIDGE_STATUS_AWAITING_TARGET_FINALITY = 3
        BRIDGE_STATUS_CLAIMABLE = 4

    tx_hash: str
    status: BridgeResult.BridgeStatus
    request: BridgeRequest

    @staticmethod
    def encode(proto_obj, bridgeresult: BridgeResult) -> None:
        """Encode BridgeResult to protobuf."""

        proto_obj.tx_hash = bridgeresult.tx_hash
        proto_obj.status = bridgeresult.status
        BridgeRequest.encode(proto_obj.request, bridgeresult.request)

    @classmethod
    def decode(cls, proto_obj) -> BridgeResult:
        """Decode proto_obj to BridgeResult."""

        tx_hash = proto_obj.tx_hash
        status = proto_obj.status
        request = BridgeRequest.decode(proto_obj.request)

        return cls(tx_hash=tx_hash, status=status, request=request)


class ErrorCode(BaseModel):
    """ErrorCode."""

    class ErrorCodeEnum(IntEnum):
        """ErrorCodeEnum."""

        ERROR_CODE_ENUM_UNKNOWN_ROUTE = 0
        ERROR_CODE_ENUM_OTHER_EXCEPTION = 1

    error_code: ErrorCode.ErrorCodeEnum

    @staticmethod
    def encode(proto_obj, errorcode: ErrorCode) -> None:
        """Encode ErrorCode to protobuf."""

        proto_obj.error_code = errorcode.error_code

    @classmethod
    def decode(cls, proto_obj) -> ErrorCode:
        """Decode proto_obj to ErrorCode."""

        error_code = proto_obj.error_code

        return cls(error_code=error_code)


for cls in BaseModel.__subclasses__():
    cls.model_rebuild()
