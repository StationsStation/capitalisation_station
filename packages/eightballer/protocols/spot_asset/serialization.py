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

"""Serialization module for spot_asset protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.spot_asset import spot_asset_pb2  # type: ignore
from packages.eightballer.protocols.spot_asset.custom_types import (  # type: ignore
    Decimal,
    ErrorCode,
)
from packages.eightballer.protocols.spot_asset.message import (  # type: ignore
    SpotAssetMessage,
)


class SpotAssetSerializer(Serializer):
    """Serialization for the 'spot_asset' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'SpotAsset' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(SpotAssetMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        spot_asset_msg = spot_asset_pb2.SpotAssetMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == SpotAssetMessage.Performative.GET_SPOT_ASSET:
            performative = spot_asset_pb2.SpotAssetMessage.Get_Spot_Asset_Performative()  # type: ignore
            name = msg.name
            performative.name = name
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            spot_asset_msg.get_spot_asset.CopyFrom(performative)
        elif performative_id == SpotAssetMessage.Performative.SPOT_ASSET:
            performative = spot_asset_pb2.SpotAssetMessage.Spot_Asset_Performative()  # type: ignore
            name = msg.name
            performative.name = name
            total = msg.total
            Decimal.encode(performative.total, total)
            free = msg.free
            Decimal.encode(performative.free, free)
            available_without_borrow = msg.available_without_borrow
            Decimal.encode(performative.available_without_borrow, available_without_borrow)
            if msg.is_set("usd_value"):
                performative.usd_value_is_set = True
                usd_value = msg.usd_value
                Decimal.encode(performative.usd_value, usd_value)
            if msg.is_set("decimal"):
                performative.decimal_is_set = True
                decimal = msg.decimal
                Decimal.encode(performative.decimal, decimal)
            spot_asset_msg.spot_asset.CopyFrom(performative)
        elif performative_id == SpotAssetMessage.Performative.GET_SPOT_ASSETS:
            performative = spot_asset_pb2.SpotAssetMessage.Get_Spot_Assets_Performative()  # type: ignore
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            spot_asset_msg.get_spot_assets.CopyFrom(performative)
        elif performative_id == SpotAssetMessage.Performative.ERROR:
            performative = spot_asset_pb2.SpotAssetMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            spot_asset_msg.error.CopyFrom(performative)
        elif performative_id == SpotAssetMessage.Performative.END:
            performative = spot_asset_pb2.SpotAssetMessage.End_Performative()  # type: ignore
            spot_asset_msg.end.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = spot_asset_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'SpotAsset' message.

        :param obj: the bytes object.
        :return: the 'SpotAsset' message.
        """
        message_pb = ProtobufMessage()
        spot_asset_pb = spot_asset_pb2.SpotAssetMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        spot_asset_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = spot_asset_pb.WhichOneof("performative")
        performative_id = SpotAssetMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == SpotAssetMessage.Performative.GET_SPOT_ASSET:
            name = spot_asset_pb.get_spot_asset.name
            performative_content["name"] = name
            exchange_id = spot_asset_pb.get_spot_asset.exchange_id
            performative_content["exchange_id"] = exchange_id
        elif performative_id == SpotAssetMessage.Performative.SPOT_ASSET:
            name = spot_asset_pb.spot_asset.name
            performative_content["name"] = name
            pb2_total = spot_asset_pb.spot_asset.total
            total = Decimal.decode(pb2_total)
            performative_content["total"] = total
            pb2_free = spot_asset_pb.spot_asset.free
            free = Decimal.decode(pb2_free)
            performative_content["free"] = free
            pb2_available_without_borrow = spot_asset_pb.spot_asset.available_without_borrow
            available_without_borrow = Decimal.decode(pb2_available_without_borrow)
            performative_content["available_without_borrow"] = available_without_borrow
            if spot_asset_pb.spot_asset.usd_value_is_set:
                pb2_usd_value = spot_asset_pb.spot_asset.usd_value
                usd_value = Decimal.decode(pb2_usd_value)
                performative_content["usd_value"] = usd_value
            if spot_asset_pb.spot_asset.decimal_is_set:
                pb2_decimal = spot_asset_pb.spot_asset.decimal
                decimal = Decimal.decode(pb2_decimal)
                performative_content["decimal"] = decimal
        elif performative_id == SpotAssetMessage.Performative.GET_SPOT_ASSETS:
            exchange_id = spot_asset_pb.get_spot_assets.exchange_id
            performative_content["exchange_id"] = exchange_id
        elif performative_id == SpotAssetMessage.Performative.ERROR:
            pb2_error_code = spot_asset_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = spot_asset_pb.error.error_msg
            performative_content["error_msg"] = error_msg
        elif performative_id == SpotAssetMessage.Performative.END:
            pass
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return SpotAssetMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
