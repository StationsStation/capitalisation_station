"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.eightballer.protocols.order_book.custom_types import (
    OrderBook,
)
from packages.eightballer.protocols.order_book.order_book_pb2 import OrderBookMessage as order_book_pb2  # noqa: N813


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(OrderBook))
def test_orderbook(orderbook: OrderBook):
    """Test OrderBook."""
    assert isinstance(orderbook, OrderBook)
    proto_obj = order_book_pb2.OrderBook()
    orderbook.encode(proto_obj, orderbook)
    result = OrderBook.decode(proto_obj)
    assert orderbook == result
