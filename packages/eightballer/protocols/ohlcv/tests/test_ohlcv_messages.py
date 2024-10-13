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

"""Test messages module for ohlcv protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.ohlcv.message import OhlcvMessage
from packages.eightballer.protocols.ohlcv.custom_types import ErrorCode


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageOhlcv(BaseProtocolMessagesTestCase):
    """Test for the 'ohlcv' protocol message."""

    MESSAGE_CLASS = OhlcvMessage

    def build_messages(self) -> List[OhlcvMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            OhlcvMessage(
                performative=OhlcvMessage.Performative.SUBSCRIBE,
                exchange_id="some str",
                market_name="some str",
                interval=12,
            ),
            OhlcvMessage(
                performative=OhlcvMessage.Performative.CANDLESTICK,
                exchange_id="some str",
                market_name="some str",
                interval=12,
                open=1.0,
                high=1.0,
                low=1.0,
                close=1.0,
                volume=1.0,
                timestamp=12,
            ),
            OhlcvMessage(
                performative=OhlcvMessage.Performative.HISTORY,
                exchange_id="some str",
                market_name="some str",
                start_timestamp=12,
                end_timestamp=12,
                interval=12,
            ),
            OhlcvMessage(
                performative=OhlcvMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
            OhlcvMessage(
                performative=OhlcvMessage.Performative.END,
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
