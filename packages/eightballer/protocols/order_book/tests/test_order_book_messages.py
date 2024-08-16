# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

"""Test messages module for order_book protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
# pylint: disable=R1735
from typing import List

import pytest
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.order_book.message import OrderBookMessage
from packages.eightballer.protocols.order_book.custom_types import OrderBook


@pytest.mark.skip("Not implemented yet")
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
                order_book=OrderBook(
                    exchange_id="some str",
                    symbol="some str",
                    asks=[[1.0, 2.0], [3.0, 4.0]],
                    bids=[[5.0, 6.0], [7.0, 8.0]],
                    timestamp=123,
                    nonce=456,
                    datetime="some str",
                ),  # check it please!
            ),
            OrderBookMessage(
                performative=OrderBookMessage.Performative.ERROR,
                error_msg="some str",
            ),
        ]

    def build_inconsistent(self) -> List[OrderBookMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            OrderBookMessage(
                performative=OrderBookMessage.Performative.SUBSCRIBE,
                # skip content: exchange_id
                symbol="some str",
                precision="some str",
                interval=12,
            ),
            OrderBookMessage(
                performative=OrderBookMessage.Performative.UNSUBSCRIBE,
                # skip content: exchange_id
                symbol="some str",
            ),
            OrderBookMessage(
                performative=OrderBookMessage.Performative.ORDER_BOOK_UPDATE,
                # skip content: order_book
            ),
            OrderBookMessage(
                performative=OrderBookMessage.Performative.ERROR,
                # skip content: error_msg
            ),
        ]
