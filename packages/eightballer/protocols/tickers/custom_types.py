"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from packages.eightballer.protocols.tickers.primitives import (
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
    UNKNOWN_TICKER = 1
    API_ERROR = 2

    @staticmethod
    def encode(pb_obj, error_code: ErrorCode) -> None:
        """Encode ErrorCode to protobuf."""
        pb_obj.error_code = error_code

    @classmethod
    def decode(cls, pb_obj) -> ErrorCode:
        """Decode protobuf to ErrorCode."""
        return cls(pb_obj.error_code)


class Ticker(BaseModel):
    """Ticker."""

    symbol: str
    timestamp: Int64
    datetime: str
    ask: Optional[Float] = None
    bid: Optional[Float] = None
    asset_a: Optional[str] = None
    asset_b: Optional[str] = None
    bid_volume: Optional[Float] = None
    ask_volume: Optional[Float] = None
    high: Optional[Float] = None
    low: Optional[Float] = None
    vwap: Optional[Float] = None
    open: Optional[Float] = None
    close: Optional[Float] = None
    last: Optional[Float] = None
    previous_close: Optional[Float] = None
    change: Optional[Float] = None
    percentage: Optional[Float] = None
    average: Optional[Float] = None
    base_volume: Optional[Float] = None
    quote_volume: Optional[Float] = None
    info: Optional[str] = None

    @staticmethod
    def encode(proto_obj, ticker: Ticker) -> None:
        """Encode Ticker to protobuf."""
        proto_obj.symbol = ticker.symbol
        proto_obj.timestamp = ticker.timestamp
        proto_obj.datetime = ticker.datetime
        if ticker.ask is not None:
            proto_obj.ask = ticker.ask
        if ticker.bid is not None:
            proto_obj.bid = ticker.bid
        if ticker.asset_a is not None:
            proto_obj.asset_a = ticker.asset_a
        if ticker.asset_b is not None:
            proto_obj.asset_b = ticker.asset_b
        if ticker.bid_volume is not None:
            proto_obj.bid_volume = ticker.bid_volume
        if ticker.ask_volume is not None:
            proto_obj.ask_volume = ticker.ask_volume
        if ticker.high is not None:
            proto_obj.high = ticker.high
        if ticker.low is not None:
            proto_obj.low = ticker.low
        if ticker.vwap is not None:
            proto_obj.vwap = ticker.vwap
        if ticker.open is not None:
            proto_obj.open = ticker.open
        if ticker.close is not None:
            proto_obj.close = ticker.close
        if ticker.last is not None:
            proto_obj.last = ticker.last
        if ticker.previous_close is not None:
            proto_obj.previous_close = ticker.previous_close
        if ticker.change is not None:
            proto_obj.change = ticker.change
        if ticker.percentage is not None:
            proto_obj.percentage = ticker.percentage
        if ticker.average is not None:
            proto_obj.average = ticker.average
        if ticker.base_volume is not None:
            proto_obj.base_volume = ticker.base_volume
        if ticker.quote_volume is not None:
            proto_obj.quote_volume = ticker.quote_volume
        if ticker.info is not None:
            proto_obj.info = ticker.info

    @classmethod
    def decode(cls, proto_obj) -> Ticker:
        """Decode proto_obj to Ticker."""
        symbol = proto_obj.symbol
        timestamp = proto_obj.timestamp
        datetime = proto_obj.datetime
        ask = proto_obj.ask if proto_obj.ask is not None and proto_obj.HasField("ask") else None
        bid = proto_obj.bid if proto_obj.bid is not None and proto_obj.HasField("bid") else None
        asset_a = proto_obj.asset_a if proto_obj.asset_a is not None and proto_obj.HasField("asset_a") else None
        asset_b = proto_obj.asset_b if proto_obj.asset_b is not None and proto_obj.HasField("asset_b") else None
        bid_volume = (
            proto_obj.bid_volume if proto_obj.bid_volume is not None and proto_obj.HasField("bid_volume") else None
        )
        ask_volume = (
            proto_obj.ask_volume if proto_obj.ask_volume is not None and proto_obj.HasField("ask_volume") else None
        )
        high = proto_obj.high if proto_obj.high is not None and proto_obj.HasField("high") else None
        low = proto_obj.low if proto_obj.low is not None and proto_obj.HasField("low") else None
        vwap = proto_obj.vwap if proto_obj.vwap is not None and proto_obj.HasField("vwap") else None
        open = proto_obj.open if proto_obj.open is not None and proto_obj.HasField("open") else None
        close = proto_obj.close if proto_obj.close is not None and proto_obj.HasField("close") else None
        last = proto_obj.last if proto_obj.last is not None and proto_obj.HasField("last") else None
        previous_close = (
            proto_obj.previous_close
            if proto_obj.previous_close is not None and proto_obj.HasField("previous_close")
            else None
        )
        change = proto_obj.change if proto_obj.change is not None and proto_obj.HasField("change") else None
        percentage = (
            proto_obj.percentage if proto_obj.percentage is not None and proto_obj.HasField("percentage") else None
        )
        average = proto_obj.average if proto_obj.average is not None and proto_obj.HasField("average") else None
        base_volume = (
            proto_obj.base_volume if proto_obj.base_volume is not None and proto_obj.HasField("base_volume") else None
        )
        quote_volume = (
            proto_obj.quote_volume
            if proto_obj.quote_volume is not None and proto_obj.HasField("quote_volume")
            else None
        )
        info = proto_obj.info if proto_obj.info is not None and proto_obj.HasField("info") else None
        return cls(
            symbol=symbol,
            timestamp=timestamp,
            datetime=datetime,
            ask=ask,
            bid=bid,
            asset_a=asset_a,
            asset_b=asset_b,
            bid_volume=bid_volume,
            ask_volume=ask_volume,
            high=high,
            low=low,
            vwap=vwap,
            open=open,
            close=close,
            last=last,
            previous_close=previous_close,
            change=change,
            percentage=percentage,
            average=average,
            base_volume=base_volume,
            quote_volume=quote_volume,
            info=info,
        )


class Tickers(BaseModel):
    """Tickers."""

    tickers: list[Ticker]

    @staticmethod
    def encode(proto_obj, tickers: Tickers) -> None:
        """Encode Tickers to protobuf."""
        for item in tickers.tickers:
            Ticker.encode(proto_obj.tickers.add(), item)

    @classmethod
    def decode(cls, proto_obj) -> Tickers:
        """Decode proto_obj to Tickers."""
        tickers = [Ticker.decode(item) for item in proto_obj.tickers]
        return cls(tickers=tickers)


for cls in BaseModel.__subclasses__():
    if cls.__module__ == __name__:
        cls.model_rebuild()
