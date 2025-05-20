# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

"""This package contains a behaviours of the Derolas Automator."""

import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from aea.skills.behaviours import State, FSMBehaviour


# ruff: noqa: BLE001
# - BLE001: Do not catch blind exception: `Exception`


class DerolasautomatorabciappEvents(Enum):
    """Events for the fsm."""

    EPOCH_ENDED = "EPOCH_ENDED"
    ALREADY_CLAIMED = "ALREADY_CLAIMED"
    GAME_ON = "GAME_ON"
    MAX_DONATORS_REACHED = "MAX_DONATORS_REACHED"
    NO_TRIGGER = "NO_TRIGGER"
    ELIGIBLE_TO_DONATE = "ELIGIBLE_TO_DONATE"
    EPOCH_ONGOING = "EPOCH_ONGOING"
    WINDOW_CLOSED = "WINDOW_CLOSED"
    CLAIMED = "CLAIMED"
    DONATED = "DONATED"
    EPOCH_FINISHED = "EPOCH_FINISHED"
    EPOCH_END_NEAR = "EPOCH_END_NEAR"
    NOT_DONATED = "NOT_DONATED"
    TX_TIMEOUT = "TX_TIMEOUT"
    CANNOT_PLAY_GAME = "CANNOT_PLAY_GAME"
    TX_FAILED = "TX_FAILED"
    CLAIMABLE = "CLAIMABLE"
    ALREADY_DONATED = "ALREADY_DONATED"
    ERROR = "ERROR"


class DerolasautomatorabciappStates(Enum):
    """States for the fsm."""

    AWAITTRIGGERROUND = "awaittriggerround"
    CHECKREADYTODONATEROUND = "checkreadytodonateround"
    MAKECLAIMROUND = "makeclaimround"
    ENDEPOCHROUND = "endepochround"
    CHECKEPOCHROUND = "checkepochround"
    CHECKCLAIMROUND = "checkclaimround"
    DONATEROUND = "donateround"


class BaseState(State, ABC):
    """Base class for states."""

    _state: DerolasautomatorabciappStates = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._event = None
        self._is_done = False

    @abstractmethod
    def act(self) -> None:
        """Perfom the act."""
        raise NotImplementedError

    def is_done(self) -> bool:
        """Is done."""
        return self._is_done

    @property
    def event(self) -> str | None:
        """Current event."""
        return self._event

    @property
    def ledger_api_dialogues(self):
        """Ledger API Dialogues."""
        return self.context.ledger_api_dialogues

    @property
    def contract_api_dialogues(self):
        """Contract API Dialogues."""
        return self.context.contract_api_dialogues

    @property
    def derolas_staking_contract(self):
        """Derolas Staking contract."""
        return self.context.derolas_state.derolas_staking_contract

    @property
    def derolas_contract_address(self):
        """Derolas Staking contract."""
        return self.context.derolas_state.derolas_contract_address

    @property
    def base_ledger_api(self):
        """Base Ledger API."""
        return self.context.derolas_state.base_ledger_api


class AwaitTriggerRound(BaseState):
    """This class implements the behaviour of the state AwaitTriggerRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.AWAITTRIGGERROUND

    def act(self) -> None:
        """Perfom the act."""

        self._event = DerolasautomatorabciappEvents.NO_TRIGGER

        try:
            if self.can_play_game:
                self._event = DerolasautomatorabciappEvents.GAME_ON
            else:
                self._event = DerolasautomatorabciappEvents.CANNOT_PLAY_GAME
        except Exception as e:
            self.logger.info(f"Exception in {self.__class__.__name__}: {e}")
            self._event = DerolasautomatorabciappEvents.ERROR

        self._is_done = True

    @property
    def can_play_game(self):
        """Call "can_play_game" on Derolas contract."""

        return self.derolas_staking_contract.can_play_game(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )["bool"]


class CheckEpochRound(BaseState):
    """This class implements the behaviour of the state CheckEpochRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.CHECKEPOCHROUND

    def act(self) -> None:
        """Perfom the act."""

        self._event = DerolasautomatorabciappEvents.ERROR
        self._event = DerolasautomatorabciappEvents.CANNOT_PLAY_GAME
        self._event = DerolasautomatorabciappEvents.EPOCH_END_NEAR
        self._event = DerolasautomatorabciappEvents.EPOCH_FINISHED
        self._event = DerolasautomatorabciappEvents.EPOCH_ONGOING
        self._is_done = True


