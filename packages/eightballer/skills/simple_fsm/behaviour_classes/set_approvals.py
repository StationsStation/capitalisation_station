"""Collect data round behaviour class."""

from typing import TYPE_CHECKING
from datetime import datetime, timedelta
from collections.abc import Generator

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.skills.simple_fsm.strategy import TZ, ArbitrageStrategy
from packages.eightballer.protocols.approvals.message import ApprovalsMessage
from packages.eightballer.protocols.approvals.custom_types import Approval
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseConnectionRound


if TYPE_CHECKING:
    from aea.protocols.dialogue.base import Dialogue as BaseDialogue


APPROVALS_TIMEOUT_SECONDS = 120
DEFAULT_ENCODING = "utf-8"


class SetApprovalsRound(BaseConnectionRound):
    """This class implements the CollectDataRound state."""

    matching_round = "setapprovals"
    attempts = 0
    started = False

    supported_protocols = {
        ApprovalsMessage.protocol_id: [],
    }

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy

    def _handle_startup(self) -> None:
        """Handle the startup of the state."""
        self.started = True
        self.started_at = datetime.now(tz=TZ)
        self.context.logger.info(f"Starting approvals collection. at {self.started_at}")
        self.pending_approvals: list[BaseDialogue] = []
        for k in self.supported_protocols:
            self.supported_protocols[k] = []

        for exchange_id, ledgers in self.strategy.dexs.items():
            for ledger_id in ledgers:
                for asset in [self.strategy.strategy_init_kwargs.get(i) for i in ["base_asset", "quote_asset"]]:
                    self.context.logger.info(f"Sending approval for {asset} on {exchange_id}")
                    approval_request = self.submit_msg(
                        protocol_performative=ApprovalsMessage.Performative.SET_APPROVAL,
                        connection_id=DCXT_PUBLIC_ID,
                        approval=Approval(
                            exchange_id=exchange_id,
                            ledger_id=ledger_id,
                            amount=2**256 - 1,
                            asset_id=asset,
                            is_eoa=True,
                        ),
                    )
                    self.pending_approvals.append(approval_request)

    def act(self) -> Generator:
        """Perform the action of the state."""

        if not self.started:
            self._handle_startup()
            return None

        total_expected_responses = len(self.pending_approvals)
        current_responses = sum(len(i) for i in self.supported_protocols.values())
        if any(
            [
                total_expected_responses != current_responses,
            ]
        ):
            msg = (
                "Waiting for all messages to be received. "
                + f"{current_responses}/{total_expected_responses}"
                + "received."
            )
            self.context.logger.debug(msg)
            if not datetime.now(tz=TZ) - timedelta(seconds=APPROVALS_TIMEOUT_SECONDS) < self.started_at:
                self.context.logger.error("Timeout waiting for messages.")
                self.started = False
                return self._handle_error()
            return None

        errors = []
        for request in self.pending_approvals:
            self.context.logger.debug(f"Request: {request}")

        if errors:
            self.context.logger.error("Error getting tickers for all exchanges")
            self._handle_error()
            return None

        self.context.logger.info("Approvals verification complete.")
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.attempts = 0
        return None

    def _handle_error(self, attempts=1) -> Generator[None, None, bool]:
        self.attempts += 1
        if self.attempts >= attempts:
            self.context.logger.error("Max attempts reached. Giving up.")
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
