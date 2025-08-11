# ------------------------------------------------------------------------------
#
#   Copyright 2022-2023 Valory AG
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

"""This package contains round behaviours of DummyAbciApp."""

from abc import ABC
from typing import cast
from collections import deque
from collections.abc import Generator

from packages.eightballer.skills.abstract_round_abci.base import AbstractRound
from packages.eightballer.skills.abstract_round_abci.common import (
    RandomnessBehaviour,
    SelectKeeperBehaviour,
)
from packages.eightballer.skills.abstract_round_abci.behaviours import (
    BaseBehaviour,
    AbstractRoundBehaviour,
)
from packages.eightballer.skills.abstract_round_abci.tests.data.dummy_abci.models import (
    Params,
)
from packages.eightballer.skills.abstract_round_abci.tests.data.dummy_abci.rounds import (
    DummyAbciApp,
    DummyFinalRound,
    SynchronizedData,
    DummyStartingRound,
    DummyRandomnessRound,
    DummyKeeperSelectionRound,
)
from packages.eightballer.skills.abstract_round_abci.tests.data.dummy_abci.payloads import (
    DummyFinalPayload,
    DummyStartingPayload,
    DummyRandomnessPayload,
    DummyKeeperSelectionPayload,
)


class DummyBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the common apps' skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class DummyStartingBehaviour(DummyBaseBehaviour):
    """DummyStartingBehaviour."""

    behaviour_id: str = "dummy_starting"
    matching_round: type[AbstractRound] = DummyStartingRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            content = "dummy"
            sender = self.context.agent_address
            payload = DummyStartingPayload(sender=sender, content=content)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class DummyRandomnessBehaviour(RandomnessBehaviour):
    """DummyRandomnessBehaviour."""

    behaviour_id: str = "dummy_randomness"
    matching_round: type[AbstractRound] = DummyRandomnessRound
    payload_class = DummyRandomnessPayload


class DummyKeeperSelectionBehaviour(SelectKeeperBehaviour):
    """DummyKeeperSelectionBehaviour."""

    behaviour_id: str = "dummy_keeper_selection"
    matching_round: type[AbstractRound] = DummyKeeperSelectionRound
    payload_class = DummyKeeperSelectionPayload

    @staticmethod
    def serialized_keepers(keepers: deque[str], keeper_retries: int = 1) -> str:
        """Get the keepers serialized."""
        if not keepers:
            return ""
        return keeper_retries.to_bytes(32, "big").hex() + "".join(keepers)

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            keepers = deque((self._select_keeper(),))
            payload = self.payload_class(self.context.agent_address, self.serialized_keepers(keepers))

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class DummyFinalBehaviour(DummyBaseBehaviour):
    """DummyFinalBehaviour."""

    behaviour_id: str = "dummy_final"
    matching_round: type[AbstractRound] = DummyFinalRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            content = True
            sender = self.context.agent_address
            payload = DummyFinalPayload(sender=sender, content=content)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class DummyRoundBehaviour(AbstractRoundBehaviour):
    """DummyRoundBehaviour."""

    initial_behaviour_cls = DummyStartingBehaviour
    abci_app_cls = DummyAbciApp
    behaviours: set[type[BaseBehaviour]] = {
        DummyFinalBehaviour,  # type: ignore
        DummyKeeperSelectionBehaviour,  # type: ignore
        DummyRandomnessBehaviour,  # type: ignore
        DummyStartingBehaviour,  # type: ignore
    }
