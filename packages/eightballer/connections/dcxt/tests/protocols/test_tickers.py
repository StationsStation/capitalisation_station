"""Test the spot_asset protocol."""
import asyncio
from unittest.mock import MagicMock

import ccxt
import pytest
from aea.mail.base import Envelope

from packages.eightballer.protocols.tickers.dialogues import (
    BaseTickersDialogues,
    TickersDialogue,
)
from packages.eightballer.protocols.tickers.message import TickersMessage
from tests.test_connections.test_dcxt_connection.test_dcxt_connection import (
    BaseDcxtConnectionTest,
    get_dialogues,
    with_timeout,
)

TEST_EXCHANGE = "lyra"
TEST_MARKET = "BTC-PERP"


@pytest.mark.asyncio
class TestFetchTickers(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseTickersDialogues, TickersDialogue)

    @with_timeout(30)
    async def test_handles_get_all_tickers(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=TickersMessage.Performative.GET_ALL_TICKERS,
            exchange_id=TEST_EXCHANGE,
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
        assert isinstance(response.message, TickersMessage)
        assert (
            response.message.performative == TickersMessage.Performative.ALL_TICKERS
        ), "Error: {}".format(response.message)


@pytest.mark.asyncio
class TestConnectionHandlesExchangeErrors(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseTickersDialogues, TickersDialogue)

    @with_timeout(3)
    async def test_handles_exchange_timeout(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=TickersMessage.Performative.GET_ALL_TICKERS,
            exchange_id=TEST_EXCHANGE,
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we create a mock object to simulate a timeout
        # simulate a raised exceptionS
        mocker = MagicMock(side_effect=ccxt.errors.RequestTimeout)
        self.connection._exchanges[TEST_EXCHANGE].fetch_tickers = mocker  # type: ignore

        response = await self.connection.protocol_interface.handle_envelope(envelope)

        assert response is not None
        assert isinstance(response, TickersMessage)
        assert (
            response.performative == TickersMessage.Performative.ERROR
        ), "Error: {}".format(response)
