"""Test the spot_asset protocol."""

import asyncio

import pytest
from aea.mail.base import Envelope

from dcxt.tests.test_dcxt_connection import BaseDcxtConnectionTest, with_timeout, get_dialogues
from packages.eightballer.protocols.spot_asset.message import SpotAssetMessage
from packages.eightballer.protocols.spot_asset.dialogues import SpotAssetDialogue, SpotAssetDialogues


@pytest.mark.skip
@pytest.mark.asyncio
class TestSpotAssetBalance(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES: get_dialogues(SpotAssetDialogues, SpotAssetDialogue)  # type: ignore

    @with_timeout(3)
    async def test_handles_get_spot_message(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=SpotAssetMessage.Performative.GET_SPOT_ASSET,
            exchange_id="ftx",
            name="BTC",
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, SpotAssetMessage)
        assert response.message.performative == SpotAssetMessage.Performative.END, f"Error: {response}"

    @with_timeout(4)
    async def test_handles_get_spot_message_result(self) -> None:
        """Test that the expected success message is received when submitting as balance request."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=SpotAssetMessage.Performative.GET_SPOT_ASSET,
            exchange_id="ftx",
            name="BTC",
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        await self.connection.receive()
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, SpotAssetMessage)
        assert response.message.performative == SpotAssetMessage.Performative.SPOT_ASSET, f"Error: {response}"
