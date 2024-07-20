"""Test the ohlcv connection."""
import asyncio

import pytest
from aea.mail.base import Envelope

from packages.eightballer.protocols.ohlcv import OhlcvMessage
from packages.eightballer.protocols.ohlcv.dialogues import OhlcvDialogue, OhlcvDialogues
from tests.test_connections.test_dcxt_connection.test_dcxt_connection import (
    BaseDcxtConnectionTest,
    get_dialogues,
    with_timeout,
)


@pytest.mark.asyncio
class TestOhlcvBalance(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(OhlcvDialogues, OhlcvDialogue)

    @with_timeout(3)
    async def test_handles_get_spot_message(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=OhlcvMessage.Performative.SUBSCRIBE,
            exchange_id="deribit",
            market_name="ETH-PERPETUAL",
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
        assert isinstance(response.message, OhlcvMessage)
        assert (
            response.message.performative == OhlcvMessage.Performative.END
        ), "Error: {}".format(response.message)

    @pytest.mark.skip("spot message not returingin for deribit")
    @with_timeout(10)
    async def test_handles_get_spot_message_result(self) -> None:
        """Test that the expected success message is received when submitting as balance request."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=OhlcvMessage.Performative.SUBSCRIBE,
            exchange_id="deribit",
            market_name="ETH-PERPETUAL",
            interval=15,
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
        assert isinstance(response.message, OhlcvMessage)
        assert (
            response.message.performative == OhlcvMessage.Performative.END
        ), "Error: {}".format(response.message)
        await asyncio.sleep(1)
        response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, OhlcvMessage)
        assert (
            response.message.performative == OhlcvMessage.Performative.CANDLESTICK
        ), "Error: {}".format(response.message)