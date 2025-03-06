"""Tests for the position interface."""

import asyncio
from unittest.mock import patch

import pytest
from aea.mail.base import Envelope

from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue, BasePositionsDialogues
from packages.eightballer.protocols.positions.custom_types import Positions
from packages.eightballer.connections.ccxt_wrapper.tests.test_ccxt_connection import (
    BaseCcxtConnectionTest,
    with_timeout,
    get_dialogues,
)


@pytest.mark.asyncio
@pytest.mark.skip("Not implemented")
class TestPositionInterface(BaseCcxtConnectionTest):
    """Test the position interface."""

    DIALOGUES = get_dialogues(BasePositionsDialogues, PositionsDialogue)

    @pytest.mark.asyncio
    @with_timeout(4)
    async def test_get_all_positions(self):
        """Test the get all positions method."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=PositionsMessage.Performative.GET_ALL_POSITIONS,
            exchange_id="deribit",
            params={},
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we make sure that we mock the api call
        with patch.object(
            self.connection._exchanges["deribit"],  # noqa
            "fetch_positions",
            return_value=[],
        ):
            await self.connection.send(envelope)
            await asyncio.sleep(1)
            response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, PositionsMessage)
        assert response.message.performative == PositionsMessage.Performative.ALL_POSITIONS, f"Error: {response}"
        assert isinstance(response.message.positions, Positions)
