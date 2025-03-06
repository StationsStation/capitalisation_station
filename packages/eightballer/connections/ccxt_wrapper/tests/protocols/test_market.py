"""Test the spot_asset protocol."""

import asyncio
from unittest.mock import MagicMock

import ccxt
import pytest
from aea.mail.base import Envelope

from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.markets.dialogues import MarketsDialogue, BaseMarketsDialogues
from packages.eightballer.connections.ccxt_wrapper.tests.test_ccxt_connection import (
    BaseCcxtConnectionTest,
    with_timeout,
    get_dialogues,
)


TEST_EXCHANGE = "deribit"
TEST_MARKET = "BTC-PERPETUAL"


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires Deribit Api Keys.")
class TestMarkets(BaseCcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseMarketsDialogues, MarketsDialogue)

    @with_timeout(3)
    async def test_handles_get_all_markets(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=MarketsMessage.Performative.GET_ALL_MARKETS,
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
        assert isinstance(response.message, MarketsMessage)
        assert response.message.performative == MarketsMessage.Performative.ALL_MARKETS, f"Error: {response}"

    @with_timeout(3)
    async def test_handles_get_market(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=MarketsMessage.Performative.GET_MARKET,
            exchange_id=TEST_EXCHANGE,
            id="BTC-PERPETUAL",
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
        assert isinstance(response.message, MarketsMessage)
        assert response.message.performative == MarketsMessage.Performative.MARKET, f"Error: {response}"


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires Deribit Api Keys.")
class TestConnectionHandlesExchangeErrors(BaseCcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseMarketsDialogues, MarketsDialogue)

    @with_timeout(3)
    async def test_handles_exchange_timeout(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=MarketsMessage.Performative.GET_ALL_MARKETS,
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
        self.connection._exchanges[TEST_EXCHANGE].fetch_markets = mocker  # noqa

        response = await self.connection.protocol_interface.handle_envelope(envelope)

        assert response is not None
        assert isinstance(response, MarketsMessage)
        assert response.performative == MarketsMessage.Performative.ERROR, f"Error: {response}"
