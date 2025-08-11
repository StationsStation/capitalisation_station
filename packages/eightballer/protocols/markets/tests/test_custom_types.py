"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.eightballer.protocols.markets.markets_pb2 import MarketsMessage as markets_pb2  # noqa: N813
from packages.eightballer.protocols.markets.custom_types import (
    Market,
    Markets,
    ErrorCode,
)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(ErrorCode))
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = markets_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert errorcode == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Market))
def test_market(market: Market):
    """Test Market."""
    assert isinstance(market, Market)
    proto_obj = markets_pb2.Market()
    market.encode(proto_obj, market)
    result = Market.decode(proto_obj)
    assert market == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Markets))
def test_markets(markets: Markets):
    """Test Markets."""
    assert isinstance(markets, Markets)
    proto_obj = markets_pb2.Markets()
    markets.encode(proto_obj, markets)
    result = Markets.decode(proto_obj)
    assert markets == result
