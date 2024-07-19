# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
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

"""Test dialogues module for positions protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase

from packages.eightballer.protocols.positions.custom_types import PositionSide
from packages.eightballer.protocols.positions.dialogues import (
    PositionsDialogue,
    PositionsDialogues,
)
from packages.eightballer.protocols.positions.message import PositionsMessage


class TestDialoguesPositions(BaseProtocolDialoguesTestCase):
    """Test for the 'positions' protocol dialogues."""

    MESSAGE_CLASS = PositionsMessage

    DIALOGUE_CLASS = PositionsDialogue

    DIALOGUES_CLASS = PositionsDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = PositionsDialogue.Role.AGENT  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return dict(
            performative=PositionsMessage.Performative.GET_ALL_POSITIONS,
            exchange_id="some str",
            params={"some str": b"some_bytes"},
            side=PositionSide.LONG,
        )
