"""Test the spot_asset protocol."""

import asyncio
from unittest.mock import MagicMock

import pytest
from aea.mail.base import Envelope

import ccxt
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.orders.dialogues import OrdersDialogue, BaseOrdersDialogues

from ..test_ccxt_connection import DEFAULT_EXCHANGE_ID, BaseCcxtConnectionTest, with_timeout, get_dialogues


TEST_SETTLEMENTS = [
    {
        "type": "delivery",
        "timestamp": "1664524800043",
        "session_profit_loss": "4088.961154351",
        "profit_loss": "0.036",
        "position": "-2.0",
        "mark_price": "0.0",
        "instrument_name": "ETH-30SEP22-1300-P",
        "index_price": "1343.54",
    },
    {
        "type": "delivery",
        "timestamp": "1666598400038",
        "session_profit_loss": "5507.683847052",
        "profit_loss": "-0.01553694",
        "position": "-4.0",
        "mark_price": "0.008634235",
        "instrument_name": "ETH-24OCT22-1325-C",
        "index_price": "1336.54",
    },
]


@pytest.mark.asyncio
class TestOrdersExecution(BaseCcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseOrdersDialogues, OrdersDialogue)

    @with_timeout(3)
    async def test_handles_get_orders(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=OrdersMessage.Performative.GET_ORDERS,
            exchange_id=DEFAULT_EXCHANGE_ID,
        )
        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we create a mock object to simulate a timeout
        # simulate a raised exceptionS
        mocker = MagicMock(side_effect=ccxt.errors.ExchangeError)

        self.connection._exchanges[DEFAULT_EXCHANGE_ID].fetch_open_orders = mocker  # noqa

        await self.connection.send(envelope)
        await asyncio.sleep(1)
        response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, OrdersMessage)
        # we assume that the response is an error message as we have no authentification.
        assert response.message.performative == OrdersMessage.Performative.ERROR, f"Error: {response}"

    @with_timeout(3)
    async def test_handles_get_settlements(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=OrdersMessage.Performative.GET_SETTLEMENTS,
            exchange_id=DEFAULT_EXCHANGE_ID,
            start_timestamp=0.0,
            end_timestamp=0.0,
            currency="ETH",
        )

        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )

        async def mock_fetch_settlements(*args, **kwargs):  # noqa
            del args, kwargs
            return {"result": {"settlements": TEST_SETTLEMENTS}}

        # we create a mock object to simulate the response. We will return the 2 test settlement items.
        mocker = MagicMock()
        mocker.side_effect = mock_fetch_settlements
        self.connection._exchanges[  # noqa
            DEFAULT_EXCHANGE_ID
        ].private_get_get_settlement_history_by_currency = mocker  # noqa
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, OrdersMessage)
        assert response.message.performative == OrdersMessage.Performative.ORDERS, f"Error: {response}"
