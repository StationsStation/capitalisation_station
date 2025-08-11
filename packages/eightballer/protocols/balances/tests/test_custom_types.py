"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.eightballer.protocols.balances.balances_pb2 import BalancesMessage as balances_pb2  # noqa: N813
from packages.eightballer.protocols.balances.custom_types import (
    Balance,
    Balances,
    ErrorCode,
)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Balance))
def test_balance(balance: Balance):
    """Test Balance."""
    assert isinstance(balance, Balance)
    proto_obj = balances_pb2.Balance()
    balance.encode(proto_obj, balance)
    result = Balance.decode(proto_obj)
    assert balance == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Balances))
def test_balances(balances: Balances):
    """Test Balances."""
    assert isinstance(balances, Balances)
    proto_obj = balances_pb2.Balances()
    balances.encode(proto_obj, balances)
    result = Balances.decode(proto_obj)
    assert balances == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(ErrorCode))
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = balances_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert errorcode == result
