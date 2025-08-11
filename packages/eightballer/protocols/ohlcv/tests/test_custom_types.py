"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.eightballer.protocols.ohlcv.ohlcv_pb2 import OhlcvMessage as ohlcv_pb2  # noqa: N813
from packages.eightballer.protocols.ohlcv.custom_types import (
    ErrorCode,
)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(ErrorCode))
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = ohlcv_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert errorcode == result
