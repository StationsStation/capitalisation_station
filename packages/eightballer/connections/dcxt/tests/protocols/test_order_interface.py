"""Test the spot_asset protocol."""

import asyncio
from unittest.mock import MagicMock

import pytest
from aea.mail.base import Envelope

from dcxt.tests.test_dcxt_connection import TEST_EXCHANGES, BaseDcxtConnectionTest, with_timeout, get_dialogues
from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.orders.dialogues import OrdersDialogue, BaseOrdersDialogues
from packages.eightballer.protocols.orders.custom_types import Orders


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
class TestOrdersExecution(BaseDcxtConnectionTest):
    """Test protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseOrdersDialogues, OrdersDialogue)

    @pytest.mark.skip("Not implemented for spot assets.")
    @with_timeout(3)
    async def test_handles_get_orders(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120

        for exchange in TEST_EXCHANGES:
            request, _ = dialogues.create(
                counterparty=str(self.connection.connection_id),
                performative=OrdersMessage.Performative.GET_ORDERS,
                exchange_id=exchange,
            )
            envelope = Envelope(
                to=request.to,
                sender=request.sender,
                message=request,
            )
            # we create a mock object to simulate a timeout
            # simulate a raised exceptionS
            mocker = MagicMock(side_effect=dcxt.exceptions.ExchangeError)

            self.connection._exchanges[exchange].fetch_open_orders = mocker  # noqa

            await self.connection.send(envelope)
            await asyncio.sleep(1)
            response = await self.connection.receive()
            assert response is not None
            assert isinstance(response.message, OrdersMessage)
            # we assume that the response is an error message as we have no authentification.
            assert response.message.performative == OrdersMessage.Performative.ERROR, f"Error: {response}"

    @pytest.mark.skip("Not implemented for spot assets.")
    @with_timeout(3)
    async def test_handles_get_settlements(self) -> None:
        """Can handle ohlcv messages."""
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)
        for exchange in TEST_EXCHANGES:
            request, _ = dialogues.create(
                counterparty=str(self.connection.connection_id),
                performative=OrdersMessage.Performative.GET_SETTLEMENTS,
                exchange_id=exchange,
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
                exchange
            ].private_get_get_settlement_history_by_currency = mocker
            await self.connection.send(envelope)
            await asyncio.sleep(1)
            response = await self.connection.receive()
            assert response is not None
            assert isinstance(response.message, OrdersMessage)
            assert response.message.performative == OrdersMessage.Performative.ORDERS, f"Error: {response}"

    @pytest.mark.parametrize(
        "exchange",
        TEST_EXCHANGES,
    )
    async def test_get_open_orders_mock(self, exchange: tuple[str, str]) -> None:
        """Test get open orders."""
        exchange_id, ledger_id = exchange
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=OrdersMessage.Performative.GET_ORDERS,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
        )

        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )

        # we create a mock object to simulate the response.
        async def mock_fetch_open_orders(*args, **kwargs):
            del args, kwargs
            await asyncio.sleep(0.0)
            return Orders(orders=[])

        self.connection._exchanges[ledger_id][exchange_id].fetch_open_orders = mock_fetch_open_orders  # noqa
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, OrdersMessage)
        assert response.message.performative == OrdersMessage.Performative.ORDERS, f"Error: {response}"

    @pytest.mark.parametrize(
        "exchange",
        {k: v for k, v in list(TEST_EXCHANGES.items())[:1]},  # noqa
    )
    async def test_get_open_orders_integration(self, exchange: tuple[str, str]) -> None:
        """Test get open orders."""
        exchange_id, ledger_id = exchange
        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)
        request, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=OrdersMessage.Performative.GET_ORDERS,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
        )

        envelope = Envelope(
            to=request.to,
            sender=request.sender,
            message=request,
        )
        # we create a mock object to simulate the response.
        # self.connection._exchanges[ledger_id][exchange_id].fetch_open_orders = mock_fetch_open_orders  # noqa
        await self.connection.send(envelope)
        await asyncio.sleep(1)
        response = await self.connection.receive()
        assert response is not None
        assert isinstance(response.message, OrdersMessage)
        assert response.message.performative == OrdersMessage.Performative.ORDERS, f"Error: {response}"
