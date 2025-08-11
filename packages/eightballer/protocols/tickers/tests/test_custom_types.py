"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.eightballer.protocols.tickers.tickers_pb2 import TickersMessage as tickers_pb2  # noqa: N813
from packages.eightballer.protocols.tickers.custom_types import (
    Ticker,
    Tickers,
    ErrorCode,
)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(ErrorCode))
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = tickers_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert errorcode == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Ticker))
def test_ticker(ticker: Ticker):
    """Test Ticker."""
    assert isinstance(ticker, Ticker)
    proto_obj = tickers_pb2.Ticker()
    ticker.encode(proto_obj, ticker)
    result = Ticker.decode(proto_obj)
    assert ticker == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Tickers))
def test_tickers(tickers: Tickers):
    """Test Tickers."""
    assert isinstance(tickers, Tickers)
    proto_obj = tickers_pb2.Tickers()
    tickers.encode(proto_obj, tickers)
    result = Tickers.decode(proto_obj)
    assert tickers == result
