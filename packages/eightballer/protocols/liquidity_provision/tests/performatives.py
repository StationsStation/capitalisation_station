# Auto-generated by tool

"""Models for the liquidity_provision protocol performatives to facilitate hypothesis strategy generation."""

from typing import Optional

from pydantic import BaseModel, conint

from packages.eightballer.protocols.liquidity_provision.custom_types import (
    ErrorCode,
)
from packages.eightballer.protocols.liquidity_provision.tests.primitive_strategies import (
    Int32,
)


# ruff: noqa: UP007
# UP007    - Use X | Y for type annotations  # NOTE: important edge case pydantic-hypothesis interaction!


class AddLiquidity(BaseModel):
    """Model for the `ADD_LIQUIDITY` initial speech act performative."""

    pool_id: str
    token_ids: tuple[str]
    amounts: tuple[conint(ge=Int32.min(), le=Int32.max())]
    min_mint_amount: conint(ge=Int32.min(), le=Int32.max())
    deadline: conint(ge=Int32.min(), le=Int32.max())
    user_data: Optional[bytes]
    exchange_id: str
    ledger_id: Optional[str]


class RemoveLiquidity(BaseModel):
    """Model for the `REMOVE_LIQUIDITY` initial speech act performative."""

    pool_id: str
    token_ids: tuple[str]
    burn_amount: conint(ge=Int32.min(), le=Int32.max())
    min_amounts: tuple[conint(ge=Int32.min(), le=Int32.max())]
    deadline: conint(ge=Int32.min(), le=Int32.max())
    user_data: Optional[bytes]
    exchange_id: str
    ledger_id: Optional[str]


class QueryLiquidity(BaseModel):
    """Model for the `QUERY_LIQUIDITY` initial speech act performative."""

    pool_id: str
    exchange_id: str
    ledger_id: Optional[str]


class LiquidityAdded(BaseModel):
    """Model for the `LIQUIDITY_ADDED` initial speech act performative."""

    pool_id: str
    minted_tokens: conint(ge=Int32.min(), le=Int32.max())


class LiquidityRemoved(BaseModel):
    """Model for the `LIQUIDITY_REMOVED` initial speech act performative."""

    pool_id: str
    received_amounts: tuple[conint(ge=Int32.min(), le=Int32.max())]


class LiquidityStatus(BaseModel):
    """Model for the `LIQUIDITY_STATUS` initial speech act performative."""

    pool_id: str
    current_liquidity: conint(ge=Int32.min(), le=Int32.max())
    available_tokens: tuple[conint(ge=Int32.min(), le=Int32.max())]


class Error(BaseModel):
    """Model for the `ERROR` initial speech act performative."""

    error_code: ErrorCode
    description: str


AddLiquidity.model_rebuild()
RemoveLiquidity.model_rebuild()
QueryLiquidity.model_rebuild()
LiquidityAdded.model_rebuild()
LiquidityRemoved.model_rebuild()
LiquidityStatus.model_rebuild()
Error.model_rebuild()
