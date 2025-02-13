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

"""Serialization module for ohlcv protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.ohlcv import ohlcv_pb2  # type: ignore
from packages.eightballer.protocols.ohlcv.custom_types import ErrorCode  # type: ignore
from packages.eightballer.protocols.ohlcv.message import OhlcvMessage  # type: ignore


class OhlcvSerializer(Serializer):
    """Serialization for the 'ohlcv' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Ohlcv' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(OhlcvMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        ohlcv_msg = ohlcv_pb2.OhlcvMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == OhlcvMessage.Performative.SUBSCRIBE:
            performative = ohlcv_pb2.OhlcvMessage.Subscribe_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            market_name = msg.market_name
            performative.market_name = market_name
            interval = msg.interval
            performative.interval = interval
            ohlcv_msg.subscribe.CopyFrom(performative)
        elif performative_id == OhlcvMessage.Performative.CANDLESTICK:
            performative = ohlcv_pb2.OhlcvMessage.Candlestick_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            market_name = msg.market_name
            performative.market_name = market_name
            interval = msg.interval
            performative.interval = interval
            open = msg.open
            performative.open = open
            high = msg.high
            performative.high = high
            low = msg.low
            performative.low = low
            close = msg.close
            performative.close = close
            volume = msg.volume
            performative.volume = volume
            timestamp = msg.timestamp
            performative.timestamp = timestamp
            ohlcv_msg.candlestick.CopyFrom(performative)
        elif performative_id == OhlcvMessage.Performative.HISTORY:
            performative = ohlcv_pb2.OhlcvMessage.History_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            market_name = msg.market_name
            performative.market_name = market_name
            start_timestamp = msg.start_timestamp
            performative.start_timestamp = start_timestamp
            end_timestamp = msg.end_timestamp
            performative.end_timestamp = end_timestamp
            interval = msg.interval
            performative.interval = interval
            ohlcv_msg.history.CopyFrom(performative)
        elif performative_id == OhlcvMessage.Performative.ERROR:
            performative = ohlcv_pb2.OhlcvMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            ohlcv_msg.error.CopyFrom(performative)
        elif performative_id == OhlcvMessage.Performative.END:
            performative = ohlcv_pb2.OhlcvMessage.End_Performative()  # type: ignore
            ohlcv_msg.end.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = ohlcv_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Ohlcv' message.

        :param obj: the bytes object.
        :return: the 'Ohlcv' message.
        """
        message_pb = ProtobufMessage()
        ohlcv_pb = ohlcv_pb2.OhlcvMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        ohlcv_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = ohlcv_pb.WhichOneof("performative")
        performative_id = OhlcvMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == OhlcvMessage.Performative.SUBSCRIBE:
            exchange_id = ohlcv_pb.subscribe.exchange_id
            performative_content["exchange_id"] = exchange_id
            market_name = ohlcv_pb.subscribe.market_name
            performative_content["market_name"] = market_name
            interval = ohlcv_pb.subscribe.interval
            performative_content["interval"] = interval
        elif performative_id == OhlcvMessage.Performative.CANDLESTICK:
            exchange_id = ohlcv_pb.candlestick.exchange_id
            performative_content["exchange_id"] = exchange_id
            market_name = ohlcv_pb.candlestick.market_name
            performative_content["market_name"] = market_name
            interval = ohlcv_pb.candlestick.interval
            performative_content["interval"] = interval
            open = ohlcv_pb.candlestick.open
            performative_content["open"] = open
            high = ohlcv_pb.candlestick.high
            performative_content["high"] = high
            low = ohlcv_pb.candlestick.low
            performative_content["low"] = low
            close = ohlcv_pb.candlestick.close
            performative_content["close"] = close
            volume = ohlcv_pb.candlestick.volume
            performative_content["volume"] = volume
            timestamp = ohlcv_pb.candlestick.timestamp
            performative_content["timestamp"] = timestamp
        elif performative_id == OhlcvMessage.Performative.HISTORY:
            exchange_id = ohlcv_pb.history.exchange_id
            performative_content["exchange_id"] = exchange_id
            market_name = ohlcv_pb.history.market_name
            performative_content["market_name"] = market_name
            start_timestamp = ohlcv_pb.history.start_timestamp
            performative_content["start_timestamp"] = start_timestamp
            end_timestamp = ohlcv_pb.history.end_timestamp
            performative_content["end_timestamp"] = end_timestamp
            interval = ohlcv_pb.history.interval
            performative_content["interval"] = interval
        elif performative_id == OhlcvMessage.Performative.ERROR:
            pb2_error_code = ohlcv_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = ohlcv_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = ohlcv_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        elif performative_id == OhlcvMessage.Performative.END:
            pass
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return OhlcvMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
