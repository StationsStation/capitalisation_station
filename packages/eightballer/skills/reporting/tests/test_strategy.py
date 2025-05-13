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
from copy import deepcopy
from typing import cast
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock

import pandas as pd
import pytest
from aea.test_tools.test_skill import BaseSkillTestCase

from packages.eightballer.skills.reporting.strategy import ReportingStrategy
from packages.eightballer.skills.reporting.behaviours import SYSTEM_TZ
from packages.eightballer.skills.reporting.tests.cases import (
    EXCHANGE_1,
    EXCHANGE_2,
    POSITION_CASE_1,
    POSITION_CASE_2,
    TEST_MARKET_NAME_1,
    TEST_MARKET_NAME_2,
)
from packages.eightballer.skills.reporting.tests.test_behaviour import ROOT_DIR


# pylint: disable=protected-access,too-few-public-methods,consider-using-with

DB_FILE = "test.db"


class TestOrder:
    """Test order class."""

    id: str = "test_id"
    exchange_id: str = "test_exchange_id"


@pytest.mark.skip("reason: Type str not supported for Order.symbol!")
class TestReportingStrategy(BaseSkillTestCase, ABC):
    """Base case for testing FSMBehaviour classes."""

    path_to_skill = Path(ROOT_DIR, "packages", "eightballer", "skills", "reporting")
    behaviour_name: str = None

    @classmethod
    def teardown_method(cls):
        """Teardown the test."""
        del cls
        if Path(DB_FILE).exists():
            Path(DB_FILE).unlink()

    def test_setup(self):
        """Test the setup method of the price_polling behaviour."""
        # operation
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()

    def test_from_position_to_pivot(self):
        """Test the act method of the price_polling behaviour."""
        # operation
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        positions = [POSITION_CASE_1]
        # we mock the get_marketsdata method
        strategy.get_markets_data = MagicMock(
            return_value=pd.DataFrame(
                [
                    [
                        2000,
                        "option",
                        datetime.now(tz=datetime.now().astimezone().tzinfo).isoformat(),
                        TEST_MARKET_NAME_1,
                        EXCHANGE_1,
                    ]
                ],
                columns=[
                    "strike",
                    "optionType",
                    "expiryDatetime",
                    "symbol",
                    "exchange_id",
                ],
            )
        )
        data = strategy.from_positions_to_pivot(positions, EXCHANGE_1)
        assert list(data.to_numpy()[0]) == [2000.0, "long", 1]

    def test_from_positions_to_pivot(self):
        """Test the act method of the price_polling behaviour."""
        # operation
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        positions = [POSITION_CASE_1, POSITION_CASE_2]
        # we mock the get_marketsdata method
        strategy.get_markets_data = MagicMock(
            return_value=pd.DataFrame(
                [
                    [
                        2000,
                        "call",
                        datetime.now(tz=SYSTEM_TZ).isoformat(),
                        TEST_MARKET_NAME_1,
                        EXCHANGE_1,
                    ],
                    [
                        2000,
                        "put",
                        datetime.now(tz=SYSTEM_TZ).isoformat(),
                        TEST_MARKET_NAME_2,
                        EXCHANGE_1,
                    ],
                ],
                columns=[
                    "strike",
                    "optionType",
                    "expiryDatetime",
                    "symbol",
                    "exchange_id",
                ],
            )
        )
        data = strategy.from_positions_to_pivot(positions, EXCHANGE_1)
        assert list(data.to_numpy()[0]) == [2000.0, "long", 1, 1]

    def test_nets_out_positions_in_pivot(self):
        """Test that the positions are netted out correctly."""
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        pos_1 = POSITION_CASE_1
        pos_2 = deepcopy(POSITION_CASE_1)
        pos_2.side = "short"
        pos_2.size = -pos_1.size
        positions = [pos_1, pos_2]
        # we mock the get_marketsdata method
        strategy.get_markets_data = MagicMock(
            return_value=pd.DataFrame(
                [
                    [
                        2000,
                        "option",
                        datetime.now(tz=SYSTEM_TZ).isoformat(),
                        TEST_MARKET_NAME_1,
                        EXCHANGE_1,
                    ]
                ],
                columns=[
                    "strike",
                    "optionType",
                    "expiryDatetime",
                    "symbol",
                    "exchange_id",
                ],
            )
        )
        data = strategy.from_positions_to_pivot(positions, EXCHANGE_1)
        assert list(data.to_numpy()[0]) == [2000.0, "flat", 0]

    def test_nets_out_positions_in_pivot_multiple(self):
        """Test that the positions are netted out correctly."""
        strategy = cast(ReportingStrategy, self.skill.skill_context.reporting_strategy)
        strategy.setup()
        pos_1 = POSITION_CASE_1
        pos_2 = deepcopy(POSITION_CASE_1)
        pos_2.side = "short"
        pos_2.size = -pos_1.size
        pos_2.exchange_id = EXCHANGE_2

        pos_3 = deepcopy(POSITION_CASE_1)
        pos_3.symbol = TEST_MARKET_NAME_2
        pos_3.side = "short"
        pos_3.size = pos_2.size

        pos_4 = deepcopy(pos_3)
        pos_4.exchange_id = EXCHANGE_2
        pos_4.side = "long"
        pos_4.size = pos_1.size

        positions = [pos_1, pos_2, pos_3, pos_4]
        # we mock the get_marketsdata method
        strategy.get_markets_data = MagicMock(
            return_value=pd.DataFrame(
                [
                    [1800, "call", "monday", TEST_MARKET_NAME_1, EXCHANGE_1],
                    [1900, "put", "tuesday", TEST_MARKET_NAME_2, EXCHANGE_1],
                    [1800, "call", "monday", TEST_MARKET_NAME_1, EXCHANGE_2],
                    [1900, "put", "tuesday", TEST_MARKET_NAME_2, EXCHANGE_2],
                ],
                columns=[
                    "strike",
                    "optionType",
                    "expiryDatetime",
                    "symbol",
                    "exchange_id",
                ],
            )
        )
        data = strategy.from_positions_to_pivot(positions, EXCHANGE_2)
        assert list(data.to_numpy()[0]) == [1800.0, "short", -1, 0]
        assert list(data.to_numpy()[1]) == [1900.0, "long", 0, 1]

        # we now check that the pivot is correct
        data = strategy.from_positions_to_pivot(positions, EXCHANGE_1)
        assert list(data.to_numpy()[0]) == [1800.0, "long", 1, 0]
        assert list(data.to_numpy()[1]) == [1900.0, "short", 0, -1]

        # we confirm that the netted out pivot is correct
        data = strategy.from_positions_to_pivot(positions)
        assert list(data.to_numpy()[0]) == [1800.0, "flat", 0, 0]
        assert list(data.to_numpy()[1]) == [1900.0, "flat", 0, 0]