class EndEpochRound(BaseState):
    """This class implements the behaviour of the state EndEpochRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.ENDEPOCHROUND

    def act(self) -> None:
        """Perfom the act."""

        self._event = DerolasautomatorabciappEvents.ERROR
        self._event = DerolasautomatorabciappEvents.TX_TIMEOUT
        self._event = DerolasautomatorabciappEvents.TX_FAILED
        self._event = DerolasautomatorabciappEvents.EPOCH_ENDED
        self._is_done = True


class CheckReadyToDonateRound(BaseState):
    """This class implements the behaviour of the state CheckReadyToDonateRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.CHECKREADYTODONATEROUND

    def act(self) -> None:
        """Perfom the act."""

        self._event = DerolasautomatorabciappEvents.ERROR
        self._event = DerolasautomatorabciappEvents.CANNOT_PLAY_GAME
        self._event = DerolasautomatorabciappEvents.ALREADY_DONATED
        self._event = DerolasautomatorabciappEvents.MAX_DONATORS_REACHED
        self._event = DerolasautomatorabciappEvents.ELIGIBLE_TO_DONATE
        self._is_done = True


class DonateRound(BaseState):
    """This class implements the behaviour of the state DonateRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.DONATEROUND

    def act(self) -> None:
        """Perfom the act."""

        self._event = DerolasautomatorabciappEvents.ERROR
        self._event = DerolasautomatorabciappEvents.TX_TIMEOUT
        self._event = DerolasautomatorabciappEvents.TX_FAILED
        self._event = DerolasautomatorabciappEvents.DONATED
        self._is_done = True


class CheckClaimRound(BaseState):
    """This class implements the behaviour of the state CheckClaimRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.CHECKCLAIMROUND

    def act(self) -> None:
        """Perfom the act."""

        self._event = DerolasautomatorabciappEvents.ERROR
        self._event = DerolasautomatorabciappEvents.NOT_DONATED
        self._event = DerolasautomatorabciappEvents.ALREADY_CLAIMED
        self._event = DerolasautomatorabciappEvents.WINDOW_CLOSED
        self._event = DerolasautomatorabciappEvents.EPOCH_ONGOING
        self._event = DerolasautomatorabciappEvents.CLAIMABLE
        self._is_done = True


class MakeClaimRound(BaseState):
    """This class implements the behaviour of the state MakeClaimRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.MAKECLAIMROUND

    def act(self) -> None:
        """Perfom the act."""

        self._event = DerolasautomatorabciappEvents.ERROR
        self._event = DerolasautomatorabciappEvents.TX_TIMEOUT
        self._event = DerolasautomatorabciappEvents.TX_FAILED
        self._event = DerolasautomatorabciappEvents.CLAIMED
        self._is_done = True


class DerolasautomatorabciappFsmBehaviour(FSMBehaviour):
    """This class implements a simple Finite State Machine behaviour."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.register_state(DerolasautomatorabciappStates.AWAITTRIGGERROUND.value, AwaitTriggerRound(**kwargs), True)

        self.register_state(
            DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value, CheckReadyToDonateRound(**kwargs)
        )
        self.register_state(DerolasautomatorabciappStates.MAKECLAIMROUND.value, MakeClaimRound(**kwargs))
        self.register_state(DerolasautomatorabciappStates.ENDEPOCHROUND.value, EndEpochRound(**kwargs))
        self.register_state(DerolasautomatorabciappStates.CHECKEPOCHROUND.value, CheckEpochRound(**kwargs))
        self.register_state(DerolasautomatorabciappStates.CHECKCLAIMROUND.value, CheckClaimRound(**kwargs))
        self.register_state(DerolasautomatorabciappStates.DONATEROUND.value, DonateRound(**kwargs))

        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.CANNOT_PLAY_GAME,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.GAME_ON,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.NO_TRIGGER,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
            event=DerolasautomatorabciappEvents.ALREADY_CLAIMED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
            event=DerolasautomatorabciappEvents.CLAIMABLE,
            destination=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_ONGOING,
            destination=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
            event=DerolasautomatorabciappEvents.NOT_DONATED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
            event=DerolasautomatorabciappEvents.WINDOW_CLOSED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.CANNOT_PLAY_GAME,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_END_NEAR,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_FINISHED,
            destination=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_ONGOING,
            destination=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.ALREADY_DONATED,
            destination=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.CANNOT_PLAY_GAME,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.ELIGIBLE_TO_DONATE,
            destination=DerolasautomatorabciappStates.DONATEROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.MAX_DONATORS_REACHED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.DONATED,
            destination=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.TX_FAILED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.TX_TIMEOUT,
            destination=DerolasautomatorabciappStates.CHECKCLAIMROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_ENDED,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.TX_FAILED,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.TX_TIMEOUT,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.CLAIMED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.TX_FAILED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.TX_TIMEOUT,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )

    def setup(self) -> None:
        """Implement the setup."""
        self.context.logger.info("Setting up Derolasautomatorabciapp FSM behaviour.")

    def teardown(self) -> None:
        """Implement the teardown."""
        self.context.logger.info("Tearing down Derolasautomatorabciapp FSM behaviour.")

    def act(self) -> None:
        """Implement the act."""
        if self.current is None:
            self.context.logger.info("No state to act on.")
            self.terminate()
        self.context.logger.info(f"Entering {self.current}")
        super().act()

    def terminate(self) -> None:
        """Implement the termination."""
        os._exit(0)
