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

"""Test dialogues module for balances protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase

from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.balances.dialogues import (
    BalancesDialogue,
    BaseBalancesDialogues,
)
from packages.eightballer.protocols.balances.custom_types import ErrorCode


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestDialoguesBalances(BaseProtocolDialoguesTestCase):
    """Test for the 'balances' protocol dialogues."""

    MESSAGE_CLASS = BalancesMessage

    DIALOGUE_CLASS = BalancesDialogue

    DIALOGUES_CLASS = BaseBalancesDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = BalancesDialogue.Role.AGENT  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return dict(
            performative=BalancesMessage.Performative.GET_ALL_BALANCES,
            params={"some str": b"some_bytes"},
            exchange_id="some str",
            ledger_id="some str",
            address="some str",
        )
