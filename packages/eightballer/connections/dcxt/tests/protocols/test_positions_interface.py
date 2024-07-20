# ./test_position.py

# Path: tests/test_connections/test_ccxt_connection/protocols/test_position_interface.py
"""
Tests for the position interface.
"""
import asyncio
from unittest.mock import patch

import pytest
from aea.mail.base import Envelope

from packages.ardian.connections.ccxt.interfaces.interface_base import get_dialogues
from packages.eightballer.protocols.positions.custom_types import Positions
from packages.eightballer.protocols.positions.dialogues import (
    BasePositionsDialogues,
    PositionsDialogue,
)
from packages.eightballer.protocols.positions.message import PositionsMessage
from tests.test_connections.test_dcxt_connection.protocols.test_tickers import (
    TEST_EXCHANGE,
)
from tests.test_connections.test_dcxt_connection.test_dcxt_connection import (
    BaseDcxtConnectionTest,
    get_dialogues,
    with_timeout,
)


@pytest.mark.asyncio
class TestPositionInterface(BaseDcxtConnectionTest):
    """
    Test the position interface.
    """

    DIALOGUES = get_dialogues(BasePositionsDialogues, PositionsDialogue)

    @pytest.mark.asyncio
    @with_timeout(4)
    async def test_get_all_positions(self):
        """
        Test the get all positions method.
        """
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=PositionsMessage.Performative.GET_ALL_POSITIONS,
            exchange_id=TEST_EXCHANGE,
            params={},
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we make sure that we mock the api call
        with patch.object(
            self.connection._exchanges[TEST_EXCHANGE],
            "fetch_positions",
            return_value=[],
        ) as mock_get_all_positions:
            await self.connection.send(envelope)
            await asyncio.sleep(1)
            response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, PositionsMessage)
        assert (
            response.message.performative == PositionsMessage.Performative.ALL_POSITIONS
        ), "Error: {}".format(response.message)
        assert isinstance(response.message.positions, Positions)
