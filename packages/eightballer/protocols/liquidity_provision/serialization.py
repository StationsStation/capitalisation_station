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

"""Serialization module for liquidity_provision protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.liquidity_provision import (  # type: ignore
    liquidity_provision_pb2,
)
from packages.eightballer.protocols.liquidity_provision.custom_types import (  # type: ignore
    ErrorCode,
)
from packages.eightballer.protocols.liquidity_provision.message import (  # type: ignore
    LiquidityProvisionMessage,
)


class LiquidityProvisionSerializer(Serializer):
    """Serialization for the 'liquidity_provision' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'LiquidityProvision' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(LiquidityProvisionMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        liquidity_provision_msg = liquidity_provision_pb2.LiquidityProvisionMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == LiquidityProvisionMessage.Performative.ADD_LIQUIDITY:
            performative = liquidity_provision_pb2.LiquidityProvisionMessage.Add_Liquidity_Performative()  # type: ignore
            pool_id = msg.pool_id
            performative.pool_id = pool_id
            token_ids = msg.token_ids
            performative.token_ids.extend(token_ids)
            amounts = msg.amounts
            performative.amounts.extend(amounts)
            min_mint_amount = msg.min_mint_amount
            performative.min_mint_amount = min_mint_amount
            deadline = msg.deadline
            performative.deadline = deadline
            if msg.is_set("user_data"):
                performative.user_data_is_set = True
                user_data = msg.user_data
                performative.user_data = user_data
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            liquidity_provision_msg.add_liquidity.CopyFrom(performative)
        elif performative_id == LiquidityProvisionMessage.Performative.REMOVE_LIQUIDITY:
            performative = liquidity_provision_pb2.LiquidityProvisionMessage.Remove_Liquidity_Performative()  # type: ignore
            pool_id = msg.pool_id
            performative.pool_id = pool_id
            token_ids = msg.token_ids
            performative.token_ids.extend(token_ids)
            burn_amount = msg.burn_amount
            performative.burn_amount = burn_amount
            min_amounts = msg.min_amounts
            performative.min_amounts.extend(min_amounts)
            deadline = msg.deadline
            performative.deadline = deadline
            if msg.is_set("user_data"):
                performative.user_data_is_set = True
                user_data = msg.user_data
                performative.user_data = user_data
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            liquidity_provision_msg.remove_liquidity.CopyFrom(performative)
        elif performative_id == LiquidityProvisionMessage.Performative.QUERY_LIQUIDITY:
            performative = liquidity_provision_pb2.LiquidityProvisionMessage.Query_Liquidity_Performative()  # type: ignore
            pool_id = msg.pool_id
            performative.pool_id = pool_id
            exchange_id = msg.exchange_id
            performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            liquidity_provision_msg.query_liquidity.CopyFrom(performative)
        elif performative_id == LiquidityProvisionMessage.Performative.LIQUIDITY_ADDED:
            performative = liquidity_provision_pb2.LiquidityProvisionMessage.Liquidity_Added_Performative()  # type: ignore
            pool_id = msg.pool_id
            performative.pool_id = pool_id
            minted_tokens = msg.minted_tokens
            performative.minted_tokens = minted_tokens
            liquidity_provision_msg.liquidity_added.CopyFrom(performative)
        elif performative_id == LiquidityProvisionMessage.Performative.LIQUIDITY_REMOVED:
            performative = liquidity_provision_pb2.LiquidityProvisionMessage.Liquidity_Removed_Performative()  # type: ignore
            pool_id = msg.pool_id
            performative.pool_id = pool_id
            received_amounts = msg.received_amounts
            performative.received_amounts.extend(received_amounts)
            liquidity_provision_msg.liquidity_removed.CopyFrom(performative)
        elif performative_id == LiquidityProvisionMessage.Performative.LIQUIDITY_STATUS:
            performative = liquidity_provision_pb2.LiquidityProvisionMessage.Liquidity_Status_Performative()  # type: ignore
            pool_id = msg.pool_id
            performative.pool_id = pool_id
            current_liquidity = msg.current_liquidity
            performative.current_liquidity = current_liquidity
            available_tokens = msg.available_tokens
            performative.available_tokens.extend(available_tokens)
            liquidity_provision_msg.liquidity_status.CopyFrom(performative)
        elif performative_id == LiquidityProvisionMessage.Performative.ERROR:
            performative = liquidity_provision_pb2.LiquidityProvisionMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            description = msg.description
            performative.description = description
            liquidity_provision_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = liquidity_provision_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'LiquidityProvision' message.

        :param obj: the bytes object.
        :return: the 'LiquidityProvision' message.
        """
        message_pb = ProtobufMessage()
        liquidity_provision_pb = liquidity_provision_pb2.LiquidityProvisionMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        liquidity_provision_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = liquidity_provision_pb.WhichOneof("performative")
        performative_id = LiquidityProvisionMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == LiquidityProvisionMessage.Performative.ADD_LIQUIDITY:
            pool_id = liquidity_provision_pb.add_liquidity.pool_id
            performative_content["pool_id"] = pool_id
            token_ids = liquidity_provision_pb.add_liquidity.token_ids
            token_ids_tuple = tuple(token_ids)
            performative_content["token_ids"] = token_ids_tuple
            amounts = liquidity_provision_pb.add_liquidity.amounts
            amounts_tuple = tuple(amounts)
            performative_content["amounts"] = amounts_tuple
            min_mint_amount = liquidity_provision_pb.add_liquidity.min_mint_amount
            performative_content["min_mint_amount"] = min_mint_amount
            deadline = liquidity_provision_pb.add_liquidity.deadline
            performative_content["deadline"] = deadline
            if liquidity_provision_pb.add_liquidity.user_data_is_set:
                user_data = liquidity_provision_pb.add_liquidity.user_data
                performative_content["user_data"] = user_data
            exchange_id = liquidity_provision_pb.add_liquidity.exchange_id
            performative_content["exchange_id"] = exchange_id
            if liquidity_provision_pb.add_liquidity.ledger_id_is_set:
                ledger_id = liquidity_provision_pb.add_liquidity.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == LiquidityProvisionMessage.Performative.REMOVE_LIQUIDITY:
            pool_id = liquidity_provision_pb.remove_liquidity.pool_id
            performative_content["pool_id"] = pool_id
            token_ids = liquidity_provision_pb.remove_liquidity.token_ids
            token_ids_tuple = tuple(token_ids)
            performative_content["token_ids"] = token_ids_tuple
            burn_amount = liquidity_provision_pb.remove_liquidity.burn_amount
            performative_content["burn_amount"] = burn_amount
            min_amounts = liquidity_provision_pb.remove_liquidity.min_amounts
            min_amounts_tuple = tuple(min_amounts)
            performative_content["min_amounts"] = min_amounts_tuple
            deadline = liquidity_provision_pb.remove_liquidity.deadline
            performative_content["deadline"] = deadline
            if liquidity_provision_pb.remove_liquidity.user_data_is_set:
                user_data = liquidity_provision_pb.remove_liquidity.user_data
                performative_content["user_data"] = user_data
            exchange_id = liquidity_provision_pb.remove_liquidity.exchange_id
            performative_content["exchange_id"] = exchange_id
            if liquidity_provision_pb.remove_liquidity.ledger_id_is_set:
                ledger_id = liquidity_provision_pb.remove_liquidity.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == LiquidityProvisionMessage.Performative.QUERY_LIQUIDITY:
            pool_id = liquidity_provision_pb.query_liquidity.pool_id
            performative_content["pool_id"] = pool_id
            exchange_id = liquidity_provision_pb.query_liquidity.exchange_id
            performative_content["exchange_id"] = exchange_id
            if liquidity_provision_pb.query_liquidity.ledger_id_is_set:
                ledger_id = liquidity_provision_pb.query_liquidity.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == LiquidityProvisionMessage.Performative.LIQUIDITY_ADDED:
            pool_id = liquidity_provision_pb.liquidity_added.pool_id
            performative_content["pool_id"] = pool_id
            minted_tokens = liquidity_provision_pb.liquidity_added.minted_tokens
            performative_content["minted_tokens"] = minted_tokens
        elif performative_id == LiquidityProvisionMessage.Performative.LIQUIDITY_REMOVED:
            pool_id = liquidity_provision_pb.liquidity_removed.pool_id
            performative_content["pool_id"] = pool_id
            received_amounts = liquidity_provision_pb.liquidity_removed.received_amounts
            received_amounts_tuple = tuple(received_amounts)
            performative_content["received_amounts"] = received_amounts_tuple
        elif performative_id == LiquidityProvisionMessage.Performative.LIQUIDITY_STATUS:
            pool_id = liquidity_provision_pb.liquidity_status.pool_id
            performative_content["pool_id"] = pool_id
            current_liquidity = liquidity_provision_pb.liquidity_status.current_liquidity
            performative_content["current_liquidity"] = current_liquidity
            available_tokens = liquidity_provision_pb.liquidity_status.available_tokens
            available_tokens_tuple = tuple(available_tokens)
            performative_content["available_tokens"] = available_tokens_tuple
        elif performative_id == LiquidityProvisionMessage.Performative.ERROR:
            pb2_error_code = liquidity_provision_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            description = liquidity_provision_pb.error.description
            performative_content["description"] = description
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return LiquidityProvisionMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
