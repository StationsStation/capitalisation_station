"""
Test ohlcv protocol
"""

from abc import abstractmethod

from aea.mail.base import Envelope

from packages.eightballer.protocols.ohlcv import OhlcvMessage
from packages.eightballer.protocols.ohlcv.custom_types import ErrorCode


class BaseTestMessageConstruction:
    """Base class to test message construction for the ABCI protocol."""

    msg_class = OhlcvMessage

    @abstractmethod
    def build_message(self) -> OhlcvMessage:
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


class TestSubscribeOhlcvMessage(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OhlcvMessage:
        """Build the message."""
        return OhlcvMessage(
            performative=OhlcvMessage.Performative.SUBSCRIBE,  # type: ignore
            exchange_id="test_ex",
            market_name="BTC/USD",
            interval=60,
        )


class TestCancleStickOhlcvMessage(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OhlcvMessage:
        """Build the message."""
        return OhlcvMessage(
            performative=OhlcvMessage.Performative.CANDLESTICK,  # type: ignore
            exchange_id="test_ex",
            market_name="BTC/USD",
            interval=60,
            open=10,
            high=10,
            close=10,
            low=10,
            volume=10.0,
            timestamp=1661713136,
        )


class TestHistoryOhlcvMessage(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> OhlcvMessage:
        """Build the message."""
        return OhlcvMessage(
            performative=OhlcvMessage.Performative.HISTORY,
            exchange_id="test_ex",
            market_name="BTC/USD",
            interval=60,
            start_timestamp=1661713136,
            end_timestamp=1661813136,
        )


class BaseTestCustomType:
    """Base Test class."""

    CUSTOM_TYPE: callable

    def test_initialize(self):
        """Test initialises."""
        self.CUSTOM_TYPE(1)


class TestErrorCode(BaseTestCustomType):
    """Test Error code."""

    CUSTOM_TYPE = ErrorCode
