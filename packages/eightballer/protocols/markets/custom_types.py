"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from packages.eightballer.protocols.markets.primitives import (
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


class Market(BaseModel):
    """Market."""

    id: str
    lowercase_id: Optional[str] = None
    exchange_id: Optional[str] = None
    symbol: Optional[str] = None
    base: Optional[str] = None
    quote: Optional[str] = None
    settle: Optional[str] = None
    base_id: Optional[str] = None
    quote_id: Optional[str] = None
    settle_id: Optional[str] = None
    type: Optional[str] = None
    spot: Optional[bool] = None
    margin: Optional[bool] = None
    swap: Optional[bool] = None
    future: Optional[bool] = None
    option: Optional[bool] = None
    active: Optional[bool] = None
    contract: Optional[bool] = None
    linear: Optional[bool] = None
    inverse: Optional[bool] = None
    taker: Optional[Float] = None
    maker: Optional[Float] = None
    contract_size: Optional[Float] = None
    expiry: Optional[Float] = None
    expiry_datetime: Optional[str] = None
    strike: Optional[Float] = None
    option_type: Optional[str] = None
    precision: Optional[Float] = None
    limits: Optional[str] = None
    info: Optional[str] = None

    @staticmethod
    def encode(proto_obj, market: Market) -> None:
        """Encode Market to protobuf."""
        proto_obj.id = market.id
        if market.lowercase_id is not None:
            proto_obj.lowercase_id = market.lowercase_id
        if market.exchange_id is not None:
            proto_obj.exchange_id = market.exchange_id
        if market.symbol is not None:
            proto_obj.symbol = market.symbol
        if market.base is not None:
            proto_obj.base = market.base
        if market.quote is not None:
            proto_obj.quote = market.quote
        if market.settle is not None:
            proto_obj.settle = market.settle
        if market.base_id is not None:
            proto_obj.base_id = market.base_id
        if market.quote_id is not None:
            proto_obj.quote_id = market.quote_id
        if market.settle_id is not None:
            proto_obj.settle_id = market.settle_id
        if market.type is not None:
            proto_obj.type = market.type
        if market.spot is not None:
            proto_obj.spot = market.spot
        if market.margin is not None:
            proto_obj.margin = market.margin
        if market.swap is not None:
            proto_obj.swap = market.swap
        if market.future is not None:
            proto_obj.future = market.future
        if market.option is not None:
            proto_obj.option = market.option
        if market.active is not None:
            proto_obj.active = market.active
        if market.contract is not None:
            proto_obj.contract = market.contract
        if market.linear is not None:
            proto_obj.linear = market.linear
        if market.inverse is not None:
            proto_obj.inverse = market.inverse
        if market.taker is not None:
            proto_obj.taker = market.taker
        if market.maker is not None:
            proto_obj.maker = market.maker
        if market.contract_size is not None:
            proto_obj.contract_size = market.contract_size
        if market.expiry is not None:
            proto_obj.expiry = market.expiry
        if market.expiry_datetime is not None:
            proto_obj.expiry_datetime = market.expiry_datetime
        if market.strike is not None:
            proto_obj.strike = market.strike
        if market.option_type is not None:
            proto_obj.option_type = market.option_type
        if market.precision is not None:
            proto_obj.precision = market.precision
        if market.limits is not None:
            proto_obj.limits = market.limits
        if market.info is not None:
            proto_obj.info = market.info

    @classmethod
    def decode(cls, proto_obj) -> Market:
        """Decode proto_obj to Market."""
        id = proto_obj.id
        lowercase_id = (
            proto_obj.lowercase_id
            if proto_obj.lowercase_id is not None and proto_obj.HasField("lowercase_id")
            else None
        )
        exchange_id = (
            proto_obj.exchange_id if proto_obj.exchange_id is not None and proto_obj.HasField("exchange_id") else None
        )
        symbol = proto_obj.symbol if proto_obj.symbol is not None and proto_obj.HasField("symbol") else None
        base = proto_obj.base if proto_obj.base is not None and proto_obj.HasField("base") else None
        quote = proto_obj.quote if proto_obj.quote is not None and proto_obj.HasField("quote") else None
        settle = proto_obj.settle if proto_obj.settle is not None and proto_obj.HasField("settle") else None
        base_id = proto_obj.base_id if proto_obj.base_id is not None and proto_obj.HasField("base_id") else None
        quote_id = proto_obj.quote_id if proto_obj.quote_id is not None and proto_obj.HasField("quote_id") else None
        settle_id = proto_obj.settle_id if proto_obj.settle_id is not None and proto_obj.HasField("settle_id") else None
        type = proto_obj.type if proto_obj.type is not None and proto_obj.HasField("type") else None
        spot = proto_obj.spot if proto_obj.spot is not None and proto_obj.HasField("spot") else None
        margin = proto_obj.margin if proto_obj.margin is not None and proto_obj.HasField("margin") else None
        swap = proto_obj.swap if proto_obj.swap is not None and proto_obj.HasField("swap") else None
        future = proto_obj.future if proto_obj.future is not None and proto_obj.HasField("future") else None
        option = proto_obj.option if proto_obj.option is not None and proto_obj.HasField("option") else None
        active = proto_obj.active if proto_obj.active is not None and proto_obj.HasField("active") else None
        contract = proto_obj.contract if proto_obj.contract is not None and proto_obj.HasField("contract") else None
        linear = proto_obj.linear if proto_obj.linear is not None and proto_obj.HasField("linear") else None
        inverse = proto_obj.inverse if proto_obj.inverse is not None and proto_obj.HasField("inverse") else None
        taker = proto_obj.taker if proto_obj.taker is not None and proto_obj.HasField("taker") else None
        maker = proto_obj.maker if proto_obj.maker is not None and proto_obj.HasField("maker") else None
        contract_size = (
            proto_obj.contract_size
            if proto_obj.contract_size is not None and proto_obj.HasField("contract_size")
            else None
        )
        expiry = proto_obj.expiry if proto_obj.expiry is not None and proto_obj.HasField("expiry") else None
        expiry_datetime = (
            proto_obj.expiry_datetime
            if proto_obj.expiry_datetime is not None and proto_obj.HasField("expiry_datetime")
            else None
        )
        strike = proto_obj.strike if proto_obj.strike is not None and proto_obj.HasField("strike") else None
        option_type = (
            proto_obj.option_type if proto_obj.option_type is not None and proto_obj.HasField("option_type") else None
        )
        precision = proto_obj.precision if proto_obj.precision is not None and proto_obj.HasField("precision") else None
        limits = proto_obj.limits if proto_obj.limits is not None and proto_obj.HasField("limits") else None
        info = proto_obj.info if proto_obj.info is not None and proto_obj.HasField("info") else None
        return cls(
            id=id,
            lowercase_id=lowercase_id,
            exchange_id=exchange_id,
            symbol=symbol,
            base=base,
            quote=quote,
            settle=settle,
            base_id=base_id,
            quote_id=quote_id,
            settle_id=settle_id,
            type=type,
            spot=spot,
            margin=margin,
            swap=swap,
            future=future,
            option=option,
            active=active,
            contract=contract,
            linear=linear,
            inverse=inverse,
            taker=taker,
            maker=maker,
            contract_size=contract_size,
            expiry=expiry,
            expiry_datetime=expiry_datetime,
            strike=strike,
            option_type=option_type,
            precision=precision,
            limits=limits,
            info=info,
        )


class Markets(BaseModel):
    """Markets."""

    markets: list[Market]

    @staticmethod
    def encode(proto_obj, markets: Markets) -> None:
        """Encode Markets to protobuf."""
        for item in markets.markets:
            Market.encode(proto_obj.markets.add(), item)

    @classmethod
    def decode(cls, proto_obj) -> Markets:
        """Decode proto_obj to Markets."""
        markets = [Market.decode(item) for item in proto_obj.markets]
        return cls(markets=markets)


for cls in BaseModel.__subclasses__():
    if cls.__module__ == __name__:
        cls.model_rebuild()
