"""Test the spot_asset protocol."""

import asyncio
from unittest.mock import MagicMock

import pytest
from aea.mail.base import Envelope

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.tickers.dialogues import TickersDialogue, BaseTickersDialogues

from ..test_dcxt_connection import TEST_EXCHANGES, BaseDcxtConnectionTest, with_timeout, get_dialogues


TEST_MARKET = "BTC-PERP"

TIMEOUT = 10

DEFAULT_EXCHANGE = list(TEST_EXCHANGES.keys()).pop()


@pytest.mark.asyncio
class TestFetchTickers(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseTickersDialogues, TickersDialogue)

    @with_timeout(TIMEOUT)
    async def test_handles_get_all_tickers(self, exchange_id=DEFAULT_EXCHANGE) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=TickersMessage.Performative.GET_ALL_TICKERS,
            exchange_id=exchange_id,
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
        assert response.message.performative == TickersMessage.Performative.ALL_TICKERS, f"Error: {response}"


@pytest.mark.parametrize("exchange_id", TEST_EXCHANGES.keys())
@pytest.mark.asyncio
class TestConnectionHandlesExchangeErrors(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseTickersDialogues, TickersDialogue)

    async def test_handles_exchange_timeout(self, exchange_id) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=TickersMessage.Performative.GET_ALL_TICKERS,
            exchange_id=exchange_id,
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we create a mock object to simulate a timeout
        # simulate a raised exceptionS
        mocker = MagicMock(side_effect=dcxt.exceptions.RequestTimeout)
        self.connection._exchanges[exchange_id].fetch_tickers = mocker  # noqa

        response = await self.connection.protocol_interface.handle_envelope(envelope)

        assert response is not None
        assert isinstance(response, TickersMessage)
        assert response.performative == TickersMessage.Performative.ERROR, f"Error: {response}"
