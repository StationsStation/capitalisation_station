"""
Implements the interface for the Ticker protocol.
"""
from typing import Optional

from ccxt import RequestTimeout

from packages.eightballer.connections.ccxt.interfaces.interface_base import BaseInterface
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.protocols.tickers.dialogues import BaseTickersDialogues, TickersDialogue
from packages.eightballer.protocols.tickers.message import TickersMessage


def all_tickers_from_api_call(api_call):
    """
    Get all tickers from the exchange.
    """
    tickers = []
    for ticker in api_call.values():
        tickers.append(Ticker(**ticker))
    return Tickers(tickers=tickers)


class TickerInterface(BaseInterface):
    """Interface for ticker protocol."""

    protocol_id = TickersMessage.protocol_id
    dialogue_class = TickersDialogue
    dialogues_class = BaseTickersDialogues

    async def get_all_tickers(
        self, message: TickersMessage, dialogue: TickersDialogue, connection
    ) -> Optional[TickersMessage]:
        """
        Get all tickers from the exchange.
        """
        exchange = connection.exchanges[message.exchange_id]
        try:
            params = {}
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
        except RequestTimeout:
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.ERROR,
                target_message=message,
                code=TickersMessage.ErrorCode.API_ERROR,
                message="The request has timed out.",
            )
        return response_message

    async def get_ticker(
        self, message: TickersMessage, dialogue: TickersDialogue, connection
    ) -> Optional[TickersMessage]:
        """
        Get a ticker from the exchange.
        """
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
        except RequestTimeout:
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.ERROR,
                target_message=message,
                code=TickersMessage.ErrorCode.API_ERROR,
                message="The request has timed out.",
            )
        return response_message
