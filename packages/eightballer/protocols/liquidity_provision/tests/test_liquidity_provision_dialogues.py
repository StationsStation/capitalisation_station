# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

"""Test dialogues module for liquidity_provision protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase

from packages.eightballer.protocols.liquidity_provision.message import (
    LiquidityProvisionMessage,
)
from packages.eightballer.protocols.liquidity_provision.dialogues import (
    LiquidityProvisionDialogue,
    BaseLiquidityProvisionDialogues,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestDialoguesLiquidityProvision(BaseProtocolDialoguesTestCase):
    """Test for the 'liquidity_provision' protocol dialogues."""

    MESSAGE_CLASS = LiquidityProvisionMessage

    DIALOGUE_CLASS = LiquidityProvisionDialogue

    DIALOGUES_CLASS = BaseLiquidityProvisionDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = LiquidityProvisionDialogue.Role.LIQUIDITY_PROVIDER  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return {
            "performative": LiquidityProvisionMessage.Performative.ADD_LIQUIDITY,
            "pool_id": "some str",
            "token_ids": ("some str",),
            "amounts": (12,),
            "min_mint_amount": 12,
            "deadline": 12,
            "user_data": b"some_bytes",
            "exchange_id": "some str",
            "ledger_id": "some str",
        }
