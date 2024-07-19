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

"""Test dialogues module for tickers protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
# pylint: disable=R1735
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase
import pytest

from packages.eightballer.protocols.tickers.dialogues import TickersDialogue, TickersDialogues
from packages.eightballer.protocols.tickers.message import TickersMessage


@pytest.mark.skip("Not implemented yet")
class TestDialoguesTickers(BaseProtocolDialoguesTestCase):
    """Test for the 'tickers' protocol dialogues."""

    MESSAGE_CLASS = TickersMessage

    DIALOGUE_CLASS = TickersDialogue

    DIALOGUES_CLASS = TickersDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = TickersDialogue.Role.AGENT  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return dict(
            performative=TickersMessage.Performative.GET_ALL_TICKERS,
            exchange_id="some str",
            params={"some str": b"some_bytes"},
        )
