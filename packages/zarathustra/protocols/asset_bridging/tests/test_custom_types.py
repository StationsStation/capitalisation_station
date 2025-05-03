"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import given, strategies as st
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    ErrorInfo,
    BridgeResult,
    BridgeRequest,
)
from packages.zarathustra.protocols.asset_bridging.asset_bridging_pb2 import (
    AssetBridgingMessage as asset_bridging_pb2,  # noqa: N813
)


bridgerequest_strategy = st.from_type(BridgeRequest)
bridgeresult_strategy = st.from_type(BridgeResult)
errorinfo_strategy = st.from_type(ErrorInfo)


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


@given(errorinfo_strategy)
def test_errorinfo(errorinfo: ErrorInfo):
    """Test ErrorInfo."""
    assert isinstance(errorinfo, ErrorInfo)
    proto_obj = asset_bridging_pb2.ErrorInfo()
    errorinfo.encode(proto_obj, errorinfo)
    result = ErrorInfo.decode(proto_obj)
    assert id(errorinfo) != id(result)
    assert errorinfo == result
