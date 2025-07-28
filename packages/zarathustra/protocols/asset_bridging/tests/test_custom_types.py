"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.zarathustra.protocols.asset_bridging.custom_types import (
    ErrorInfo,
    BridgeResult,
    BridgeRequest,
)
from packages.zarathustra.protocols.asset_bridging.asset_bridging_pb2 import (
    AssetBridgingMessage as asset_bridging_pb2,  # noqa: N813
)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(BridgeRequest))
def test_bridgerequest(bridgerequest: BridgeRequest):
    """Test BridgeRequest."""
    assert isinstance(bridgerequest, BridgeRequest)
    proto_obj = asset_bridging_pb2.BridgeRequest()
    bridgerequest.encode(proto_obj, bridgerequest)
    result = BridgeRequest.decode(proto_obj)
    assert bridgerequest == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(BridgeResult))
def test_bridgeresult(bridgeresult: BridgeResult):
    """Test BridgeResult."""
    assert isinstance(bridgeresult, BridgeResult)
    proto_obj = asset_bridging_pb2.BridgeResult()
    bridgeresult.encode(proto_obj, bridgeresult)
    result = BridgeResult.decode(proto_obj)
    assert bridgeresult == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(ErrorInfo))
def test_errorinfo(errorinfo: ErrorInfo):
    """Test ErrorInfo."""
    assert isinstance(errorinfo, ErrorInfo)
    proto_obj = asset_bridging_pb2.ErrorInfo()
    errorinfo.encode(proto_obj, errorinfo)
    result = ErrorInfo.decode(proto_obj)
    assert errorinfo == result
