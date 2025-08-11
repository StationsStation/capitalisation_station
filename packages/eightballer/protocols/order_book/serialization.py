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

"""Serialization module for order_book protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.order_book import order_book_pb2  # type: ignore
from packages.eightballer.protocols.order_book.custom_types import (  # type: ignore
    OrderBook,
)
from packages.eightballer.protocols.order_book.message import (  # type: ignore
    OrderBookMessage,
)


class OrderBookSerializer(Serializer):
    """Serialization for the 'order_book' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'OrderBook' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(OrderBookMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        order_book_msg = order_book_pb2.OrderBookMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == OrderBookMessage.Performative.SUBSCRIBE:
            performative = order_book_pb2.OrderBookMessage.Subscribe_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            symbol = msg.symbol
            performative.symbol = symbol
            if msg.is_set("precision"):
                performative.precision_is_set = True
                precision = msg.precision
                performative.precision = precision
            if msg.is_set("interval"):
                performative.interval_is_set = True
                interval = msg.interval
                performative.interval = interval
            order_book_msg.subscribe.CopyFrom(performative)
        elif performative_id == OrderBookMessage.Performative.UNSUBSCRIBE:
            performative = order_book_pb2.OrderBookMessage.Unsubscribe_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            symbol = msg.symbol
            performative.symbol = symbol
            order_book_msg.unsubscribe.CopyFrom(performative)
        elif performative_id == OrderBookMessage.Performative.ORDER_BOOK_UPDATE:
            performative = order_book_pb2.OrderBookMessage.Order_Book_Update_Performative()  # type: ignore
            order_book = msg.order_book
            OrderBook.encode(performative.order_book, order_book)
            order_book_msg.order_book_update.CopyFrom(performative)
        elif performative_id == OrderBookMessage.Performative.ERROR:
            performative = order_book_pb2.OrderBookMessage.Error_Performative()  # type: ignore
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            order_book_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = order_book_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'OrderBook' message.

        :param obj: the bytes object.
        :return: the 'OrderBook' message.
        """
        message_pb = ProtobufMessage()
        order_book_pb = order_book_pb2.OrderBookMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        order_book_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = order_book_pb.WhichOneof("performative")
        performative_id = OrderBookMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == OrderBookMessage.Performative.SUBSCRIBE:
            exchange_id = order_book_pb.subscribe.exchange_id
            performative_content["exchange_id"] = exchange_id
            symbol = order_book_pb.subscribe.symbol
            performative_content["symbol"] = symbol
            if order_book_pb.subscribe.precision_is_set:
                precision = order_book_pb.subscribe.precision
                performative_content["precision"] = precision
            if order_book_pb.subscribe.interval_is_set:
                interval = order_book_pb.subscribe.interval
                performative_content["interval"] = interval
        elif performative_id == OrderBookMessage.Performative.UNSUBSCRIBE:
            exchange_id = order_book_pb.unsubscribe.exchange_id
            performative_content["exchange_id"] = exchange_id
            symbol = order_book_pb.unsubscribe.symbol
            performative_content["symbol"] = symbol
        elif performative_id == OrderBookMessage.Performative.ORDER_BOOK_UPDATE:
            pb2_order_book = order_book_pb.order_book_update.order_book
            order_book = OrderBook.decode(pb2_order_book)
            performative_content["order_book"] = order_book
        elif performative_id == OrderBookMessage.Performative.ERROR:
            error_msg = order_book_pb.error.error_msg
            performative_content["error_msg"] = error_msg
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return OrderBookMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
