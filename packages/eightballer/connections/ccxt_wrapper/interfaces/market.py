"""Implements the interface for market protocol."""

import os
import site
import importlib
from typing import cast

from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue

from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.markets.dialogues import MarketsDialogue, BaseMarketsDialogues
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.connections.ccxt_wrapper.interfaces.interface_base import BaseInterface


site_packages_path = site.getsitepackages()[0]
ccxt_path = os.path.join(site_packages_path, "ccxt")

ccxt_spec = importlib.util.spec_from_file_location(
    "ccxt", os.path.join(ccxt_path, "ccxt", "async_support", "__init__.py")
)
ccxt = importlib.util.module_from_spec(ccxt_spec)


def all_markets_from_api_call(api_call):
    """Convert an API call to a message."""

    def cast_to_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return value

    for market in api_call:
        for key, value in market.items():
            if key in {
                "tick_size",
                "taker_commission",
                "maker_commission",
                "strike",
                "min_trade_amount",
                "contract_size",
            }:
                market[key] = cast_to_float(value)

    return Markets(
        markets=[Market(**market) for market in api_call],
    )


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
            response_message = cast(
                Message | None,
                dialogue.reply(
                    performative=MarketsMessage.Performative.ALL_MARKETS,
                    target_message=message,
                    markets=all_markets_from_api_call(markets),
                    exchange_id=message.exchange_id,
                ),
            )
            connection.logger.debug(f"Fetched {len(markets)} markets for {message.exchange_id}")
        except ccxt.RequestTimeout:
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
