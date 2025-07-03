"""Base interface for approvals protocol."""

from typing import TYPE_CHECKING

import requests

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.approvals.message import ApprovalsMessage
from packages.eightballer.protocols.approvals.dialogues import (
    ApprovalsDialogue,
    BaseApprovalsDialogues,
)
from packages.eightballer.connections.dcxt.interfaces.interface_base import (
    BaseInterface,
)


if TYPE_CHECKING:
    from packages.eightballer.connections.dcxt.dcxt.defi_exchange import (
        BaseErc20Exchange,
    )


class ApprovalsInterface(BaseInterface):
    """Interface for approvals protocol."""

    protocol_id = ApprovalsMessage.protocol_id
    dialogue_class = ApprovalsDialogue
    dialogues_class = BaseApprovalsDialogues

    async def set_approval(
        self, message: ApprovalsMessage, dialogue: ApprovalsDialogue, connection
    ) -> ApprovalsMessage | None:
        """Get all approvals from the exchange."""

        approval = message.approval
        exchanges = connection.exchanges.get(approval.ledger_id)
        if exchanges is None:
            connection.logger.warning(f"Ledger {approval.ledger_id} not found.")
            return dialogue.reply(
                performative=ApprovalsMessage.Performative.ERROR,
                target_message=message,
                error_code=ApprovalsMessage.ErrorCode.UNKNOWN_LEDGER,
                error_msg="Ledger not found",
            )
        exchange: BaseErc20Exchange = exchanges.get(approval.exchange_id)
        if exchange is None:
            connection.logger.warning(f"Exchange {approval.exchange_id} not found.")
            return dialogue.reply(
                performative=ApprovalsMessage.Performative.ERROR,
                target_message=message,
                error_code=ApprovalsMessage.ErrorCode.UNKNOWN_EXCHANGE,
                error_msg="Exchange not found",
            )

        try:
            exchange.set_approval(
                asset_id=approval.asset_id,
                is_eoa=approval.is_eoa,
                amount=approval.amount,
            )
            response_message = dialogue.reply(
                performative=ApprovalsMessage.Performative.APPROVAL_RESPONSE,
                approval=message.approval,
                target_message=message,
            )

        except dcxt.exceptions.BadSymbol:
            connection.logger.warning(
                f"Bad symbol when fetching approvals for {message.approval.exchange_id}: {approval.asset_id}"
            )
            response_message = dialogue.reply(
                performative=ApprovalsMessage.Performative.ERROR,
                target_message=message,
                error_code=ApprovalsMessage.ErrorCode.UNKNOWN_ASSET,
                error_msg="Bad symbol",
            )
        except (
            dcxt.exceptions.RequestTimeout,
            dcxt.exceptions.ExchangeNotAvailable,
            dcxt.exceptions.RpcError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
        ):
            connection.logger.warning(f"Request timeout when fetching approvals for {message.approval.exchange_id}")
            response_message = dialogue.reply(
                performative=ApprovalsMessage.Performative.ERROR,
                target_message=message,
                error_code=ApprovalsMessage.ErrorCode.FAILED_TO_SET_APPROVAL,
                error_msg="Request timeout",
            )
        return response_message
