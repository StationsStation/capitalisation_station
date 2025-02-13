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

"""Test messages module for liquidity_provision protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.liquidity_provision.message import (
    LiquidityProvisionMessage,
)
from packages.eightballer.protocols.liquidity_provision.custom_types import ErrorCode


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageLiquidityProvision(BaseProtocolMessagesTestCase):
    """Test for the 'liquidity_provision' protocol message."""

    MESSAGE_CLASS = LiquidityProvisionMessage

    def build_messages(self) -> list[LiquidityProvisionMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            LiquidityProvisionMessage(
                performative=LiquidityProvisionMessage.Performative.ADD_LIQUIDITY,
                pool_id="some str",
                token_ids=("some str",),
                amounts=(12,),
                min_mint_amount=12,
                deadline=12,
                user_data=b"some_bytes",
                exchange_id="some str",
                ledger_id="some str",
            ),
            LiquidityProvisionMessage(
                performative=LiquidityProvisionMessage.Performative.REMOVE_LIQUIDITY,
                pool_id="some str",
                token_ids=("some str",),
                burn_amount=12,
                min_amounts=(12,),
                deadline=12,
                user_data=b"some_bytes",
                exchange_id="some str",
                ledger_id="some str",
            ),
            LiquidityProvisionMessage(
                performative=LiquidityProvisionMessage.Performative.QUERY_LIQUIDITY,
                pool_id="some str",
                exchange_id="some str",
                ledger_id="some str",
            ),
            LiquidityProvisionMessage(
                performative=LiquidityProvisionMessage.Performative.LIQUIDITY_ADDED,
                pool_id="some str",
                minted_tokens=12,
            ),
            LiquidityProvisionMessage(
                performative=LiquidityProvisionMessage.Performative.LIQUIDITY_REMOVED,
                pool_id="some str",
                received_amounts=(12,),
            ),
            LiquidityProvisionMessage(
                performative=LiquidityProvisionMessage.Performative.LIQUIDITY_STATUS,
                pool_id="some str",
                current_liquidity=12,
                available_tokens=(12,),
            ),
            LiquidityProvisionMessage(
                performative=LiquidityProvisionMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                description="some str",
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
