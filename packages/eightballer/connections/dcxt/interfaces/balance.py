"""
Base interface for balances protocol.
"""

from typing import Optional

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.balances.dialogues import BalancesDialogue, BaseBalancesDialogues
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


class BalanceInterface(BaseInterface):
    """
    Interface for balances protocol.
    """

    protocol_id = BalancesMessage.protocol_id
    dialogue_class = BalancesDialogue
    dialogues_class = BaseBalancesDialogues

    async def get_all_balances(
        self, message: BalancesMessage, dialogue: BalancesDialogue, connection
    ) -> Optional[BalancesMessage]:
        """
        Get all balances from the exchange.
        """
        exchange = connection.exchanges[f"{message.exchange_id}_{message.ledger_id}"]
        try:
            params = {}
            for key, value in message.params.items():
                params[key] = value.decode()
            balances = await exchange.fetch_balance(
                ledger_id=message.ledger_id, exchange_id=message.exchange_id, address=message.address, params=params
            )
            response_message = dialogue.reply(
                performative=BalancesMessage.Performative.ALL_BALANCES,
                target_message=message,
                balances=balances,
                exchange_id=message.exchange_id,
            )
            connection.logger.debug(f"Fetched {len(balances.balances)} balances for {message.exchange_id}")
        except dcxt.exceptions.RequestTimeout:
            connection.logger.warning(f"Request timeout when fetching balances for {message.exchange_id}")
            response_message = dialogue.reply(
                performative=BalancesMessage.Performative.ERROR,
                target_message=message,
                error_code=BalancesMessage.ErrorCode.API_ERROR,
                error_msg="Request timeout",
            )
        return response_message
