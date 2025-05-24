"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from packages.zarathustra.protocols.asset_bridging.primitives import (
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


class BridgeRequest(BaseModel):
    """BridgeRequest."""

    source_ledger_id: str
    target_ledger_id: str
    source_token: str
    target_token: Optional[str] = None
    amount: Float
    bridge: str
    receiver: Optional[str] = None

    @staticmethod
    def encode(proto_obj, bridgerequest: BridgeRequest) -> None:
        """Encode BridgeRequest to protobuf."""
        proto_obj.source_ledger_id = bridgerequest.source_ledger_id
        proto_obj.target_ledger_id = bridgerequest.target_ledger_id
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
        source_ledger_id = proto_obj.source_ledger_id
        target_ledger_id = proto_obj.target_ledger_id
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
            source_ledger_id=source_ledger_id,
            target_ledger_id=target_ledger_id,
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


class ErrorInfo(BaseModel):
    """ErrorInfo."""

    class Code(IntEnum):
        """Code."""

        CODE_INVALID_PERFORMATIVE = 0
        CODE_CONNECTION_ERROR = 1
        CODE_INVALID_ROUTE = 2
        CODE_INVALID_PARAMETERS = 3
        CODE_ALREADY_FINALIZED = 4
        CODE_OTHER_EXCEPTION = 5

    code: ErrorInfo.Code
    message: str

    @staticmethod
    def encode(proto_obj, errorinfo: ErrorInfo) -> None:
        """Encode ErrorInfo to protobuf."""
        proto_obj.code = errorinfo.code
        proto_obj.message = errorinfo.message

    @classmethod
    def decode(cls, proto_obj) -> ErrorInfo:
        """Decode proto_obj to ErrorInfo."""
        code = proto_obj.code
        message = proto_obj.message
        return cls(code=code, message=message)


for cls in BaseModel.__subclasses__():
    if cls.__module__ == __name__:
        cls.model_rebuild()
