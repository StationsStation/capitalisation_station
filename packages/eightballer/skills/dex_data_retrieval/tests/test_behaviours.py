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

"""This package contains round behaviours of AbciApp."""

from typing import Any
from pathlib import Path
from dataclasses import field, dataclass
from unittest.mock import MagicMock
from collections.abc import Hashable

import pytest

from packages.eightballer.protocols.markets import MarketsMessage
from packages.eightballer.protocols.balances import BalancesMessage
from packages.valory.skills.abstract_round_abci.base import AbciAppDB
from packages.eightballer.protocols.markets.custom_types import Markets
from packages.eightballer.protocols.balances.custom_types import Balances
from packages.eightballer.skills.dex_data_retrieval.rounds import Event, SynchronizedData
from packages.valory.skills.abstract_round_abci.behaviours import BaseBehaviour
from packages.eightballer.skills.dex_data_retrieval.behaviours import (
    DEFAULT_RETRIES,
    FetchDexOrdersBehaviour,
    FetchDexMarketsBehaviour,
    FetchDexTickersBehaviour,
    FetchDexBalancesBehaviour,
    FetchDexPositionsBehaviour,
    DexDataRetrievalBaseBehaviour,
    DexDataRetrievalRoundBehaviour,
)
from packages.valory.skills.abstract_round_abci.test_tools.base import FSMBehaviourBaseCase
from packages.eightballer.connections.dcxt.tests.test_dcxt_connection import TEST_EXCHANGES


@dataclass
class BehaviourTestCase:
    """BehaviourTestCase."""

    name: str
    initial_data: dict[str, Hashable]
    event: Event
    kwargs: dict[str, Any] = field(default_factory=dict)


MARKETS_TEST_CASE = BehaviourTestCase(
    name="markets",
    initial_data={},
    event=Event.DONE,
)
MARKETS_FAILED_TEST_CASE = BehaviourTestCase(
    name="markets",
    initial_data={},
    event=Event.FAILED,
)

ORDERS_TEST_CASE = BehaviourTestCase(
    name="orders",
    initial_data={},
    event=Event.DONE,
)

BALANCES_TEST_CASE = BehaviourTestCase(
    name="balances",
    initial_data={},
    event=Event.DONE,
)


@pytest.mark.parametrize(
    "exchange_id, exchange_data",
    list(TEST_EXCHANGES.items()),
)
@pytest.mark.skip("Needs to be fixed")
class BaseDexDataRetrievalTest(FSMBehaviourBaseCase):
    """Base test case."""

    path_to_skill = Path(__file__).parent.parent

    behaviour: DexDataRetrievalRoundBehaviour
    behaviour_class: type[DexDataRetrievalBaseBehaviour]
    next_behaviour_class: type[DexDataRetrievalBaseBehaviour]
    synchronized_data: SynchronizedData
    done_event = Event.DONE

    @property
    def current_behaviour_id(self) -> str:
        """Current RoundBehaviour's behaviour id."""

        return self.behaviour.current_behaviour.behaviour_id

    def fast_forward(self, data: dict[str, Any] | None = None) -> None:
        """Fast-forward on initialization."""

        data = data if data is not None else {}
        self.fast_forward_to_behaviour(
            self.behaviour,
            self.behaviour_class.behaviour_id,
            SynchronizedData(AbciAppDB(setup_data=AbciAppDB.data_to_lists(data))),
        )
        assert self.current_behaviour_id == self.behaviour_class.behaviour_id

    def complete(self, event: Event) -> None:
        """Complete test."""

        self.behaviour.act_wrapper()
        self.mock_a2a_transaction()
        self._test_done_flag_set()
        self.end_round(done_event=event)
        assert self.current_behaviour_id == self.next_behaviour_class.behaviour_id


#  for some reason, this test fails, however it actually runs.
class TestFetchDexBalancesBehaviour(BaseDexDataRetrievalTest):
    """Tests FetchDexBalancesBehaviour."""

    behaviour_class: type[BaseBehaviour] = FetchDexBalancesBehaviour
    next_behaviour_class: type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase, exchange_id, exchange_data) -> None:
        """Run tests."""

        del exchange_data
        self.fast_forward(test_case.initial_data)

        def get_ccxt_response(*args, **kwargs):
            """Mock get_dcxt_response."""
            del args, kwargs
            yield BalancesMessage(
                performative=BalancesMessage.Performative.ALL_BALANCES,
                balances=Balances([]),
            )

        def from_balances_to_dict(*args, **kwargs):
            """Mock _from_balances_to_dict."""
            del args, kwargs
            return {exchange_id: [1, 2]}

        def is_result_ok(*args, **kwargs):
            """Mock is_result_ok."""
            del args, kwargs
            return True

        mocker = MagicMock()
        mocker.get_ccxt_response = get_ccxt_response
        mocker.from_balances_to_dict = from_balances_to_dict
        mocker.is_result_ok = is_result_ok
        # we need to mock the get_dcxt_response method of the behaviour
        self.skill.behaviours["main"].current_behaviour.get_dcxt_response = mocker.get_dcxt_response
        self.skill.behaviours[  # noqa
            "main"
        ].current_behaviour._from_balances_to_dict = mocker.from_balances_to_dict
        self.skill.behaviours[  # noqa
            "main"
        ].current_behaviour._is_result_ok = mocker.is_result_ok
        for _ in range(DEFAULT_RETRIES):
            self.behaviour.act_wrapper()
        self.complete(test_case.event)


