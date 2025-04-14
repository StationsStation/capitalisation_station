"""No Opportunity Round State."""

import asyncio
from typing import Any

from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseBehaviour


class NoOpportunityRound(BaseBehaviour):
    """This class implements the NoOpportunityRound state."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._is_done = False  # Initially, the state is not done
        self.started = False

    async def act(self) -> None:
        """Perform the action of the state."""
        if self.started:
            return
        self.strategy.error_count = 0
        await asyncio.sleep(self.strategy.cool_down_period)
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.strategy.state.current_period += 1
