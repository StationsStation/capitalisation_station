"""
Test order protocol
"""
from abc import abstractmethod

from aea.mail.base import Envelope

from packages.eightballer.protocols.spot_asset import SpotAssetMessage
from packages.eightballer.protocols.spot_asset.custom_types import ErrorCode


class BaseTestMessageConstruction:
    """Base class to test message construction for the ABCI protocol."""

    msg_class = SpotAssetMessage

    id: float = "btc"
    total: float = 0.001
    free: float = 0.001
    available_without_borrow: float = 0.001
    usd_value: float = 10
    exchange_id: str = "binance"

    @abstractmethod
    def build_message(self) -> SpotAssetMessage:
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
        assert (
            expected_envelope.protocol_specification_id
            == actual_envelope.protocol_specification_id
        )
        assert expected_envelope.message != actual_envelope.message

        actual_msg = self.msg_class.serializer.decode(actual_envelope.message_bytes)
        actual_msg.to = actual_envelope.to
        actual_msg.sender = actual_envelope.sender
        expected_msg = msg
        assert expected_msg == actual_msg


class TestCreateAssetMessage(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> SpotAssetMessage:
        """Build the message."""
        return SpotAssetMessage(
            performative=SpotAssetMessage.Performative.SPOT_ASSET,  # type: ignore
            name=self.id,
            total=self.total,
            free=self.free,
            available_without_borrow=self.available_without_borrow,
            usd_value=self.usd_value,
        )


class TestGetSpotAsset(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> SpotAssetMessage:
        """Build the message."""
        return SpotAssetMessage(
            performative=SpotAssetMessage.Performative.GET_SPOT_ASSET,  # type: ignore
            name=self.id,
            exchange_id=self.exchange_id,
        )


class TestGetSpotAssets(BaseTestMessageConstruction):
    """Test message."""

    def build_message(self) -> SpotAssetMessage:
        """Build the message."""
        return SpotAssetMessage(
            performative=SpotAssetMessage.Performative.GET_SPOT_ASSETS,  # type: ignore
            exchange_id=self.exchange_id,
        )


class BaseTestCustomType:
    """Base Test class"""

    CUSTOM_TYPE: callable

    def test_initialize(self):
        """Test if initialises."""
        self.CUSTOM_TYPE(1)


class TestErrorCode(BaseTestCustomType):
    """Custome Error code."""

    CUSTOM_TYPE = ErrorCode
