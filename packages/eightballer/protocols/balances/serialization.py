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

"""Serialization module for balances protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.balances import balances_pb2  # type: ignore
from packages.eightballer.protocols.balances.custom_types import (  # type: ignore
    Balance,
    Balances,
    ErrorCode,
)
from packages.eightballer.protocols.balances.message import (  # type: ignore
    BalancesMessage,
)


class BalancesSerializer(Serializer):
    """Serialization for the 'balances' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Balances' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(BalancesMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        balances_msg = balances_pb2.BalancesMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == BalancesMessage.Performative.GET_ALL_BALANCES:
            performative = balances_pb2.BalancesMessage.Get_All_Balances_Performative()  # type: ignore
            if msg.is_set("params"):
                performative.params_is_set = True
                params = msg.params
                performative.params.update(params)
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            if msg.is_set("address"):
                performative.address_is_set = True
                address = msg.address
                performative.address = address
            balances_msg.get_all_balances.CopyFrom(performative)
        elif performative_id == BalancesMessage.Performative.GET_BALANCE:
            performative = balances_pb2.BalancesMessage.Get_Balance_Performative()  # type: ignore
            asset_id = msg.asset_id
            performative.asset_id = asset_id
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            if msg.is_set("address"):
                performative.address_is_set = True
                address = msg.address
                performative.address = address
            balances_msg.get_balance.CopyFrom(performative)
        elif performative_id == BalancesMessage.Performative.ALL_BALANCES:
            performative = balances_pb2.BalancesMessage.All_Balances_Performative()  # type: ignore
            balances = msg.balances
            Balances.encode(performative.balances, balances)
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            balances_msg.all_balances.CopyFrom(performative)
        elif performative_id == BalancesMessage.Performative.BALANCE:
            performative = balances_pb2.BalancesMessage.Balance_Performative()  # type: ignore
            balance = msg.balance
            Balance.encode(performative.balance, balance)
            balances_msg.balance.CopyFrom(performative)
        elif performative_id == BalancesMessage.Performative.ERROR:
            performative = balances_pb2.BalancesMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            balances_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = balances_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Balances' message.

        :param obj: the bytes object.
        :return: the 'Balances' message.
        """
        message_pb = ProtobufMessage()
        balances_pb = balances_pb2.BalancesMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        balances_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = balances_pb.WhichOneof("performative")
        performative_id = BalancesMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == BalancesMessage.Performative.GET_ALL_BALANCES:
            if balances_pb.get_all_balances.params_is_set:
                params = balances_pb.get_all_balances.params
                params_dict = dict(params)
                performative_content["params"] = params_dict
            if balances_pb.get_all_balances.exchange_id_is_set:
                exchange_id = balances_pb.get_all_balances.exchange_id
                performative_content["exchange_id"] = exchange_id
            if balances_pb.get_all_balances.ledger_id_is_set:
                ledger_id = balances_pb.get_all_balances.ledger_id
                performative_content["ledger_id"] = ledger_id
            if balances_pb.get_all_balances.address_is_set:
                address = balances_pb.get_all_balances.address
                performative_content["address"] = address
        elif performative_id == BalancesMessage.Performative.GET_BALANCE:
            asset_id = balances_pb.get_balance.asset_id
            performative_content["asset_id"] = asset_id
            if balances_pb.get_balance.exchange_id_is_set:
                exchange_id = balances_pb.get_balance.exchange_id
                performative_content["exchange_id"] = exchange_id
            if balances_pb.get_balance.ledger_id_is_set:
                ledger_id = balances_pb.get_balance.ledger_id
                performative_content["ledger_id"] = ledger_id
            if balances_pb.get_balance.address_is_set:
                address = balances_pb.get_balance.address
                performative_content["address"] = address
        elif performative_id == BalancesMessage.Performative.ALL_BALANCES:
            pb2_balances = balances_pb.all_balances.balances
            balances = Balances.decode(pb2_balances)
            performative_content["balances"] = balances
            if balances_pb.all_balances.ledger_id_is_set:
                ledger_id = balances_pb.all_balances.ledger_id
                performative_content["ledger_id"] = ledger_id
            if balances_pb.all_balances.exchange_id_is_set:
                exchange_id = balances_pb.all_balances.exchange_id
                performative_content["exchange_id"] = exchange_id
        elif performative_id == BalancesMessage.Performative.BALANCE:
            pb2_balance = balances_pb.balance.balance
            balance = Balance.decode(pb2_balance)
            performative_content["balance"] = balance
        elif performative_id == BalancesMessage.Performative.ERROR:
            pb2_error_code = balances_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = balances_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = balances_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return BalancesMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
