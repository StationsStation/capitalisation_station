# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""This package contains the tests for rounds of HelloWorld."""

from typing import Any
from dataclasses import field, dataclass
from collections.abc import Mapping, Callable, Hashable

import pytest

from packages.valory.skills.abstract_round_abci.base import AbstractRound, BaseTxPayload
from packages.eightballer.skills.dex_data_retrieval.rounds import (
    Event,
    SynchronizedData,
    FetchDexOrdersRound,
    FetchDexMarketsRound,
    FetchDexBalancesRound,
    FetchDexPositionsRound,
)
from packages.valory.skills.abstract_round_abci.test_tools.rounds import BaseRoundTestClass


@dataclass
class RoundTestCase:
    """RoundTestCase."""

    name: str
    initial_data: dict[str, Hashable]
    payloads: Mapping[str, BaseTxPayload]
    final_data: dict[str, Hashable]
    event: Event
    synchronized_data_attr_checks: list[Callable] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)


MAX_PARTICIPANTS: int = 4


class BaseHelloWorldRoundTest(BaseRoundTestClass):
    """Base test class for HelloWorld rounds."""

    round_cls: type[AbstractRound]
    synchronized_data: SynchronizedData
    _synchronized_data_class = SynchronizedData
    _event_class = Event

    def run_test(self, test_case: RoundTestCase) -> None:
        """Run the test."""

        self.synchronized_data.update(**test_case.initial_data)

        test_round = self.round_cls(
            synchronized_data=self.synchronized_data,
        )

        self._complete_run(
            self._test_round(
                test_round=test_round,
                round_payloads=test_case.payloads,
                synchronized_data_update_fn=lambda sync_data, _: sync_data.update(**test_case.final_data),
                synchronized_data_attr_checks=test_case.synchronized_data_attr_checks,
                exit_event=test_case.event,
                **test_case.kwargs,  # varies per BaseRoundTestClass child
            )
        )

    def _test_round(self, test_round: AbstractRound, **kwargs: Any) -> AbstractRound:
        """Test the round."""
        return test_round.run(**kwargs)


class TestFetchDexBalancesRound(BaseHelloWorldRoundTest):
    """Tests for FetchDexBalancesRound."""

    round_class = FetchDexBalancesRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestFetchDexMarketsRound(BaseHelloWorldRoundTest):
    """Tests for FetchDexMarketsRound."""

    round_class = FetchDexMarketsRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestFetchDexOrdersRound(BaseHelloWorldRoundTest):
    """Tests for FetchDexOrdersRound."""

    round_class = FetchDexOrdersRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestFetchDexPositionsRound(BaseHelloWorldRoundTest):
    """Tests for FetchDexPositionsRound."""

    round_class = FetchDexPositionsRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)
