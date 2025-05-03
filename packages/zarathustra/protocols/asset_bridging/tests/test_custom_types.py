"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import given, strategies as st
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    ErrorCode,
    BridgeResult,
    BridgeRequest,
)
from packages.zarathustra.protocols.asset_bridging.asset_bridging_pb2 import (
    AssetBridgingMessage as asset_bridging_pb2,  # noqa: N813
)


bridgerequest_strategy = st.from_type(BridgeRequest)
bridgeresult_strategy = st.from_type(BridgeResult)
errorcode_strategy = st.from_type(ErrorCode)


@given(bridgerequest_strategy)
def test_bridgerequest(bridgerequest: BridgeRequest):
    """Test BridgeRequest."""
    assert isinstance(bridgerequest, BridgeRequest)
    proto_obj = asset_bridging_pb2.BridgeRequest()
    bridgerequest.encode(proto_obj, bridgerequest)
    result = BridgeRequest.decode(proto_obj)
    assert id(bridgerequest) != id(result)
    assert bridgerequest == result


@given(bridgeresult_strategy)
def test_bridgeresult(bridgeresult: BridgeResult):
    """Test BridgeResult."""
    assert isinstance(bridgeresult, BridgeResult)
    proto_obj = asset_bridging_pb2.BridgeResult()
    bridgeresult.encode(proto_obj, bridgeresult)
    result = BridgeResult.decode(proto_obj)
    assert id(bridgeresult) != id(result)
    assert bridgeresult == result


@given(errorcode_strategy)
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = asset_bridging_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert id(errorcode) != id(result)
    assert errorcode == result
