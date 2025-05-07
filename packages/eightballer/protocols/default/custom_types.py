"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel


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

    UNSUPPORTED_PROTOCOL = 0
    DECODING_ERROR = 1
    INVALID_MESSAGE = 2
    UNSUPPORTED_SKILL = 3
    INVALID_DIALOGUE = 4

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
