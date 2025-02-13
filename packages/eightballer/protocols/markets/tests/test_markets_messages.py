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

"""Test messages module for markets protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.markets.custom_types import (
    Market,
    Markets,
    ErrorCode,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageMarkets(BaseProtocolMessagesTestCase):
    """Test for the 'markets' protocol message."""

    MESSAGE_CLASS = MarketsMessage

    def build_messages(self) -> list[MarketsMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            MarketsMessage(
                performative=MarketsMessage.Performative.GET_ALL_MARKETS,
                exchange_id="some str",
                currency="some str",
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.GET_MARKET,
                id="some str",
                exchange_id="some str",
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.ALL_MARKETS,
                markets=Markets(**load_data("Markets")),  # check it please!
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.MARKET,
                market=Market(**load_data("Market")),  # check it please!
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
