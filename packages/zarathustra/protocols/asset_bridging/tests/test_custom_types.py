"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import given, strategies as st
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    ErrorCode,
    BridgeStatus,
)
from packages.zarathustra.protocols.asset_bridging.asset_bridging_pb2 import (
    AssetBridgingMessage as asset_bridging_pb2,  # noqa: N813
)


bridgestatus_strategy = st.from_type(BridgeStatus)
errorcode_strategy = st.from_type(ErrorCode)


@given(bridgestatus_strategy)
def test_bridgestatus(bridgestatus: BridgeStatus):
    """Test BridgeStatus."""
    assert isinstance(bridgestatus, BridgeStatus)
    proto_obj = asset_bridging_pb2.BridgeStatus()
    bridgestatus.encode(proto_obj, bridgestatus)
    result = BridgeStatus.decode(proto_obj)
    assert id(bridgestatus) != id(result)
    assert bridgestatus == result


@given(errorcode_strategy)
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = asset_bridging_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert id(errorcode) != id(result)
    assert errorcode == result
