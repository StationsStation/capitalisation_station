"""Implements the interface for the Ticker protocol."""

import json

import requests

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.tickers.dialogues import TickersDialogue, BaseTickersDialogues
from packages.eightballer.connections.dcxt.dcxt.exceptions import RpcError, ExchangeNotAvailable, SorRetrievalException
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


class TickerInterface(BaseInterface):
    """Interface for ticker protocol."""

    protocol_id = TickersMessage.protocol_id
    dialogue_class = TickersDialogue
    dialogues_class = BaseTickersDialogues

    async def get_all_tickers(
        self, message: TickersMessage, dialogue: TickersDialogue, connection
    ) -> TickersMessage | None:
        """Get all tickers from the exchange."""
        exchange = connection.exchanges[message.ledger_id][message.exchange_id]
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
                ledger_id=message.ledger_id,
            )
        except (
            dcxt.exceptions.RequestTimeout,
            dcxt.exceptions.ExchangeError,
            ExchangeNotAvailable,
            RpcError,
            SorRetrievalException,
        ):
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.ERROR,
                target_message=message,
                error_code=TickersMessage.ErrorCode.API_ERROR,
                error_msg="The request has timed out.",
                error_data={},
            )
        return response_message

    async def get_ticker(self, message: TickersMessage, dialogue: TickersDialogue, connection) -> TickersMessage | None:
        """Get a ticker from the exchange."""
        exchange = connection.exchanges[message.ledger_id][message.exchange_id]
        try:
            ticker = await exchange.fetch_ticker(
                symbol=message.symbol,
                asset_a=message.asset_a,
                asset_b=message.asset_b,
                params=json.loads(message.params.decode("utf-8")) if message.params is not None else {},
            )
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.TICKER,
                target_message=message,
                ticker=ticker,
            )
        except (
            dcxt.exceptions.RequestTimeout,
            dcxt.exceptions.RpcError,
            dcxt.exceptions.ExchangeError,
            ExchangeNotAvailable,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
        ):
            response_message = dialogue.reply(
                performative=TickersMessage.Performative.ERROR,
                target_message=message,
                error_code=TickersMessage.ErrorCode.API_ERROR,
                error_msg="The request has timed out.",
                error_data={},
            )
        return response_message
