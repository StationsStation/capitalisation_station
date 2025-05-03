# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2025 zarathustra
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

"""Serialization module for asset_bridging protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.zarathustra.protocols.asset_bridging import (  # type: ignore
    asset_bridging_pb2,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import (  # type: ignore
    BridgeRequest,
    BridgeResult,
    ErrorInfo,
)
from packages.zarathustra.protocols.asset_bridging.message import (  # type: ignore
    AssetBridgingMessage,
)


class AssetBridgingSerializer(Serializer):
    """Serialization for the 'asset_bridging' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'AssetBridging' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(AssetBridgingMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        asset_bridging_msg = asset_bridging_pb2.AssetBridgingMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == AssetBridgingMessage.Performative.REQUEST_BRIDGE:
            performative = asset_bridging_pb2.AssetBridgingMessage.Request_Bridge_Performative()  # type: ignore
            request = msg.request
            BridgeRequest.encode(performative.request, request)
            asset_bridging_msg.request_bridge.CopyFrom(performative)
        elif performative_id == AssetBridgingMessage.Performative.BRIDGE_STATUS:
            performative = asset_bridging_pb2.AssetBridgingMessage.Bridge_Status_Performative()  # type: ignore
            result = msg.result
            BridgeResult.encode(performative.result, result)
            asset_bridging_msg.bridge_status.CopyFrom(performative)
        elif performative_id == AssetBridgingMessage.Performative.REQUEST_STATUS:
            performative = asset_bridging_pb2.AssetBridgingMessage.Request_Status_Performative()  # type: ignore
            result = msg.result
            BridgeResult.encode(performative.result, result)
            asset_bridging_msg.request_status.CopyFrom(performative)
        elif performative_id == AssetBridgingMessage.Performative.ERROR:
            performative = asset_bridging_pb2.AssetBridgingMessage.Error_Performative()  # type: ignore
            info = msg.info
            ErrorInfo.encode(performative.info, info)
            asset_bridging_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = asset_bridging_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'AssetBridging' message.

        :param obj: the bytes object.
        :return: the 'AssetBridging' message.
        """
        message_pb = ProtobufMessage()
        asset_bridging_pb = asset_bridging_pb2.AssetBridgingMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        asset_bridging_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = asset_bridging_pb.WhichOneof("performative")
        performative_id = AssetBridgingMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == AssetBridgingMessage.Performative.REQUEST_BRIDGE:
            pb2_request = asset_bridging_pb.request_bridge.request
            request = BridgeRequest.decode(pb2_request)
            performative_content["request"] = request
        elif performative_id == AssetBridgingMessage.Performative.BRIDGE_STATUS:
            pb2_result = asset_bridging_pb.bridge_status.result
            result = BridgeResult.decode(pb2_result)
            performative_content["result"] = result
        elif performative_id == AssetBridgingMessage.Performative.REQUEST_STATUS:
            pb2_result = asset_bridging_pb.request_status.result
            result = BridgeResult.decode(pb2_result)
            performative_content["result"] = result
        elif performative_id == AssetBridgingMessage.Performative.ERROR:
            pb2_info = asset_bridging_pb.error.info
            info = ErrorInfo.decode(pb2_info)
            performative_content["info"] = info
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return AssetBridgingMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
