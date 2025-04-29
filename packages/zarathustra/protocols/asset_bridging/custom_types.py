"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel


# ruff: noqa: N806, C901, PLR0912, PLR0914, PLR0915, A001
# N806     - variable should be lowercase
# C901     - function is too complex
# PLR0912  - too many branches
# PLR0914  - too many local variables
# PLR0915  - too many statements
# A001     - shadowing builtin names like `id` and `type`

MAX_PROTO_SIZE = 2 * 1024 * 1024 * 1024  # 2 GiB in bytes


class BridgeStatus(BaseModel):
    """BridgeStatus."""

    class BridgeStatusEnum(IntEnum):
        """BridgeStatusEnum."""

        BRIDGE_STATUS_ENUM_IN_PROGRESS = 0
        BRIDGE_STATUS_ENUM_PENDING_CLAIM = 1
        BRIDGE_STATUS_ENUM_COMPLETED = 2
        BRIDGE_STATUS_ENUM_FAILED = 3

    status: BridgeStatus.BridgeStatusEnum

    @staticmethod
    def encode(proto_obj, bridgestatus: BridgeStatus) -> None:
        """Encode BridgeStatus to protobuf."""

        proto_obj.status = bridgestatus.status

    @classmethod
    def decode(cls, proto_obj) -> BridgeStatus:
        """Decode proto_obj to BridgeStatus."""

        status = proto_obj.status

        return cls(status=status)


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
