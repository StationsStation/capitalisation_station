"""Some tests for the HttpHandler of the simple_fsm skill."""

from pathlib import Path
from unittest.mock import patch

import pytest
from aea.test_tools.test_skill import BaseSkillTestCase

from packages.eightballer.skills.simple_fsm import PUBLIC_ID
from packages.eightballer.skills.simple_fsm.behaviours import (
    ExecuteOrdersRound,
    ArbitrageabciappEvents,
    UnexpectedStateException,
)
from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus


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
        result = state.handle_submitted_order_response(
            order,
        )
        assert result is not None

    @pytest.mark.parametrize("order_data", UNHAPPY_ORDER_SUBMISSION_RESULTS)
    def test_handle_submitted_order_unhappy_path(self, order_data):
        """Test that the response from the connection is handled correctly. We should raise an exception."""
        order = Order(**order_data)
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        with pytest.raises(UnexpectedStateException):
            state.handle_submitted_order_response(
                order,
            )
