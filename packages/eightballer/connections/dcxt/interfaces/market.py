"""Implements the interface for market protocol."""

from typing import cast

from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.markets.dialogues import MarketsDialogue, BaseMarketsDialogues
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


class MarketInterface(BaseInterface):
    """Interface for market protocol."""

    protocol_id = MarketsMessage.protocol_id
    dialogue_class = MarketsDialogue
    dialogues_class = BaseMarketsDialogues

    async def get_all_markets(self, message: MarketsMessage, dialogue: Dialogue, connection) -> Message | None:
        """Get all markets from the exchange."""
        exchange = connection.exchanges[message.exchange_id]
        try:
            params = {}
            if message.currency is not None:
                params["currency"] = message.currency
            markets = await exchange.fetch_markets(params=params)
            response_message = dialogue.reply(
                performative=MarketsMessage.Performative.ALL_MARKETS,
                target_message=message,
                markets=markets,
                exchange_id=message.exchange_id,
            )
        except dcxt.exceptions.RequestTimeout:
            connection.logger.warning(f"Request timeout when fetching markets for {message.exchange_id}")
            response_message = cast(
                Message | None,
                dialogue.reply(
                    performative=MarketsMessage.Performative.ERROR,
                    target_message=message,
                    error_code=MarketsMessage.ErrorCode.DECODING_ERROR,
                    error_msg="Request timeout",
                    error_data={"msg": b"Request timeout"},
                ),
            )

        return response_message
