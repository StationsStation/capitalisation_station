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

"""Test dialogues module for spot_asset protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase

from packages.eightballer.protocols.spot_asset.message import SpotAssetMessage
from packages.eightballer.protocols.spot_asset.dialogues import (
    SpotAssetDialogue,
    BaseSpotAssetDialogues,
)
from packages.eightballer.protocols.spot_asset.custom_types import ErrorCode


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestDialoguesSpotAsset(BaseProtocolDialoguesTestCase):
    """Test for the 'spot_asset' protocol dialogues."""

    MESSAGE_CLASS = SpotAssetMessage

    DIALOGUE_CLASS = SpotAssetDialogue

    DIALOGUES_CLASS = BaseSpotAssetDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = SpotAssetDialogue.Role.AGENT  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return dict(
            performative=SpotAssetMessage.Performative.GET_SPOT_ASSET,
            name="some str",
            exchange_id="some str",
        )
