"""This package contains round behaviours of AbciApp."""

from typing import Any
from pathlib import Path
from dataclasses import field, dataclass
from collections.abc import Hashable

import pytest

from packages.eightballer.skills.abstract_round_abci.base import AbciAppDB
from packages.eightballer.skills.dex_data_retrieval.rounds import Event, SynchronizedData
from packages.eightballer.skills.chained_dex_app.behaviours import DexDataAbciAppConsensusBehaviour
from packages.eightballer.skills.dex_data_retrieval.behaviours import FetchDexPositionsBehaviour
from packages.eightballer.skills.abstract_round_abci.behaviours import BaseBehaviour
from packages.eightballer.skills.abstract_round_abci.test_tools.base import FSMBehaviourBaseCase


TEST_EXCHANGE = "lyra"


@dataclass
class BehaviourTestCase:
    """BehaviourTestCase."""

    name: str
    initial_data: dict[str, Hashable]
    event: Event
    kwargs: dict[str, Any] = field(default_factory=dict)


TEST_CASE = BehaviourTestCase(
    name="base",
    initial_data={},
    event=Event.DONE,
)


class BaseChainedDexTest(FSMBehaviourBaseCase):
    """Base test case."""

    path_to_skill = Path(__file__).parent.parent

    behaviour: DexDataAbciAppConsensusBehaviour
    behaviour_class: type[BaseBehaviour]
    next_behaviour_class: type[BaseBehaviour]
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


class TestChained(BaseChainedDexTest):
    """Tests FetchDexPositionsBehaviour."""

    behaviour_class: type[BaseBehaviour] = FetchDexPositionsBehaviour
    next_behaviour_class: type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [TEST_CASE])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
