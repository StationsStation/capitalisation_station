# -*- coding: utf-8 -*-
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

"""Test messages module for balances protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.balances.custom_types import (
    Balance,
    Balances,
    ErrorCode,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageBalances(BaseProtocolMessagesTestCase):
    """Test for the 'balances' protocol message."""

    MESSAGE_CLASS = BalancesMessage

    def build_messages(self) -> List[BalancesMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            BalancesMessage(
                performative=BalancesMessage.Performative.GET_ALL_BALANCES,
                params={"some str": b"some_bytes"},
                exchange_id="some str",
                ledger_id="some str",
                address="some str",
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.GET_BALANCE,
                asset_id="some str",
                exchange_id="some str",
                ledger_id="some str",
                address="some str",
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.ALL_BALANCES,
                balances=Balances(**load_data("Balances")),  # check it please!
                ledger_id="some str",
                exchange_id="some str",
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.BALANCE,
                balance=Balance(**load_data("Balance")),  # check it please!
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
