# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2025 zarathustra
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

"""Test dialogues module for asset_bridging protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import (
    AssetBridgingDialogue,
    BaseAssetBridgingDialogues,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import ErrorInfo, BridgeResult, BridgeRequest


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestDialoguesAssetBridging(BaseProtocolDialoguesTestCase):
    """Test for the 'asset_bridging' protocol dialogues."""

    MESSAGE_CLASS = AssetBridgingMessage

    DIALOGUE_CLASS = AssetBridgingDialogue

    DIALOGUES_CLASS = BaseAssetBridgingDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = AssetBridgingDialogue.Role.AGENT  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return dict(
            performative=AssetBridgingMessage.Performative.REQUEST_BRIDGE,
            request=BridgeRequest(**load_data("BridgeRequest")),  # check it please!
        )
