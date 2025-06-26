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

"""Test dialogues module for orders protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.orders.dialogues import (
    OrdersDialogue,
    BaseOrdersDialogues,
)
from packages.eightballer.protocols.orders.custom_types import Order


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestDialoguesOrders(BaseProtocolDialoguesTestCase):
    """Test for the 'orders' protocol dialogues."""

    MESSAGE_CLASS = OrdersMessage

    DIALOGUE_CLASS = OrdersDialogue

    DIALOGUES_CLASS = BaseOrdersDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = OrdersDialogue.Role.AGENT  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return {
            "performative": OrdersMessage.Performative.CREATE_ORDER,
            "order": Order(**load_data("Order")),  # check it please!
            "exchange_id": "some str",
            "ledger_id": "some str",
        }
