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

"""Test messages module for positions protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import List

import pytest
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.protocols.positions.custom_types import Position, ErrorCode, Positions, PositionSide


TEST_POSITION = {
    "info": {
        "vega": "-2.00738",
        "total_profit_loss": "0.019502577",
        "theta": "0.91107",
        "size": "-1.0",
        "settlement_price": "0.015945",
        "realized_profit_loss": "0.0",
        "open_orders_margin": "0.0",
        "mark_price": "0.017497",
        "maintenance_margin": "0.092497423",
        "kind": "option",
        "instrument_name": "ETH-25AUG23-2100-C",
        "initial_margin": "0.117497423",
        "index_price": "1882.4",
        "gamma": "-0.00122",
        "floating_profit_loss_usd": "34.968581",
        "floating_profit_loss": "-0.001552855",
        "direction": "sell",
        "delta": "-0.23791",
        "average_price_usd": "67.90573",
        "average_price": "0.037",
    },
    "id": None,
    "symbol": "ETH/USD:ETH-230825-2100-C",
    "timestamp": 1689243067080,
    "datetime": "2023-07-13T10:11:07.080Z",
    "lastUpdateTimestamp": None,
    "initialMargin": 0.117497423,
    "initialMarginPercentage": None,
    "maintenanceMargin": 0.092497423,
    "maintenanceMarginPercentage": None,
    "entryPrice": 0.037,
    "notional": None,
    "leverage": None,
    "unrealizedPnl": -0.001552855,
    "contracts": None,
    "contractSize": 1.0,
    "marginRatio": None,
    "liquidationPrice": None,
    "markPrice": 0.017497,
    "lastPrice": None,
    "collateral": None,
    "marginMode": None,
    "side": "short",
    "percentage": None,
}


@pytest.mark.skip("Not implemented yet")
class TestMessagePositions(BaseProtocolMessagesTestCase):
    """Test for the 'positions' protocol message."""

    MESSAGE_CLASS = PositionsMessage

    def build_messages(self) -> List[PositionsMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            PositionsMessage(
                performative=PositionsMessage.Performative.GET_ALL_POSITIONS,
                exchange_id="some str",
                params={"some str": b"some_bytes"},
                side=PositionSide.LONG,
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.GET_POSITION,
                position_id="some str",
                exchange_id="some str",
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.ALL_POSITIONS,
                positions=Positions(positions=[]),  # check it please!
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.POSITION,
                position=Position.from_api_call(TEST_POSITION),  # check it please!
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.ERROR,
                error_code=ErrorCode.API_ERROR,  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self) -> List[PositionsMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            PositionsMessage(
                performative=PositionsMessage.Performative.GET_ALL_POSITIONS,
                # skip content: exchange_id
                params={"some str": b"some_bytes"},
                side=PositionSide.LONG,
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.GET_POSITION,
                # skip content: position_id
                exchange_id="some str",
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.ALL_POSITIONS,
                # skip content: positions
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.POSITION,
                # skip content: position
            ),
            PositionsMessage(
                performative=PositionsMessage.Performative.ERROR,
                # skip content: error_code
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]
