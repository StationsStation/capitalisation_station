"""Some tests for the HttpHandler of the simple_fsm skill."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from aea.test_tools.test_skill import BaseSkillTestCase

from packages.eightballer.skills.simple_fsm import PUBLIC_ID
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.skills.simple_fsm.behaviours import (
    ExecuteOrdersRound,
    ArbitrageabciappEvents,
    UnexpectedStateException,
)
from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus
from packages.eightballer.protocols.balances.custom_types import Balances
from packages.eightballer.skills.simple_fsm.behaviour_classes.collect_data_round import CollectDataRound


ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent


HAPPY_ORDER_SUBMISSION_RESULTS = [
    {
        "symbol": "LBTC/USDC",
        "type": OrderType.LIMIT,
        "status": OrderStatus.OPEN,
        "side": OrderSide.BUY,
    },
    {
        "symbol": "WEETH/USD",
        "type": OrderType.LIMIT,
        "status": OrderStatus.NEW,
        "side": OrderSide.SELL,
    },
    {
        "symbol": "LBTC/USDC",
        "type": OrderType.LIMIT,
        "status": OrderStatus.FILLED,
        "side": OrderSide.BUY,
    },
]

UNHAPPY_ORDER_SUBMISSION_RESULTS = [
    {
        "symbol": "LBTC/USDC",
        "type": OrderType.LIMIT,
        "status": OrderStatus.PARTIALLY_FILLED,
        "side": OrderSide.BUY,
    },
    {
        "symbol": "WEETH/USD",
        "type": OrderType.LIMIT,
        "status": OrderStatus.CANCELLED,
        "side": OrderSide.SELL,
    },
]


class TestExecuteOrdersRound(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)
    round_class = ExecuteOrdersRound

    @pytest.mark.skip("Skipping test for now.")
    def test_act(
        self,
        bridge_request,
    ):
        """Test the act method of the round."""
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        state.strategy.current_bridge_request = bridge_request
        with (
            patch.object(state.strategy, "build_transaction", return_value="transaction"),
            patch.object(state.strategy, "sign_and_send_txn", return_value=[True, bridge_request.claim_txn]),
        ):
            state.act()
        assert state.is_done
        assert state.event == ArbitrageabciappEvents.DONE

    @pytest.mark.parametrize("order_data", HAPPY_ORDER_SUBMISSION_RESULTS)
    def test_handle_submitted_order_happy_path(self, order_data):
        """Test that the response from the connection is handled correctly."""
        order = Order(**order_data)
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        state.strategy.state.submitted_orders.append(order)
        result = state.handle_submitted_order_response(
            order,
        )
        assert result is not None

    @pytest.mark.skip("Skipping test for now. post queues, test not functional.")
    @pytest.mark.parametrize("order_data", UNHAPPY_ORDER_SUBMISSION_RESULTS)
    def test_handle_submitted_order_unhappy_path(self, order_data):
        """Test that the response from the connection is handled correctly. We should raise an exception."""
        order = Order(**order_data)
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        state.strategy.state.submitted_orders.append(order)

        with pytest.raises(UnexpectedStateException) as excinfo:
            state.handle_submitted_order_response(
                order,
            )
        assert str(excinfo.value)

    @pytest.mark.skip("Skipping test for now. post queues, test not functional.")
    @pytest.mark.parametrize("order_data", HAPPY_ORDER_SUBMISSION_RESULTS)
    def test_send_failed_entry_create_order(self, order_data):
        """Test that the send_create_order method works correctly."""
        state: ExecuteOrdersRound = self.round_class(name="test", skill_context=self.skill.skill_context)

        def dummy_get_response(*args, **kwargs):
            del args, kwargs
            yield None

        order = Order(**order_data)
        with patch.object(state, "get_response", side_effect=dummy_get_response):
            res = state.send_create_order(
                order,
                is_entry_order=True,
                is_exit_order=False,
            )
            res = res
            assert res is None
        assert state._event == ArbitrageabciappEvents.ENTRY_EXIT_ERROR, "Event should be ENTRY_EXIT_ERROR"  # noqa


@pytest.mark.skip("Skipping as now use queues.")
class TestCollectDataRound(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)
    round_class = CollectDataRound

    def test_happy_path_collect_data(
        self,
    ):
        """Test that the send_create_order method works correctly."""
        self.round_class(name="test", skill_context=self.skill.skill_context)
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        state.setup()

        msg = BalancesMessage(performative=BalancesMessage.Performative.ALL_BALANCES, balances=Balances(balances=[]))

        def mock_generator():
            yield msg

        # Create the mock for get_response
        mock_get_response = MagicMock()
        mock_get_response.return_value = mock_generator()

        # Patch the get_response method
        with patch.object(state, "get_response", mock_get_response):
            # Run the function under test
            state.act()
            mock_get_response.assert_called_once()

    def test_unhappy_path_collect_data(
        self,
    ):
        """Test that the send_create_order method works correctly."""
        self.round_class(name="test", skill_context=self.skill.skill_context)
        state = self.round_class(name="test", skill_context=self.skill.skill_context)

        def dummy_get_response(*args, **kwargs):
            del args, kwargs
            yield None

        with (
            patch.object(state, "get_response", new=dummy_get_response),
            patch.object(state, "get_tickers", side_effect=dummy_get_response),
        ):
            list(state.act())

        assert state.is_done()
        assert state._event == ArbitrageabciappEvents.TIMEOUT, "Event should be TIMEOUT"  # noqa
