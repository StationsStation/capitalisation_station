"""This module contains the tests of the handler class of the price_poller skill."""

from typing import cast
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from aea.test_tools.test_skill import BaseSkillTestCase

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.skills.reporting.handlers import OrdersReportingHandler, PositionsReportingHandler
from packages.eightballer.skills.reporting.strategy import ReportingStrategy
from packages.eightballer.protocols.orders.dialogues import OrdersDialogues
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.protocols.orders.custom_types import Order, Orders, OrderSide, OrderType, OrderStatus
from packages.eightballer.protocols.positions.custom_types import Position
from packages.eightballer.skills.reporting.tests.test_strategy import DB_FILE
from packages.eightballer.skills.reporting.tests.test_behaviour import ROOT_DIR
from packages.eightballer.connections.dcxt.tests.test_dcxt_connection import DEFAULT_EXCHANGE_ID


PATH_TO_SKILL = Path(ROOT_DIR, "packages", "eightballer", "skills", "reporting")


@pytest.mark.skip("reason: Type str not supported for Order.symbol!")
class TestOrderHandler(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = PATH_TO_SKILL

    @classmethod
    def teardown_method(cls):
        """Teardown the test."""
        if Path(DB_FILE).exists():
            Path(DB_FILE).unlink()

    @classmethod
    def setup(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        cls.handler = cast(
            OrdersReportingHandler,
            cls._skill.skill_context.handlers.orders_reporting_handler,
        )
        cls.logger = cls._skill.skill_context.logger

        cls.dialogues = cast(OrdersDialogues, cls._skill.skill_context.orders_dialogues)
        cls.skill_id = str(cls._skill.skill_context.skill_id)
        cls.sender = "fetchai/some_skill:0.1.0"

        # orders message
        cls.order_params = {
            "id": "123",
            "symbol": "BTC/USD",
            "status": OrderStatus.OPEN.value,
            "exchange_id": DEFAULT_EXCHANGE_ID,
            "side": OrderSide.BUY.value,
            "type": OrderType.LIMIT.value,
        }
        cls.position_params = {
            "id": "123",
            "symbol": "BTC/USD",
            "size": 0.1,
            "entry_price": 10000.0,
        }

    def test_setup(self):
        """Test the setup method."""
        self.handler.setup()

    def test_handle_order_message(self):
        """Test the _handle_request method of the http_echo handler where method is get."""
        # setup
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        self.handler.setup()
        incoming_message = cast(
            OrdersMessage,
            self.build_incoming_message(
                message_type=OrdersMessage,
                performative=OrdersMessage.Performative.ORDER,
                to=self.skill_id,
                sender=self.sender,
                order=Order(**self.order_params),
            ),
        )

        # operation
        with patch.object(self.logger, "log"):
            self.handler.handle(incoming_message)

        # after
        self.assert_quantity_in_outbox(0)

    def test_handle_orders_message(self):
        """Test the _handle_request method of the http_echo handler where method is get."""
        # setup
        self.handler.setup()
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        incoming_message = cast(
            OrdersMessage,
            self.build_incoming_message(
                message_type=OrdersMessage,
                performative=OrdersMessage.Performative.ORDERS,
                to=self.skill_id,
                sender=self.sender,
                orders=Orders(orders=[Order(**self.order_params)]),
            ),
        )

        # operation
        with patch.object(self.logger, "log"):
            self.handler.handle(incoming_message)

        # after
        self.assert_quantity_in_outbox(0)


@pytest.mark.skip("reason: Type str not supported for Order.symbol!")
class TestPositionHandler(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = PATH_TO_SKILL

    @classmethod
    def setup(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        cls.handler = cast(
            PositionsReportingHandler,
            cls._skill.skill_context.handlers.positions_reporting_handler,
        )
        cls.logger = cls._skill.skill_context.logger

        cls.dialogues = cast(OrdersDialogues, cls._skill.skill_context.orders_dialogues)
        cls.skill_id = str(cls._skill.skill_context.skill_id)
        cls.sender = "fetchai/some_skill:0.1.0"

        # orders message
        cls.position_params = {
            "id": "123",
            "symbol": "BTC/USD",
            "size": 0.1,
            "entry_price": 10000.0,
        }

    def test_handle_position_message(self):
        """Test the handle position of the position handler."""
        self.handler.setup()
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        incoming_message = cast(
            PositionsMessage,
            self.build_incoming_message(
                message_type=PositionsMessage,
                performative=PositionsMessage.Performative.POSITION,
                to=self.skill_id,
                sender=self.sender,
                exchange_id=DEFAULT_EXCHANGE_ID,
                position=Position(**self.position_params),
            ),
        )
        # we patch the strategy save_pivot_to_db method
        mock_func = MagicMock()
        mock_func.save_pivot_to_db.return_value = None
        strategy.save_pivot_to_db = mock_func.save_position_to_db
        with patch.object(self.logger, "log"):
            self.handler.handle(incoming_message)
        self.assert_quantity_in_outbox(0)

    def test_handle_position_bad_symbol_message(self):
        """Test the handle position of the position handler."""
        self.handler.setup()
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        incoming_message = cast(
            PositionsMessage,
            self.build_incoming_message(
                message_type=PositionsMessage,
                performative=PositionsMessage.Performative.ERROR,
                to=self.skill_id,
                sender=self.sender,
                error_code=PositionsMessage.ErrorCode.UNKNOWN_POSITION,
                error_msg="Bad symbol",
            ),
        )
        # we patch the strategy save_pivot_to_db method
        with patch.object(self.logger, "log"):
            self.handler.handle(incoming_message)
        self.assert_quantity_in_outbox(0)
