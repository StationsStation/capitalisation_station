# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2025 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Serialization module for tickers protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.tickers import tickers_pb2  # type: ignore
from packages.eightballer.protocols.tickers.custom_types import (  # type: ignore
    ErrorCode,
    Ticker,
    Tickers,
)
from packages.eightballer.protocols.tickers.message import (  # type: ignore
    TickersMessage,
)


class TickersSerializer(Serializer):
    """Serialization for the 'tickers' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Tickers' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(TickersMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        tickers_msg = tickers_pb2.TickersMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == TickersMessage.Performative.GET_ALL_TICKERS:
            performative = tickers_pb2.TickersMessage.Get_All_Tickers_Performative()  # type: ignore
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("params"):
                performative.params_is_set = True
                params = msg.params
                performative.params = params
            tickers_msg.get_all_tickers.CopyFrom(performative)
        elif performative_id == TickersMessage.Performative.GET_TICKER:
            performative = tickers_pb2.TickersMessage.Get_Ticker_Performative()  # type: ignore
            if msg.is_set("symbol"):
                performative.symbol_is_set = True
                symbol = msg.symbol
                performative.symbol = symbol
            if msg.is_set("asset_a"):
                performative.asset_a_is_set = True
                asset_a = msg.asset_a
                performative.asset_a = asset_a
            if msg.is_set("asset_b"):
                performative.asset_b_is_set = True
                asset_b = msg.asset_b
                performative.asset_b = asset_b
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            if msg.is_set("params"):
                performative.params_is_set = True
                params = msg.params
                performative.params = params
            tickers_msg.get_ticker.CopyFrom(performative)
        elif performative_id == TickersMessage.Performative.ALL_TICKERS:
            performative = tickers_pb2.TickersMessage.All_Tickers_Performative()  # type: ignore
            tickers = msg.tickers
            Tickers.encode(performative.tickers, tickers)
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            tickers_msg.all_tickers.CopyFrom(performative)
        elif performative_id == TickersMessage.Performative.TICKER:
            performative = tickers_pb2.TickersMessage.Ticker_Performative()  # type: ignore
            ticker = msg.ticker
            Ticker.encode(performative.ticker, ticker)
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            tickers_msg.ticker.CopyFrom(performative)
        elif performative_id == TickersMessage.Performative.ERROR:
            performative = tickers_pb2.TickersMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            tickers_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = tickers_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Tickers' message.

        :param obj: the bytes object.
        :return: the 'Tickers' message.
        """
        message_pb = ProtobufMessage()
        tickers_pb = tickers_pb2.TickersMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        tickers_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = tickers_pb.WhichOneof("performative")
        performative_id = TickersMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == TickersMessage.Performative.GET_ALL_TICKERS:
            if tickers_pb.get_all_tickers.ledger_id_is_set:
                ledger_id = tickers_pb.get_all_tickers.ledger_id
                performative_content["ledger_id"] = ledger_id
            if tickers_pb.get_all_tickers.exchange_id_is_set:
                exchange_id = tickers_pb.get_all_tickers.exchange_id
                performative_content["exchange_id"] = exchange_id
            if tickers_pb.get_all_tickers.params_is_set:
                params = tickers_pb.get_all_tickers.params
                performative_content["params"] = params
        elif performative_id == TickersMessage.Performative.GET_TICKER:
            if tickers_pb.get_ticker.symbol_is_set:
                symbol = tickers_pb.get_ticker.symbol
                performative_content["symbol"] = symbol
            if tickers_pb.get_ticker.asset_a_is_set:
                asset_a = tickers_pb.get_ticker.asset_a
                performative_content["asset_a"] = asset_a
            if tickers_pb.get_ticker.asset_b_is_set:
                asset_b = tickers_pb.get_ticker.asset_b
                performative_content["asset_b"] = asset_b
            if tickers_pb.get_ticker.exchange_id_is_set:
                exchange_id = tickers_pb.get_ticker.exchange_id
                performative_content["exchange_id"] = exchange_id
            if tickers_pb.get_ticker.ledger_id_is_set:
                ledger_id = tickers_pb.get_ticker.ledger_id
                performative_content["ledger_id"] = ledger_id
            if tickers_pb.get_ticker.params_is_set:
                params = tickers_pb.get_ticker.params
                performative_content["params"] = params
        elif performative_id == TickersMessage.Performative.ALL_TICKERS:
            pb2_tickers = tickers_pb.all_tickers.tickers
            tickers = Tickers.decode(pb2_tickers)
            performative_content["tickers"] = tickers
            if tickers_pb.all_tickers.exchange_id_is_set:
                exchange_id = tickers_pb.all_tickers.exchange_id
                performative_content["exchange_id"] = exchange_id
            if tickers_pb.all_tickers.ledger_id_is_set:
                ledger_id = tickers_pb.all_tickers.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == TickersMessage.Performative.TICKER:
            pb2_ticker = tickers_pb.ticker.ticker
            ticker = Ticker.decode(pb2_ticker)
            performative_content["ticker"] = ticker
            if tickers_pb.ticker.exchange_id_is_set:
                exchange_id = tickers_pb.ticker.exchange_id
                performative_content["exchange_id"] = exchange_id
            if tickers_pb.ticker.ledger_id_is_set:
                ledger_id = tickers_pb.ticker.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == TickersMessage.Performative.ERROR:
            pb2_error_code = tickers_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = tickers_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = tickers_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return TickersMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
