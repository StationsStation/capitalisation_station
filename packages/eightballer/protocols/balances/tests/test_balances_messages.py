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

"""Test messages module for balances protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
# pylint: disable=R1735
from typing import List

from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.balances.custom_types import Balance, Balances, ErrorCode
from packages.eightballer.protocols.balances.message import BalancesMessage

TEST_BALANCE = Balance(
    asset_id="some str",
    free=0.0,
    used=1.0,
    total=1.0,
)

TEST_BALANCES = Balances(balances=[TEST_BALANCE])


class TestMessageBalances(BaseProtocolMessagesTestCase):
    """Test for the 'balances' protocol message."""

    MESSAGE_CLASS = BalancesMessage

    def build_messages(self) -> List[BalancesMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            BalancesMessage(
                performative=BalancesMessage.Performative.GET_ALL_BALANCES,
                exchange_id="some str",
                params={"some str": b"some_bytes"},
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.GET_BALANCE,
                asset_id="some str",
                exchange_id="some str",
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.ALL_BALANCES,
                balances=TEST_BALANCES,
            ),
            BalancesMessage(performative=BalancesMessage.Performative.BALANCE, balance=TEST_BALANCE),
            BalancesMessage(
                performative=BalancesMessage.Performative.ERROR,
                error_code=ErrorCode(1),
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self) -> List[BalancesMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            BalancesMessage(
                performative=BalancesMessage.Performative.GET_ALL_BALANCES,
                # skip content: exchange_id
                params={"some str": b"some_bytes"},
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.GET_BALANCE,
                # skip content: asset_id
                exchange_id="some str",
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.ALL_BALANCES,
                # skip content: balances
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.BALANCE,
                # skip content: balance
            ),
            BalancesMessage(
                performative=BalancesMessage.Performative.ERROR,
                # skip content: error_code
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]
