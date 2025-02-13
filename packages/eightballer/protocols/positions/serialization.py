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

"""Serialization module for positions protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.positions import positions_pb2  # type: ignore
from packages.eightballer.protocols.positions.custom_types import (  # type: ignore
    ErrorCode,
    Position,
    PositionSide,
    Positions,
)
from packages.eightballer.protocols.positions.message import (  # type: ignore
    PositionsMessage,
)


class PositionsSerializer(Serializer):
    """Serialization for the 'positions' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Positions' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(PositionsMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        positions_msg = positions_pb2.PositionsMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == PositionsMessage.Performative.GET_ALL_POSITIONS:
            performative = positions_pb2.PositionsMessage.Get_All_Positions_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            if msg.is_set("params"):
                performative.params_is_set = True
                params = msg.params
                performative.params.update(params)
            if msg.is_set("side"):
                performative.side_is_set = True
                side = msg.side
                PositionSide.encode(performative.side, side)
            positions_msg.get_all_positions.CopyFrom(performative)
        elif performative_id == PositionsMessage.Performative.GET_POSITION:
            performative = positions_pb2.PositionsMessage.Get_Position_Performative()  # type: ignore
            position_id = msg.position_id
            performative.position_id = position_id
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            positions_msg.get_position.CopyFrom(performative)
        elif performative_id == PositionsMessage.Performative.ALL_POSITIONS:
            performative = positions_pb2.PositionsMessage.All_Positions_Performative()  # type: ignore
            positions = msg.positions
            Positions.encode(performative.positions, positions)
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            positions_msg.all_positions.CopyFrom(performative)
        elif performative_id == PositionsMessage.Performative.POSITION:
            performative = positions_pb2.PositionsMessage.Position_Performative()  # type: ignore
            position = msg.position
            Position.encode(performative.position, position)
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            positions_msg.position.CopyFrom(performative)
        elif performative_id == PositionsMessage.Performative.ERROR:
            performative = positions_pb2.PositionsMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            positions_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = positions_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Positions' message.

        :param obj: the bytes object.
        :return: the 'Positions' message.
        """
        message_pb = ProtobufMessage()
        positions_pb = positions_pb2.PositionsMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        positions_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = positions_pb.WhichOneof("performative")
        performative_id = PositionsMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == PositionsMessage.Performative.GET_ALL_POSITIONS:
            exchange_id = positions_pb.get_all_positions.exchange_id
            performative_content["exchange_id"] = exchange_id
            if positions_pb.get_all_positions.params_is_set:
                params = positions_pb.get_all_positions.params
                params_dict = dict(params)
                performative_content["params"] = params_dict
            if positions_pb.get_all_positions.side_is_set:
                pb2_side = positions_pb.get_all_positions.side
                side = PositionSide.decode(pb2_side)
                performative_content["side"] = side
        elif performative_id == PositionsMessage.Performative.GET_POSITION:
            position_id = positions_pb.get_position.position_id
            performative_content["position_id"] = position_id
            exchange_id = positions_pb.get_position.exchange_id
            performative_content["exchange_id"] = exchange_id
        elif performative_id == PositionsMessage.Performative.ALL_POSITIONS:
            pb2_positions = positions_pb.all_positions.positions
            positions = Positions.decode(pb2_positions)
            performative_content["positions"] = positions
            exchange_id = positions_pb.all_positions.exchange_id
            performative_content["exchange_id"] = exchange_id
        elif performative_id == PositionsMessage.Performative.POSITION:
            pb2_position = positions_pb.position.position
            position = Position.decode(pb2_position)
            performative_content["position"] = position
            exchange_id = positions_pb.position.exchange_id
            performative_content["exchange_id"] = exchange_id
        elif performative_id == PositionsMessage.Performative.ERROR:
            pb2_error_code = positions_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = positions_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = positions_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return PositionsMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
