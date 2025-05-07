"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import given, strategies as st

from packages.eightballer.protocols.positions.custom_types import (
    Position,
    ErrorCode,
    Positions,
    PositionSide,
)
from packages.eightballer.protocols.positions.positions_pb2 import PositionsMessage as positions_pb2  # noqa: N813


@given(st.from_type(ErrorCode))
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = positions_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert errorcode == result


@given(st.from_type(Position))
def test_position(position: Position):
    """Test Position."""
    assert isinstance(position, Position)
    proto_obj = positions_pb2.Position()
    position.encode(proto_obj, position)
    result = Position.decode(proto_obj)
    assert position == result


@given(st.from_type(PositionSide))
def test_positionside(positionside: PositionSide):
    """Test PositionSide."""
    assert isinstance(positionside, PositionSide)
    proto_obj = positions_pb2.PositionSide()
    positionside.encode(proto_obj, positionside)
    result = PositionSide.decode(proto_obj)
    assert positionside == result


@given(st.from_type(Positions))
def test_positions(positions: Positions):
    """Test Positions."""
    assert isinstance(positions, Positions)
    proto_obj = positions_pb2.Positions()
    positions.encode(proto_obj, positions)
    result = Positions.decode(proto_obj)
    assert positions == result