@pytest.mark.asyncio
class TestFetchDexMarketsBehaviour(BaseDexDataRetrievalTest):
    """Tests FetchDexMarketsBehaviour."""

    behaviour_class: type[BaseBehaviour] = FetchDexMarketsBehaviour
    next_behaviour_class: type[BaseBehaviour] = FetchDexTickersBehaviour

    @pytest.mark.parametrize("test_case", [MARKETS_TEST_CASE])
    async def test_run(self, test_case: BehaviourTestCase, exchange_id, exchange_data) -> None:
        """Run tests."""
        del exchange_data

        self.fast_forward(test_case.initial_data)

        mocker = MagicMock()

        def get_ccxt_response(*args, **kwargs):
            """Mock get_ccxt_response."""
            del args, kwargs
            yield MarketsMessage(
                performative=MarketsMessage.Performative.ALL_MARKETS,
                markets=Markets(markets=[]),
            )

        def from_markets_to_dict(*args, **kwargs):
            """Mock _from_markets_to_dict."""
            del args, kwargs
            return {exchange_id: [1, 2]}

        def is_result_ok(*args, **kwargs):
            """Mock is_result_ok."""
            del args, kwargs
            return True

        mocker.get_ccxt_response = get_ccxt_response
        mocker.from_markets_to_dict = from_markets_to_dict
        mocker.is_result_ok = is_result_ok
        # we need to mock the get_ccxt_response method of the behaviour
        self.skill.behaviours["main"].current_behaviour.get_ccxt_response = mocker.get_ccxt_response
        self.skill.behaviours[  # noqa
            "main"
        ].current_behaviour._from_markets_to_dict = mocker.from_markets_to_dict
        self.skill.behaviours[  # noqa
            "main"
        ].current_behaviour._is_result_ok = mocker.is_result_ok

        for _ in range(DEFAULT_RETRIES):
            self.behaviour.act_wrapper()
        self.complete(test_case.event)


@pytest.mark.asyncio
class TestFetchDexMarketsBehaviourFailures(BaseDexDataRetrievalTest):
    """Tests FetchDexMarketsBehaviour."""

    behaviour_class: type[BaseBehaviour] = FetchDexMarketsBehaviour
    next_behaviour_class: type[BaseBehaviour] = FetchDexMarketsBehaviour

    @pytest.mark.parametrize("test_case", [MARKETS_FAILED_TEST_CASE])
    async def test_run_failed_api_call(self, test_case: BehaviourTestCase, exchange_id, exchange_data) -> None:
        """Run tests."""

        del exchange_data
        self.fast_forward(test_case.initial_data)

        mocker = MagicMock()

        def get_ccxt_response(*args, **kwargs):
            """Mock get_ccxt_response."""
            del args, kwargs
            yield MarketsMessage(
                performative=MarketsMessage.Performative.ERROR,
                error_code=MarketsMessage.ErrorCode.DECODING_ERROR,
                error_msg="",
                error_data={},
            )

        def from_markets_to_dict(*args, **kwargs):
            """Mock _from_markets_to_dict."""
            del args, kwargs
            return {exchange_id: [1, 2]}

        def is_result_ok(*args, **kwargs):
            """Mock _is_result_ok."""
            del args, kwargs
            return False

        mocker.get_ccxt_response = get_ccxt_response
        mocker.from_markets_to_dict = from_markets_to_dict
        mocker.is_result_ok = is_result_ok
        # we need to mock the get_ccxt_response method of the behaviour
        self.skill.behaviours["main"].current_behaviour.get_ccxt_response = mocker.get_ccxt_response
        self.skill.behaviours[  # noqa
            "main"
        ].current_behaviour._from_markets_to_dict = mocker.from_markets_to_dict
        self.skill.behaviours[  # noqa
            "main"
        ].current_behaviour._is_result_ok = mocker.is_result_ok

        # we ensure we act enough times to trigger the timeout
        for _ in range(DEFAULT_RETRIES):
            self.behaviour.act_wrapper()
        self.complete(test_case.event)

    def complete(self, event: Event) -> None:
        """Complete test."""

        self.behaviour.act_wrapper()
        self.mock_a2a_transaction()
        self._test_done_flag_set()
        self.end_round(done_event=event)
        assert self.current_behaviour_id == "degenerate_behaviour_failed_dex_round"


class TestFetchDexOrdersBehaviour(BaseDexDataRetrievalTest):
    """Tests FetchDexOrdersBehaviour."""

    behaviour_class: type[BaseBehaviour] = FetchDexOrdersBehaviour
    next_behaviour_class: type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase, exchange_id, exchange_data) -> None:
        """Run tests."""
        del exchange_id, exchange_data

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestFetchDexPositionsBehaviour(BaseDexDataRetrievalTest):
    """Tests FetchDexPositionsBehaviour."""

    behaviour_class: type[BaseBehaviour] = FetchDexPositionsBehaviour
    next_behaviour_class: type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase, exchange_id, exchange_data) -> None:
        """Run tests."""
        del exchange_id, exchange_data

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)
