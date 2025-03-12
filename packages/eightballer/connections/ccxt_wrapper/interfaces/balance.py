"""Base interface for balances protocol."""

import ccxt
import requests

from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.balances.dialogues import BalancesDialogue, BaseBalancesDialogues
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.connections.ccxt_wrapper.interfaces.interface_base import BaseInterface


def all_balances_from_api_call(api_call):
    """Get all balances from the exchange."""
    for key in [
        "info",
        "free",
        "used",
        "total",
    ]:
        api_call.pop(key, None)

    balances = []
    for asset, data in [(asset, data) for asset, data in api_call.items() if data is not None]:
        data["asset_id"] = asset
        balances.append(Balance(**data, is_native=False))
    return Balances(balances=balances)


class BalanceInterface(BaseInterface):
    """Interface for balances protocol."""

    protocol_id = BalancesMessage.protocol_id
    dialogue_class = BalancesDialogue
    dialogues_class = BaseBalancesDialogues

    async def get_all_balances(
        self, message: BalancesMessage, dialogue: BalancesDialogue, connection
    ) -> BalancesMessage | None:
        """Get all balances from the exchange."""
        exchange = connection.exchanges[message.exchange_id]
        try:
            params = {}
            if message.params is not None:
                for key, value in message.params.items():
                    params[key] = value.decode()
            connection.logger.info(f"Fetching balances for {message.exchange_id} with params: {params}")
            balances = await exchange.fetch_balance(params=params)
            balances = all_balances_from_api_call(balances)
            response_message = dialogue.reply(
                performative=BalancesMessage.Performative.ALL_BALANCES,
                target_message=message,
                balances=balances,
                exchange_id=message.exchange_id,
                ledger_id=message.ledger_id,
            )
            connection.logger.info(f"Fetched {len(balances.balances)} balances for {message.exchange_id}")
        except (
            ccxt.RequestTimeout,
            ccxt.ExchangeNotAvailable,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
        ):
            connection.logger.warning(f"Request timeout when fetching balances for {message.exchange_id}")
            response_message = dialogue.reply(
                performative=BalancesMessage.Performative.ERROR,
                target_message=message,
                error_code=BalancesMessage.ErrorCode.API_ERROR,
                error_msg="Request timeout",
            )
        return response_message
