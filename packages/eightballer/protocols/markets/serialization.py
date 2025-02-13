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

"""Serialization module for markets protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.markets import markets_pb2  # type: ignore
from packages.eightballer.protocols.markets.custom_types import (  # type: ignore
    ErrorCode,
    Market,
    Markets,
)
from packages.eightballer.protocols.markets.message import (  # type: ignore
    MarketsMessage,
)


class MarketsSerializer(Serializer):
    """Serialization for the 'markets' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Markets' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(MarketsMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        markets_msg = markets_pb2.MarketsMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == MarketsMessage.Performative.GET_ALL_MARKETS:
            performative = markets_pb2.MarketsMessage.Get_All_Markets_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            if msg.is_set("currency"):
                performative.currency_is_set = True
                currency = msg.currency
                performative.currency = currency
            markets_msg.get_all_markets.CopyFrom(performative)
        elif performative_id == MarketsMessage.Performative.GET_MARKET:
            performative = markets_pb2.MarketsMessage.Get_Market_Performative()  # type: ignore
            id = msg.id
            performative.id = id
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            markets_msg.get_market.CopyFrom(performative)
        elif performative_id == MarketsMessage.Performative.ALL_MARKETS:
            performative = markets_pb2.MarketsMessage.All_Markets_Performative()  # type: ignore
            markets = msg.markets
            Markets.encode(performative.markets, markets)
            markets_msg.all_markets.CopyFrom(performative)
        elif performative_id == MarketsMessage.Performative.MARKET:
            performative = markets_pb2.MarketsMessage.Market_Performative()  # type: ignore
            market = msg.market
            Market.encode(performative.market, market)
            markets_msg.market.CopyFrom(performative)
        elif performative_id == MarketsMessage.Performative.ERROR:
            performative = markets_pb2.MarketsMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            markets_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = markets_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Markets' message.

        :param obj: the bytes object.
        :return: the 'Markets' message.
        """
        message_pb = ProtobufMessage()
        markets_pb = markets_pb2.MarketsMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        markets_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = markets_pb.WhichOneof("performative")
        performative_id = MarketsMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == MarketsMessage.Performative.GET_ALL_MARKETS:
            exchange_id = markets_pb.get_all_markets.exchange_id
            performative_content["exchange_id"] = exchange_id
            if markets_pb.get_all_markets.currency_is_set:
                currency = markets_pb.get_all_markets.currency
                performative_content["currency"] = currency
        elif performative_id == MarketsMessage.Performative.GET_MARKET:
            id = markets_pb.get_market.id
            performative_content["id"] = id
            exchange_id = markets_pb.get_market.exchange_id
            performative_content["exchange_id"] = exchange_id
        elif performative_id == MarketsMessage.Performative.ALL_MARKETS:
            pb2_markets = markets_pb.all_markets.markets
            markets = Markets.decode(pb2_markets)
            performative_content["markets"] = markets
        elif performative_id == MarketsMessage.Performative.MARKET:
            pb2_market = markets_pb.market.market
            market = Market.decode(pb2_market)
            performative_content["market"] = market
        elif performative_id == MarketsMessage.Performative.ERROR:
            pb2_error_code = markets_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = markets_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = markets_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return MarketsMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
