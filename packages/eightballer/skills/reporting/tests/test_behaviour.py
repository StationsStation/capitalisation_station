# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 8baller
#   Copyright 2021-2023 Valory AG
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

"""Tests for valory/abstract_round_abci skill's behaviours."""

from abc import ABC
from typing import cast
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from aea.test_tools.test_skill import BaseSkillTestCase

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.skills.reporting.strategy import ReportingStrategy
from packages.eightballer.skills.reporting.behaviours import from_id_to_instrument_name, from_instrument_name_to_id
from packages.eightballer.protocols.orders.custom_types import OrderSide, OrderType


# pylint: disable=protected-access,too-few-public-methods,consider-using-with

DB_FILE = "test.db"

ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent


class TestOrder:
    """Test order class."""

    id: str = "test_id"
    exchange_id: str = "lyra"
    type: OrderType = OrderType.LIMIT
    side: OrderSide = OrderSide.BUY


class BaseReportingTestCase(BaseSkillTestCase, ABC):
    """Base case for testing FSMBehaviour classes."""

    path_to_skill = Path(ROOT_DIR, "packages", "eightballer", "skills", "reporting")
    behaviour_name: str = None

    def test_setup(self):
        """Test the setup method of the price_polling behaviour."""
        # operation
        behaviour = self.skill.behaviours[self.behaviour_name]
        behaviour.setup()

    @classmethod
    def teardown_method(cls):
        """Teardown the test."""
        del cls
        if Path(DB_FILE).exists():
            Path(DB_FILE).unlink()

    @pytest.mark.skip
    def test_act(self):
        """Test the act method of the price_polling behaviour."""
        # operation
        behaviour = self.skill.behaviours[self.behaviour_name]
        behaviour.setup()
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        behaviour.act()


class TestEodSetup(BaseReportingTestCase):
    """Test that the setup is correct."""

    behaviour_name = "eod_reporting"


@pytest.mark.skip("reason: Type str not supported for Order.symbol!")
class TestReconciliationSetup(BaseReportingTestCase):
    """Test that the setup is correct."""

    behaviour_name = "reconciliation_reporting"

    def test_creates_order_request(self):
        """We check that the reconcilliation behaviour puts a request on the order queue."""

        behaviour = self.skill.behaviours[self.behaviour_name]
        behaviour.setup()
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        # we need to patch in the result from the strategy get_orders
        mocker = MagicMock()
        mocker.get_orders.return_value = [TestOrder]
        strategy.get_orders = mocker.get_orders

        behaviour.act()
        msg = self.get_message_from_outbox()
        has_attributes, error_str = self.message_has_attributes(
            actual_message=msg,
            message_type=OrdersMessage,
            performative=OrdersMessage.Performative.GET_ORDER,
            to=str(DCXT_PUBLIC_ID),
            sender=str(self.skill.public_id),
        )
        assert msg.order.exchange_id == TestOrder.exchange_id
        assert has_attributes, error_str

        # we check we also get the settlements.
        msg = self.get_message_from_outbox()
        has_attributes, error_str = self.message_has_attributes(
            actual_message=msg,
            message_type=OrdersMessage,
            performative=OrdersMessage.Performative.GET_SETTLEMENTS,
            to=str(DCXT_PUBLIC_ID),
            sender=str(self.skill.public_id),
        )

    @pytest.mark.parametrize(
        ("in_string", "out_string"),
        [
            ("ETH/USD:ETH-231027-2000-C", "ETH-27OCT23-2000-C"),
            ("ETH/USD:ETH-231027-2000-P", "ETH-27OCT23-2000-P"),
            ("ETH/USD:ETH-230825-1500-P", "ETH-25AUG23-1500-P"),
        ],
    )
    def test_from_instrument_name_to_id(self, in_string, out_string):
        """Test if it is possible to convert from instrument to id."""
        assert from_instrument_name_to_id(in_string) == out_string

    @pytest.mark.parametrize(
        ("in_string", "out_string"),
        [
            ("ETH-27OCT23-2000-C", "ETH/USD:ETH-231027-2000-C"),
            ("ETH-27OCT23-2000-P", "ETH/USD:ETH-231027-2000-P"),
            ("ETH-25AUG23-1500-P", "ETH/USD:ETH-230825-1500-P"),
            ("ETH-30SEP22-1300-P", "ETH/USD:ETH-220930-1300-P"),
            ("ETH-11AUG23-1750-P", "ETH/USD:ETH-230811-1750-P"),
            ("ETH-4AUG23-1900-C", "ETH/USD:ETH-230804-1900-C"),
            ("ETH-4AUG23-1950-C", "ETH/USD:ETH-230804-1950-C"),
            ("ETH-2AUG23-1825-C", "ETH/USD:ETH-230802-1825-C"),
            ("ETH-2AUG23-1850-C", "ETH/USD:ETH-230802-1850-C"),
            ("ETH-28JUL23-1850-P", "ETH/USD:ETH-230728-1850-P"),
            ("ETH-28JUL23-2000-C", "ETH/USD:ETH-230728-2000-C"),
            ("ETH-28JUL23-2100-C", "ETH/USD:ETH-230728-2100-C"),
            ("ETH-30JUN23-2000-C", "ETH/USD:ETH-230630-2000-C"),
            ("ETH-16JUN23-1950-C", "ETH/USD:ETH-230616-1950-C"),
            ("ETH-27JAN23-1300-P", "ETH/USD:ETH-230127-1300-P"),
            ("ETH-30DEC22-1300-P", "ETH/USD:ETH-221230-1300-P"),
            ("ETH-18NOV22-1400-P", "ETH/USD:ETH-221118-1400-P"),
            ("ETH-11NOV22-1400-P", "ETH/USD:ETH-221111-1400-P"),
            ("ETH-9NOV22-1500-P", "ETH/USD:ETH-221109-1500-P"),
            ("ETH-4NOV22-1250-P", "ETH/USD:ETH-221104-1250-P"),
            ("ETH-24OCT22-1325-C", "ETH/USD:ETH-221024-1325-C"),
        ],
    )
    def test_from_id_to_instrument_name(self, in_string, out_string):
        """Test if it is possible to convert from id to instrument."""
        assert from_id_to_instrument_name(in_string) == out_string
