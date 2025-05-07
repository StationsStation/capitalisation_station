"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from packages.eightballer.protocols.positions.primitives import (
    Float,
    Int64,
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

    UNKNOWN_EXCHANGE = 0
    UNKNOWN_POSITION = 1
    API_ERROR = 2

    @staticmethod
    def encode(pb_obj, error_code: ErrorCode) -> None:
        """Encode ErrorCode to protobuf."""
        pb_obj.error_code = error_code

    @classmethod
    def decode(cls, pb_obj) -> ErrorCode:
        """Decode protobuf to ErrorCode."""
        return cls(pb_obj.error_code)


class Position(BaseModel):
    """Position."""

    id: str
    symbol: str
    timestamp: Optional[Int64] = None
    datetime: Optional[str] = None
    last_update_timestamp: Optional[Int64] = None
    initial_margin: Optional[Float] = None
    initial_margin_percentage: Optional[Float] = None
    maintenance_margin: Optional[Float] = None
    maintenance_margin_percentage: Optional[Float] = None
    entry_price: Optional[Float] = None
    notional: Optional[Float] = None
    leverage: Optional[Float] = None
    unrealized_pnl: Optional[Float] = None
    contracts: Optional[Float] = None
    contract_size: Optional[Float] = None
    margin_ratio: Optional[Float] = None
    liquidation_price: Optional[Float] = None
    mark_price: Optional[Float] = None
    last_price: Optional[Float] = None
    collateral: Optional[Float] = None
    margin_mode: Optional[str] = None
    side: Optional[PositionSide] = None
    percentage: Optional[Float] = None
    info: Optional[str] = None
    size: Optional[Float] = None
    exchange_id: Optional[str] = None
    hedged: Optional[str] = None
    stop_loss_price: Optional[Float] = None
    take_profit_price: Optional[Float] = None

    @staticmethod
    def encode(proto_obj, position: Position) -> None:
        """Encode Position to protobuf."""
        proto_obj.id = position.id
        proto_obj.symbol = position.symbol
        if position.timestamp is not None:
            proto_obj.timestamp = position.timestamp
        if position.datetime is not None:
            proto_obj.datetime = position.datetime
        if position.last_update_timestamp is not None:
            proto_obj.last_update_timestamp = position.last_update_timestamp
        if position.initial_margin is not None:
            proto_obj.initial_margin = position.initial_margin
        if position.initial_margin_percentage is not None:
            proto_obj.initial_margin_percentage = position.initial_margin_percentage
        if position.maintenance_margin is not None:
            proto_obj.maintenance_margin = position.maintenance_margin
        if position.maintenance_margin_percentage is not None:
            proto_obj.maintenance_margin_percentage = position.maintenance_margin_percentage
        if position.entry_price is not None:
            proto_obj.entry_price = position.entry_price
        if position.notional is not None:
            proto_obj.notional = position.notional
        if position.leverage is not None:
            proto_obj.leverage = position.leverage
        if position.unrealized_pnl is not None:
            proto_obj.unrealized_pnl = position.unrealized_pnl
        if position.contracts is not None:
            proto_obj.contracts = position.contracts
        if position.contract_size is not None:
            proto_obj.contract_size = position.contract_size
        if position.margin_ratio is not None:
            proto_obj.margin_ratio = position.margin_ratio
        if position.liquidation_price is not None:
            proto_obj.liquidation_price = position.liquidation_price
        if position.mark_price is not None:
            proto_obj.mark_price = position.mark_price
        if position.last_price is not None:
            proto_obj.last_price = position.last_price
        if position.collateral is not None:
            proto_obj.collateral = position.collateral
        if position.margin_mode is not None:
            proto_obj.margin_mode = position.margin_mode
        if position.side is not None:
            temp = proto_obj.side.__class__()
            PositionSide.encode(temp, position.side)
            proto_obj.side.CopyFrom(temp)
        if position.percentage is not None:
            proto_obj.percentage = position.percentage
        if position.info is not None:
            proto_obj.info = position.info
        if position.size is not None:
            proto_obj.size = position.size
        if position.exchange_id is not None:
            proto_obj.exchange_id = position.exchange_id
        if position.hedged is not None:
            proto_obj.hedged = position.hedged
        if position.stop_loss_price is not None:
            proto_obj.stop_loss_price = position.stop_loss_price
        if position.take_profit_price is not None:
            proto_obj.take_profit_price = position.take_profit_price

    @classmethod
    def decode(cls, proto_obj) -> Position:
        """Decode proto_obj to Position."""
        id = proto_obj.id
        symbol = proto_obj.symbol
        timestamp = proto_obj.timestamp if proto_obj.timestamp is not None and proto_obj.HasField("timestamp") else None
        datetime = proto_obj.datetime if proto_obj.datetime is not None and proto_obj.HasField("datetime") else None
        last_update_timestamp = (
            proto_obj.last_update_timestamp
            if proto_obj.last_update_timestamp is not None and proto_obj.HasField("last_update_timestamp")
            else None
        )
        initial_margin = (
            proto_obj.initial_margin
            if proto_obj.initial_margin is not None and proto_obj.HasField("initial_margin")
            else None
        )
        initial_margin_percentage = (
            proto_obj.initial_margin_percentage
            if proto_obj.initial_margin_percentage is not None and proto_obj.HasField("initial_margin_percentage")
            else None
        )
        maintenance_margin = (
            proto_obj.maintenance_margin
            if proto_obj.maintenance_margin is not None and proto_obj.HasField("maintenance_margin")
            else None
        )
        maintenance_margin_percentage = (
            proto_obj.maintenance_margin_percentage
            if proto_obj.maintenance_margin_percentage is not None
            and proto_obj.HasField("maintenance_margin_percentage")
            else None
        )
        entry_price = (
            proto_obj.entry_price if proto_obj.entry_price is not None and proto_obj.HasField("entry_price") else None
        )
        notional = proto_obj.notional if proto_obj.notional is not None and proto_obj.HasField("notional") else None
        leverage = proto_obj.leverage if proto_obj.leverage is not None and proto_obj.HasField("leverage") else None
        unrealized_pnl = (
            proto_obj.unrealized_pnl
            if proto_obj.unrealized_pnl is not None and proto_obj.HasField("unrealized_pnl")
            else None
        )
        contracts = proto_obj.contracts if proto_obj.contracts is not None and proto_obj.HasField("contracts") else None
        contract_size = (
            proto_obj.contract_size
            if proto_obj.contract_size is not None and proto_obj.HasField("contract_size")
            else None
        )
        margin_ratio = (
            proto_obj.margin_ratio
            if proto_obj.margin_ratio is not None and proto_obj.HasField("margin_ratio")
            else None
        )
        liquidation_price = (
            proto_obj.liquidation_price
            if proto_obj.liquidation_price is not None and proto_obj.HasField("liquidation_price")
            else None
        )
        mark_price = (
            proto_obj.mark_price if proto_obj.mark_price is not None and proto_obj.HasField("mark_price") else None
        )
        last_price = (
            proto_obj.last_price if proto_obj.last_price is not None and proto_obj.HasField("last_price") else None
        )
        collateral = (
            proto_obj.collateral if proto_obj.collateral is not None and proto_obj.HasField("collateral") else None
        )
        margin_mode = (
            proto_obj.margin_mode if proto_obj.margin_mode is not None and proto_obj.HasField("margin_mode") else None
        )
        side = (
            PositionSide.decode(proto_obj.side) if proto_obj.side is not None and proto_obj.HasField("side") else None
        )
        percentage = (
            proto_obj.percentage if proto_obj.percentage is not None and proto_obj.HasField("percentage") else None
        )
        info = proto_obj.info if proto_obj.info is not None and proto_obj.HasField("info") else None
        size = proto_obj.size if proto_obj.size is not None and proto_obj.HasField("size") else None
        exchange_id = (
            proto_obj.exchange_id if proto_obj.exchange_id is not None and proto_obj.HasField("exchange_id") else None
        )
        hedged = proto_obj.hedged if proto_obj.hedged is not None and proto_obj.HasField("hedged") else None
        stop_loss_price = (
            proto_obj.stop_loss_price
            if proto_obj.stop_loss_price is not None and proto_obj.HasField("stop_loss_price")
            else None
        )
        take_profit_price = (
            proto_obj.take_profit_price
            if proto_obj.take_profit_price is not None and proto_obj.HasField("take_profit_price")
            else None
        )
        return cls(
            id=id,
            symbol=symbol,
            timestamp=timestamp,
            datetime=datetime,
            last_update_timestamp=last_update_timestamp,
            initial_margin=initial_margin,
            initial_margin_percentage=initial_margin_percentage,
            maintenance_margin=maintenance_margin,
            maintenance_margin_percentage=maintenance_margin_percentage,
            entry_price=entry_price,
            notional=notional,
            leverage=leverage,
            unrealized_pnl=unrealized_pnl,
            contracts=contracts,
            contract_size=contract_size,
            margin_ratio=margin_ratio,
            liquidation_price=liquidation_price,
            mark_price=mark_price,
            last_price=last_price,
            collateral=collateral,
            margin_mode=margin_mode,
            side=side,
            percentage=percentage,
            info=info,
            size=size,
            exchange_id=exchange_id,
            hedged=hedged,
            stop_loss_price=stop_loss_price,
            take_profit_price=take_profit_price,
        )


class PositionSide(IntEnum):
    """PositionSide."""

    LONG = 0
    SHORT = 1

    @staticmethod
    def encode(pb_obj, position_side: PositionSide) -> None:
        """Encode PositionSide to protobuf."""
        pb_obj.position_side = position_side

    @classmethod
    def decode(cls, pb_obj) -> PositionSide:
        """Decode protobuf to PositionSide."""
        return cls(pb_obj.position_side)


class Positions(BaseModel):
    """Positions."""

    positions: list[Position]

    @staticmethod
    def encode(proto_obj, positions: Positions) -> None:
        """Encode Positions to protobuf."""
        for item in positions.positions:
            Position.encode(proto_obj.positions.add(), item)

    @classmethod
    def decode(cls, proto_obj) -> Positions:
        """Decode proto_obj to Positions."""
        positions = [Position.decode(item) for item in proto_obj.positions]
        return cls(positions=positions)


for cls in BaseModel.__subclasses__():
    if cls.__module__ == __name__:
        cls.model_rebuild()
