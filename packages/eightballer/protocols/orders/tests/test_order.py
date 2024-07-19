"""
Test order protocol
"""
# pylint: disable=R1735
from abc import abstractmethod

from aea.mail.base import Envelope

from packages.eightballer.protocols.orders import OrdersMessage
from packages.eightballer.protocols.orders.custom_types import ErrorCode, Order, OrderSide, OrderStatus, OrderType

RAW_ORDER = {
    "id": "test_order",
    "amount": 1,
    "filled": 1,
    "exchange_id": "test_ex",
    "status": OrderStatus.FILLED,
    "side": OrderSide.BUY,
    "type": OrderType.LIMIT,
}


class BaseTestMessageConstruction:
    """Base class to test message construction for the ABCI protocol."""

    msg_class = OrdersMessage

    @abstractmethod
    def build_message(self) -> OrdersMessage:
        """Build the message to be used for testing."""

    def test_run(self) -> None:
        """Run the test."""
        msg = self.build_message()
        msg.to = "receiver"
        envelope = Envelope(to=msg.to, sender="sender", message=msg)
        envelope_bytes = envelope.encode()

        actual_envelope = Envelope.decode(envelope_bytes)
        expected_envelope = envelope

        assert expected_envelope.to == actual_envelope.to
        assert expected_envelope.sender == actual_envelope.sender
        assert expected_envelope.protocol_specification_id == actual_envelope.protocol_specification_id
        assert expected_envelope.message != actual_envelope.message

        actual_msg = self.msg_class.serializer.decode(actual_envelope.message_bytes)
        actual_msg.to = actual_envelope.to
        actual_msg.sender = actual_envelope.sender
        expected_msg = msg
        assert expected_msg == actual_msg


class TestCreateOrdersMessage(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OrdersMessage:
        """Build the message."""
        order = Order(**RAW_ORDER)
        return OrdersMessage(
            performative=OrdersMessage.Performative.CREATE_ORDER,
            order=order,
        )


class TestCreateCancelOrder(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OrdersMessage:
        """Build the message."""
        params = dict(exchange_id="test_ex", id="test_order")
        return OrdersMessage(
            performative=OrdersMessage.Performative.CANCEL_ORDER,  # type: ignore
            order=Order(**params),
        )


class TestGetOrder(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OrdersMessage:
        """Build the message."""
        params = dict(id="test_order")
        return OrdersMessage(
            performative=OrdersMessage.Performative.GET_ORDER,
            order=Order(**params),  # type: ignore
        )


class TestOrder(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OrdersMessage:
        """Build the message."""
        params = dict(
            id="test_order",
            amount=1,
            filled=1,
            side=OrderSide.BUY,
            exchange_id="test_ex",
            status=OrderStatus.FILLED,
            type=OrderType.LIMIT,
            symbol="test_market",
        )
        return OrdersMessage(
            performative=OrdersMessage.Performative.ORDER,
            order=Order(**params),  # type: ignore
        )


class TestGetOrders(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OrdersMessage:
        """Build the message."""
        params = dict(
            exchange_id="test_ex",
            status=OrderStatus.OPEN,
            order_type=OrderType.LIMIT,
        )
        return OrdersMessage(performative=OrdersMessage.Performative.GET_ORDERS, **params)  # type: ignore


class BaseTestCustomType:
    """Base Test class"""

    CUSTOM_TYPE: callable

    def test_initialize(self):
        """Test if initialises."""
        self.CUSTOM_TYPE(1)


class TestOrderSide(BaseTestCustomType):
    """Custom order side."""

    CUSTOM_TYPE = OrderSide


class TestOrderType(BaseTestCustomType):
    """Custome order type."""

    CUSTOM_TYPE = OrderType


class TestOrderStatus(BaseTestCustomType):
    """Custom Status code."""

    CUSTOM_TYPE = OrderStatus


class TestErrorCode(BaseTestCustomType):
    """Custome Error code."""

    CUSTOM_TYPE = ErrorCode
