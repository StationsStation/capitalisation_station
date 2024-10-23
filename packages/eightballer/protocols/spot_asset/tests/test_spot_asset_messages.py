# -*- coding: utf-8 -*-
#                                                                             --
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
#                                                                             --

"""Test messages module for spot_asset protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.spot_asset.message import SpotAssetMessage
from packages.eightballer.protocols.spot_asset.custom_types import Decimal, ErrorCode


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageSpotAsset(BaseProtocolMessagesTestCase):
    """Test for the 'spot_asset' protocol message."""

    MESSAGE_CLASS = SpotAssetMessage

    def build_messages(self) -> List[SpotAssetMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            SpotAssetMessage(
                performative=SpotAssetMessage.Performative.GET_SPOT_ASSET,
                name="some str",
                exchange_id="some str",
            ),
            SpotAssetMessage(
                performative=SpotAssetMessage.Performative.SPOT_ASSET,
                name="some str",
                total=Decimal(**load_data("Decimal")),  # check it please!
                free=Decimal(**load_data("Decimal")),  # check it please!
                available_without_borrow=Decimal(**load_data("Decimal")),  # check it please!
                usd_value=Decimal(**load_data("Decimal")),
                decimal=Decimal(**load_data("Decimal")),
            ),
            SpotAssetMessage(
                performative=SpotAssetMessage.Performative.GET_SPOT_ASSETS,
                exchange_id="some str",
            ),
            SpotAssetMessage(
                performative=SpotAssetMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
            ),
            SpotAssetMessage(
                performative=SpotAssetMessage.Performative.END,
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
