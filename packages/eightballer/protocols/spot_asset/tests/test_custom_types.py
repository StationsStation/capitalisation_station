"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.eightballer.protocols.spot_asset.custom_types import (
    Decimal,
    ErrorCode,
)
from packages.eightballer.protocols.spot_asset.spot_asset_pb2 import SpotAssetMessage as spot_asset_pb2  # noqa: N813


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Decimal))
def test_decimal(decimal: Decimal):
    """Test Decimal."""
    assert isinstance(decimal, Decimal)
    proto_obj = spot_asset_pb2.Decimal()
    decimal.encode(proto_obj, decimal)
    result = Decimal.decode(proto_obj)
    assert decimal == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(ErrorCode))
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = spot_asset_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert errorcode == result
