"""
Implements the interface for the Ticker protocol.
"""
from typing import Optional

from ccxt import RequestTimeout

from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface
from packages.eightballer.protocols.tickers.custom_types import Ticker
from packages.eightballer.protocols.tickers.dialogues import BaseTickersDialogues, TickersDialogue
from packages.eightballer.protocols.tickers.message import TickersMessage


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

            if message.params is not None:
                for key, value in message.params.items():
                    params[key] = value.decode()
            tickers = await exchange.fetch_tickers(params=params)
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
                error_code=TickersMessage.ErrorCode.API_ERROR,
                error_msg="The request has timed out.",
                error_data={},
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
                error_code=TickersMessage.ErrorCode.API_ERROR,
                error_msg="The request has timed out.",
                error_data={},
            )
        return response_message
