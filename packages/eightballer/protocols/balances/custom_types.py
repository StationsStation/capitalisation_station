"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from packages.eightballer.protocols.balances.primitives import (
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


class Balance(BaseModel):
    """Balance."""

    asset_id: str
    free: Float
    used: Float
    total: Float
    is_native: bool
    contract_address: Optional[str] = None

    @staticmethod
    def encode(proto_obj, balance: Balance) -> None:
        """Encode Balance to protobuf."""
        proto_obj.asset_id = balance.asset_id
        proto_obj.free = balance.free
        proto_obj.used = balance.used
        proto_obj.total = balance.total
        proto_obj.is_native = balance.is_native
        if balance.contract_address is not None:
            proto_obj.contract_address = balance.contract_address

    @classmethod
    def decode(cls, proto_obj) -> Balance:
        """Decode proto_obj to Balance."""
        asset_id = proto_obj.asset_id
        free = proto_obj.free
        used = proto_obj.used
        total = proto_obj.total
        is_native = proto_obj.is_native
        contract_address = (
            proto_obj.contract_address
            if proto_obj.contract_address is not None and proto_obj.HasField("contract_address")
            else None
        )
        return cls(
            asset_id=asset_id, free=free, used=used, total=total, is_native=is_native, contract_address=contract_address
        )


class Balances(BaseModel):
    """Balances."""

    balances: list[Balance]

    @staticmethod
    def encode(proto_obj, balances: Balances) -> None:
        """Encode Balances to protobuf."""
        for item in balances.balances:
            Balance.encode(proto_obj.balances.add(), item)

    @classmethod
    def decode(cls, proto_obj) -> Balances:
        """Decode proto_obj to Balances."""
        balances = [Balance.decode(item) for item in proto_obj.balances]
        return cls(balances=balances)


class ErrorCode(IntEnum):
    """ErrorCode."""

    UNKNOWN_EXCHANGE = 0
    UNKNOWN_ASSET = 1
    API_ERROR = 2

    @staticmethod
    def encode(pb_obj, error_code: ErrorCode) -> None:
        """Encode ErrorCode to protobuf."""
        pb_obj.error_code = error_code

    @classmethod
    def decode(cls, pb_obj) -> ErrorCode:
        """Decode protobuf to ErrorCode."""
        return cls(pb_obj.error_code)


for cls in BaseModel.__subclasses__():
    if cls.__module__ == __name__:
        cls.model_rebuild()
