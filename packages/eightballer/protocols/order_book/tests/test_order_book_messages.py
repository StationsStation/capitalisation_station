# -*- coding: utf-8 -*-
#                                                                             --
#
#   Copyright 2024 eightballer
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

"""Test messages module for order_book protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.order_book.message import OrderBookMessage
from packages.eightballer.protocols.order_book.custom_types import OrderBook


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageOrderBook(BaseProtocolMessagesTestCase):
    """Test for the 'order_book' protocol message."""

    MESSAGE_CLASS = OrderBookMessage

    def build_messages(self) -> List[OrderBookMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            OrderBookMessage(
                performative=OrderBookMessage.Performative.SUBSCRIBE,
                exchange_id="some str",
                symbol="some str",
                precision="some str",
                interval=12,
            ),
            OrderBookMessage(
                performative=OrderBookMessage.Performative.UNSUBSCRIBE,
                exchange_id="some str",
                symbol="some str",
            ),
            OrderBookMessage(
                performative=OrderBookMessage.Performative.ORDER_BOOK_UPDATE,
                order_book=OrderBook(**load_data("OrderBook")),  # check it please!
            ),
            OrderBookMessage(
                performative=OrderBookMessage.Performative.ERROR,
                error_msg="some str",
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
