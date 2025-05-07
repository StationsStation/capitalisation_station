"""Module containing the pydantic models generated from the .proto file."""

from __future__ import annotations

from pydantic import BaseModel

from packages.eightballer.protocols.order_book.primitives import (
    Int32,
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


class OrderBook(BaseModel):
    """OrderBook."""

    exchange_id: str
    symbol: str
    bids: list[Int32]
    asks: list[Int32]
    timestamp: Int32
    datetime: str
    nonce: Int32

    @staticmethod
    def encode(proto_obj, orderbook: OrderBook) -> None:
        """Encode OrderBook to protobuf."""
        proto_obj.exchange_id = orderbook.exchange_id
        proto_obj.symbol = orderbook.symbol
        for item in orderbook.bids:
            proto_obj.bids.append(item)
        for item in orderbook.asks:
            proto_obj.asks.append(item)
        proto_obj.timestamp = orderbook.timestamp
        proto_obj.datetime = orderbook.datetime
        proto_obj.nonce = orderbook.nonce

    @classmethod
    def decode(cls, proto_obj) -> OrderBook:
        """Decode proto_obj to OrderBook."""
        exchange_id = proto_obj.exchange_id
        symbol = proto_obj.symbol
        bids = list(proto_obj.bids)
        asks = list(proto_obj.asks)
        timestamp = proto_obj.timestamp
        datetime = proto_obj.datetime
        nonce = proto_obj.nonce
        return cls(
            exchange_id=exchange_id,
            symbol=symbol,
            bids=bids,
            asks=asks,
            timestamp=timestamp,
            datetime=datetime,
            nonce=nonce,
        )


for cls in BaseModel.__subclasses__():
    if cls.__module__ == __name__:
        cls.model_rebuild()
