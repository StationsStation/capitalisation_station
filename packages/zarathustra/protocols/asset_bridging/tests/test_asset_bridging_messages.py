# -*- coding: utf-8 -*-
#                                                                             --
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
#                                                                             --

"""Test messages module for asset_bridging protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    ErrorInfo,
    BridgeResult,
    BridgeRequest,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageAssetBridging(BaseProtocolMessagesTestCase):
    """Test for the 'asset_bridging' protocol message."""

    MESSAGE_CLASS = AssetBridgingMessage

    def build_messages(self) -> List[AssetBridgingMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            AssetBridgingMessage(
                performative=AssetBridgingMessage.Performative.REQUEST_BRIDGE,
                request=BridgeRequest(**load_data("BridgeRequest")),  # check it please!
            ),
            AssetBridgingMessage(
                performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
                result=BridgeResult(0),  # check it please!
            ),
            AssetBridgingMessage(
                performative=AssetBridgingMessage.Performative.REQUEST_STATUS,
                result=BridgeResult(0),  # check it please!
            ),
            AssetBridgingMessage(
                performative=AssetBridgingMessage.Performative.ERROR,
                info=ErrorInfo(0),  # check it please!
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
