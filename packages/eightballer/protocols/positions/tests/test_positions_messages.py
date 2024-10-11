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

"""Test messages module for positions protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.protocols.positions.custom_types import (
    Position,
    ErrorCode,
    Positions,
    PositionSide,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessagePositions(BaseProtocolMessagesTestCase):
    """Test for the 'positions' protocol message."""

    MESSAGE_CLASS = PositionsMessage

    def build_messages(self) -> List[PositionsMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            PositionsMessage(
                performative=PositionsMessage.Performative.GET_ALL_POSITIONS,
                exchange_id="some str",
                params={"some str": b"some_bytes"},
                side=PositionSide(0),
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.GET_POSITION,
                position_id="some str",
                exchange_id="some str",
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.ALL_POSITIONS,
                positions=Positions(**load_data("Positions")),  # check it please!
                exchange_id="some str",
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.POSITION,
                position=Position(**load_data("Position")),  # check it please!
                exchange_id="some str",
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
