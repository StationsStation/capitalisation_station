"""Some tests for the HttpHandler of the simple_fsm skill."""

from pathlib import Path

from aea.test_tools.test_skill import BaseSkillTestCase

from packages.eightballer.protocols.orders import OrdersMessage
from packages.eightballer.connections.dcxt.connection import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus


ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent


class TestHandler(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(__file__).parent.parent

    @classmethod
    def method_setup(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()

    def test_setup(self):
        """Test the setup method of the handler."""
        self.assert_quantity_in_outbox(0)

    def test_handle_orders(self):
        """Test the handle_orders method of the handler."""
        orders_message = OrdersMessage(
            performative=OrdersMessage.Performative.ORDER,
            order=Order(
                symbol="BTC/USD",
                type=OrderType.LIMIT,
                status=OrderStatus.OPEN,
                side=OrderSide.BUY,
            ),
        )
        orders_message.sender = str(DCXT_PUBLIC_ID)
        orders_message.to = str(self.skill.skill_context.skill_id)
        self.skill.skill_context.handlers.dex_orders_handler.handle_wrapper(orders_message)
        self.assert_quantity_in_outbox(0)
