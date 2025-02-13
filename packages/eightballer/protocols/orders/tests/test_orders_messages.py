#                                                                             --
#
#   Copyright 2025 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#                                                                             --

"""Test messages module for orders protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.orders.custom_types import (
    Order,
    Orders,
    ErrorCode,
    OrderSide,
    OrderType,
    OrderStatus,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageOrders(BaseProtocolMessagesTestCase):
    """Test for the 'orders' protocol message."""

    MESSAGE_CLASS = OrdersMessage

    def build_messages(self) -> list[OrdersMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            OrdersMessage(
                performative=OrdersMessage.Performative.CREATE_ORDER,
                order=Order(**load_data("Order")),  # check it please!
                exchange_id="some str",
                ledger_id="some str",
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.ORDER_CREATED,
                order=Order(**load_data("Order")),  # check it please!
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.CANCEL_ORDER,
                order=Order(**load_data("Order")),  # check it please!
                exchange_id="some str",
                ledger_id="some str",
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.ORDER_CANCELLED,
                order=Order(**load_data("Order")),  # check it please!
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.GET_ORDERS,
                symbol="some str",
                currency="some str",
                order_type=OrderType(0),
                side=OrderSide(0),
                status=OrderStatus(0),
                exchange_id="some str",
                ledger_id="some str",
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.GET_SETTLEMENTS,
                currency="some str",
                end_timestamp=1.0,
                start_timestamp=1.0,
                ledger_id="some str",
                exchange_id="some str",
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.GET_ORDER,
                order=Order(**load_data("Order")),  # check it please!
                exchange_id="some str",
                ledger_id="some str",
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.ORDER,
                order=Order(**load_data("Order")),  # check it please!
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.ORDERS,
                orders=Orders(**load_data("Orders")),  # check it please!
            ),
            OrdersMessage(
                performative=OrdersMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
