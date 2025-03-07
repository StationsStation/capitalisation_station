"""Implements the interface for the Ticker protocol."""

import os
import site
import importlib

from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.tickers.dialogues import TickersDialogue, BaseTickersDialogues
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.connections.ccxt_wrapper.interfaces.interface_base import BaseInterface


site_packages_path = site.getsitepackages()[0]
ccxt_path = os.path.join(site_packages_path, "ccxt")

ccxt_spec = importlib.util.spec_from_file_location(
    "ccxt", os.path.join(ccxt_path, "ccxt", "async_support", "__init__.py")
)
ccxt = importlib.util.module_from_spec(ccxt_spec)


def all_tickers_from_api_call(api_call):
    """Get all tickers from the exchange."""
    tickers = []
    for ticker in api_call.values():
        ticker["info"] = None
        # We skip markets with no bid or ask
        if not ticker.get("bid") or not ticker.get("ask"):
            continue
        tickers.append(Ticker(**ticker))
    return Tickers(tickers=tickers)


class TickerInterface(BaseInterface):
    """Interface for ticker protocol."""

    protocol_id = TickersMessage.protocol_id
    dialogue_class = TickersDialogue
    dialogues_class = BaseTickersDialogues

    async def get_all_tickers(
        self, message: TickersMessage, dialogue: TickersDialogue, connection
    ) -> TickersMessage | None:
        """Get all tickers from the exchange."""
        exchange = connection.exchanges[message.exchange_id]
        try:
            params = {}
            if message.params is not None:
                for key, value in message.params.items():
                    params[key] = value.decode()
            tickers = await exchange.fetch_tickers(params=params)
            tickers = all_tickers_from_api_call(tickers)
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.ALL_TICKERS,
                target_message=message,
                tickers=tickers,
                exchange_id=message.exchange_id,
            )
        except ccxt.RequestTimeout:
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.ERROR,
                target_message=message,
                error_code=TickersMessage.ErrorCode.API_ERROR,
                error_msg="The request has timed out.",
            )
        return response_message

    async def get_ticker(self, message: TickersMessage, dialogue: TickersDialogue, connection) -> TickersMessage | None:
        """Get a ticker from the exchange."""
        exchange = connection.exchanges[message.exchange_id]
        try:
            params = {}
            for key, value in message.params.items():
                params[key] = value.decode()
            ticker = await exchange.fetch_ticker(message.symbol, params=params)
            ticker = Ticker(**ticker)
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.TICKER,
                target_message=message,
                ticker=ticker,
            )
        except ccxt.RequestTimeout:
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.ERROR,
                target_message=message,
                code=TickersMessage.ErrorCode.API_ERROR,
                message="The request has timed out.",
            )
        return response_message
