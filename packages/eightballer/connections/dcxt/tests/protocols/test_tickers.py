"""Test the spot_asset protocol."""

import asyncio
from unittest.mock import MagicMock

import pytest
from aea.mail.base import Envelope

from dcxt.tests.test_dcxt_connection import TIMEOUT, TEST_EXCHANGES, BaseDcxtConnectionTest, get_dialogues
from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.tickers.dialogues import TickersDialogue, BaseTickersDialogues


TEST_MARKET = "WETH/USDC"


DEFAULT_EXCHANGE = list(TEST_EXCHANGES.keys()).pop()


@pytest.mark.flaky(reruns=3, reruns_delay=60)
@pytest.mark.asyncio
@pytest.mark.parametrize("exchange", TEST_EXCHANGES)
class TestFetchTickers(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseTickersDialogues, TickersDialogue)

    async def test_handles_get_all_tickers(
        self,
        exchange: tuple[str, str],
    ) -> None:
        """Can handle ohlcv messages."""
        exchange_id, ledger_id = exchange
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=TickersMessage.Performative.GET_ALL_TICKERS,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        async with asyncio.timeout(TIMEOUT * 2):  # we need to wait for the response a bit longer
            response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, TickersMessage)
        assert response.message.performative == TickersMessage.Performative.ALL_TICKERS, f"Error: {response}"


@pytest.mark.asyncio
@pytest.mark.parametrize("exchange", list(TEST_EXCHANGES.keys()))
class TestFetchTicker(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseTickersDialogues, TickersDialogue)

    async def test_handles_get_ticker(
        self,
        exchange: tuple[str, str],
    ) -> None:
        """Can handle ohlcv messages."""
        exchange_id, ledger_id = exchange
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=TickersMessage.Performative.GET_TICKER,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
            symbol=TEST_MARKET if exchange_id != "derive" else "ETH/USDC",  # Derive exchange does not support WETH/USDC
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        async with asyncio.timeout(TIMEOUT):
            response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, TickersMessage)
        assert response.message.performative == TickersMessage.Performative.TICKER, f"Error: {response}"


@pytest.mark.parametrize("exchange_id", TEST_EXCHANGES.keys())
@pytest.mark.asyncio
class TestConnectionHandlesExchangeErrors(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseTickersDialogues, TickersDialogue)

    async def test_handles_exchange_timeout(
        self,
        exchange_id,
    ) -> None:
        """Can handle ohlcv messages."""
        exchange_id, ledger_id = exchange_id
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=TickersMessage.Performative.GET_ALL_TICKERS,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we create a mock object to simulate a timeout
        # simulate a raised exceptionS
        mocker = MagicMock(side_effect=dcxt.exceptions.RequestTimeout)
        self.connection._exchanges[ledger_id][exchange_id].fetch_tickers = mocker  # noqa

        response = await self.connection.protocol_interface.handle_envelope(envelope)

        assert response is not None
        assert isinstance(response, TickersMessage)
        assert response.performative == TickersMessage.Performative.ERROR, f"Error: {response}"
