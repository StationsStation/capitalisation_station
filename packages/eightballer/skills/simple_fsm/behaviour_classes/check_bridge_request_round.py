"""Collect data round behaviour class."""

import time
from collections.abc import Generator

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.skills.simple_fsm.strategy import ArbitrageStrategy
from packages.eightballer.protocols.approvals.message import ApprovalsMessage
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseConnectionRound
from packages.eightballer.skills.simple_fsm.strategy import InProgressBridgeRequest

AWAITING_INITIAL_BRIDGE_RESULT = object()
APPROVALS_TIMEOUT_SECONDS = 120
DEFAULT_ENCODING = "utf-8"


class CheckBridgeRequestRound(BaseConnectionRound):
    """This class implements the CheckBridgeRequestRound state."""

    matching_round = "checkbridgerequestround"
    attempts = 0
    started = False

    supported_protocols = {
        AssetBridgingMessage.protocol_id: [],
    }

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy

    def act(self) -> None:
        """Perform the action of the state."""

        while self.strategy.state.bridge_requests:
            request = self.strategy.state.bridge_requests.popleft()
            self.submit_msg(
                protocol_performative=AssetBridgingMessage.Performative.REQUEST_BRIDGE,
                connection_id=DCXT_PUBLIC_ID,
                request=request,
            )
            self.context.logger.info("Submitted bridge request.", extra={"request": request})
            entry = InProgressBridgeRequest(payload=AWAITING_INITIAL_BRIDGE_RESULT)
            self.strategy.state.bridge_requests_in_progress[request.request_id] = entry

        now = time.monotonic()
        for rid, entry in tuple(self.strategy.state.bridge_requests_in_progress.items()):
            if  now - entry.ts > self.strategy.bridge_request_timeout:
                self.strategy.state.bridge_requests_in_progress.pop(rid)
                self.context.logger.warning(f"Bridge request {rid} timed out after {now - entry.ts:.1f}s: {entry}")
                # TODO: remove: we won't ever use THIS bridge again if no completion

        for entry in self.strategy.state.bridge_requests_in_progress.values():
            if entry.payload is AWAITING_INITIAL_BRIDGE_RESULT:
                continue
            self.submit_msg(
                protocol_performative=AssetBridgingMessage.Performative.REQUEST_STATUS,
                connection_id=DCXT_PUBLIC_ID,
                result=entry.payload,
            )
            self.context.logger.info("Submitted bridge request status.", extra={"result": entry.payload})

        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.attempts = 0

    def _handle_error(self, attempts=1) -> Generator[None, None, bool]:
        self.attempts += 1
        if self.attempts >= attempts:
            self.context.logger.error(f"Max retry attempts ({self.attempts}) reached.")
            self._event = ArbitrageabciappEvents.TIMEOUT
            self._is_done = True
            return False
        return True

    def _validate_approval_msg(self, approval: ApprovalsMessage) -> bool:
        """Validate the ticker message."""
        msg = f"This method is not implemented yet. {approval}"
        raise NotImplementedError(msg)

    def setup(self) -> None:
        """Setup the state."""
        self.started = False
        self._is_done = False
        self._event = ArbitrageabciappEvents.TIMEOUT
        self.attempts = 0
        super().setup()
