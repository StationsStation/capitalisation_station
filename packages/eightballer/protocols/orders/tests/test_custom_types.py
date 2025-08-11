"""Module containing tests for the pydantic models generated from the .proto file."""

from hypothesis import HealthCheck, given, settings, strategies as st

from packages.eightballer.protocols.orders.orders_pb2 import OrdersMessage as orders_pb2  # noqa: N813
from packages.eightballer.protocols.orders.custom_types import (
    Order,
    Orders,
    ErrorCode,
    OrderSide,
    OrderType,
    OrderStatus,
)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(ErrorCode))
def test_errorcode(errorcode: ErrorCode):
    """Test ErrorCode."""
    assert isinstance(errorcode, ErrorCode)
    proto_obj = orders_pb2.ErrorCode()
    errorcode.encode(proto_obj, errorcode)
    result = ErrorCode.decode(proto_obj)
    assert errorcode == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Order))
def test_order(order: Order):
    """Test Order."""
    assert isinstance(order, Order)
    proto_obj = orders_pb2.Order()
    order.encode(proto_obj, order)
    result = Order.decode(proto_obj)
    assert order == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(OrderSide))
def test_orderside(orderside: OrderSide):
    """Test OrderSide."""
    assert isinstance(orderside, OrderSide)
    proto_obj = orders_pb2.OrderSide()
    orderside.encode(proto_obj, orderside)
    result = OrderSide.decode(proto_obj)
    assert orderside == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(OrderStatus))
def test_orderstatus(orderstatus: OrderStatus):
    """Test OrderStatus."""
    assert isinstance(orderstatus, OrderStatus)
    proto_obj = orders_pb2.OrderStatus()
    orderstatus.encode(proto_obj, orderstatus)
    result = OrderStatus.decode(proto_obj)
    assert orderstatus == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(OrderType))
def test_ordertype(ordertype: OrderType):
    """Test OrderType."""
    assert isinstance(ordertype, OrderType)
    proto_obj = orders_pb2.OrderType()
    ordertype.encode(proto_obj, ordertype)
    result = OrderType.decode(proto_obj)
    assert ordertype == result


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(Orders))
def test_orders(orders: Orders):
    """Test Orders."""
    assert isinstance(orders, Orders)
    proto_obj = orders_pb2.Orders()
    orders.encode(proto_obj, orders)
    result = Orders.decode(proto_obj)
    assert orders == result
