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

"""Serialization module for approvals protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.approvals import approvals_pb2  # type: ignore
from packages.eightballer.protocols.approvals.custom_types import (  # type: ignore
    Approval,
    ErrorCode,
)
from packages.eightballer.protocols.approvals.message import (  # type: ignore
    ApprovalsMessage,
)


class ApprovalsSerializer(Serializer):
    """Serialization for the 'approvals' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Approvals' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(ApprovalsMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        approvals_msg = approvals_pb2.ApprovalsMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == ApprovalsMessage.Performative.SET_APPROVAL:
            performative = approvals_pb2.ApprovalsMessage.Set_Approval_Performative()  # type: ignore
            approval = msg.approval
            Approval.encode(performative.approval, approval)
            approvals_msg.set_approval.CopyFrom(performative)
        elif performative_id == ApprovalsMessage.Performative.GET_APPROVAL:
            performative = approvals_pb2.ApprovalsMessage.Get_Approval_Performative()  # type: ignore
            approval = msg.approval
            Approval.encode(performative.approval, approval)
            approvals_msg.get_approval.CopyFrom(performative)
        elif performative_id == ApprovalsMessage.Performative.APPROVAL_RESPONSE:
            performative = approvals_pb2.ApprovalsMessage.Approval_Response_Performative()  # type: ignore
            approval = msg.approval
            Approval.encode(performative.approval, approval)
            approvals_msg.approval_response.CopyFrom(performative)
        elif performative_id == ApprovalsMessage.Performative.ERROR:
            performative = approvals_pb2.ApprovalsMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            approvals_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = approvals_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Approvals' message.

        :param obj: the bytes object.
        :return: the 'Approvals' message.
        """
        message_pb = ProtobufMessage()
        approvals_pb = approvals_pb2.ApprovalsMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        approvals_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = approvals_pb.WhichOneof("performative")
        performative_id = ApprovalsMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == ApprovalsMessage.Performative.SET_APPROVAL:
            pb2_approval = approvals_pb.set_approval.approval
            approval = Approval.decode(pb2_approval)
            performative_content["approval"] = approval
        elif performative_id == ApprovalsMessage.Performative.GET_APPROVAL:
            pb2_approval = approvals_pb.get_approval.approval
            approval = Approval.decode(pb2_approval)
            performative_content["approval"] = approval
        elif performative_id == ApprovalsMessage.Performative.APPROVAL_RESPONSE:
            pb2_approval = approvals_pb.approval_response.approval
            approval = Approval.decode(pb2_approval)
            performative_content["approval"] = approval
        elif performative_id == ApprovalsMessage.Performative.ERROR:
            pb2_error_code = approvals_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = approvals_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = approvals_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return ApprovalsMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
