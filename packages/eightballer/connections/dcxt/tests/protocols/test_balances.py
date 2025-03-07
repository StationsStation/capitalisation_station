"""Test the spot_asset protocol."""

import asyncio
from unittest.mock import MagicMock

import pytest
from aea.mail.base import Envelope

from dcxt.tests.test_dcxt_connection import TEST_EXCHANGES, BaseDcxtConnectionTest, with_timeout, get_dialogues
from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.balances.dialogues import BalancesDialogue, BaseBalancesDialogues
from packages.eightballer.connections.dcxt.tests.protocols.test_tickers import TIMEOUT


@pytest.mark.asyncio
@pytest.mark.skip("Not implemented")
class TestMarkets(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseBalancesDialogues, BalancesDialogue)

    @with_timeout(TIMEOUT)
    async def test_handles_get_all_markets(
        self,
    ) -> None:
        """Can handle ohlcv messages."""
        for exchange in TEST_EXCHANGES:
            await self.connection.connect()
            dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
            exchange_id, ledger_id = exchange.split("_")
            request, _ = dialogues.create(
                counterparty=str(self.connection.connection_id),
                performative=BalancesMessage.Performative.GET_ALL_BALANCES,
                exchange_id=exchange_id,
                ledger_id=ledger_id,
                params={},
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
            assert isinstance(response.message, BalancesMessage)
            assert response.message.performative == BalancesMessage.Performative.ALL_MARKETS, f"Error: {response}"


@pytest.mark.asyncio
@pytest.mark.skip("Not implemented")
class TestConnectionHandlesExchangeErrors(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseBalancesDialogues, BalancesDialogue)

    @pytest.mark.parametrize("exchange", TEST_EXCHANGES)
    async def test_handles_exchange_timeout(self, exchange) -> None:
        """Can handle ohlcv messages."""

        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        exchange_id, ledger_id = exchange.split("_")
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=BalancesMessage.Performative.GET_ALL_BALANCES,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
            params={},
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we create a mock object to simulate a timeout
        # simulate a raised exceptionS

        mocker = MagicMock(side_effect=dcxt.exceptions.RequestTimeout)
        self.connection._exchanges[exchange].fetch_markets = mocker  # noqa

        response = await self.connection.protocol_interface.handle_envelope(envelope)

        assert response is not None
        assert isinstance(response, BalancesMessage)
        assert response.performative == BalancesMessage.Performative.ERROR, f"Error: {response}"
