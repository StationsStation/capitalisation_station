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

"""Serialization module for orders protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.orders import orders_pb2  # type: ignore
from packages.eightballer.protocols.orders.custom_types import (  # type: ignore
    ErrorCode,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    Orders,
)
from packages.eightballer.protocols.orders.message import OrdersMessage  # type: ignore


class OrdersSerializer(Serializer):
    """Serialization for the 'orders' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Orders' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(OrdersMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        orders_msg = orders_pb2.OrdersMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == OrdersMessage.Performative.CREATE_ORDER:
            performative = orders_pb2.OrdersMessage.Create_Order_Performative()  # type: ignore
            order = msg.order
            Order.encode(performative.order, order)
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            orders_msg.create_order.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.ORDER_CREATED:
            performative = orders_pb2.OrdersMessage.Order_Created_Performative()  # type: ignore
            order = msg.order
            Order.encode(performative.order, order)
            orders_msg.order_created.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.CANCEL_ORDER:
            performative = orders_pb2.OrdersMessage.Cancel_Order_Performative()  # type: ignore
            order = msg.order
            Order.encode(performative.order, order)
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            orders_msg.cancel_order.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.ORDER_CANCELLED:
            performative = orders_pb2.OrdersMessage.Order_Cancelled_Performative()  # type: ignore
            order = msg.order
            Order.encode(performative.order, order)
            orders_msg.order_cancelled.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.GET_ORDERS:
            performative = orders_pb2.OrdersMessage.Get_Orders_Performative()  # type: ignore
            if msg.is_set("symbol"):
                performative.symbol_is_set = True
                symbol = msg.symbol
                performative.symbol = symbol
            if msg.is_set("currency"):
                performative.currency_is_set = True
                currency = msg.currency
                performative.currency = currency
            if msg.is_set("order_type"):
                performative.order_type_is_set = True
                order_type = msg.order_type
                OrderType.encode(performative.order_type, order_type)
            if msg.is_set("side"):
                performative.side_is_set = True
                side = msg.side
                OrderSide.encode(performative.side, side)
            if msg.is_set("status"):
                performative.status_is_set = True
                status = msg.status
                OrderStatus.encode(performative.status, status)
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            if msg.is_set("account"):
                performative.account_is_set = True
                account = msg.account
                performative.account = account
            orders_msg.get_orders.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.GET_SETTLEMENTS:
            performative = orders_pb2.OrdersMessage.Get_Settlements_Performative()  # type: ignore
            if msg.is_set("currency"):
                performative.currency_is_set = True
                currency = msg.currency
                performative.currency = currency
            if msg.is_set("end_timestamp"):
                performative.end_timestamp_is_set = True
                end_timestamp = msg.end_timestamp
                performative.end_timestamp = end_timestamp
            if msg.is_set("start_timestamp"):
                performative.start_timestamp_is_set = True
                start_timestamp = msg.start_timestamp
                performative.start_timestamp = start_timestamp
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            orders_msg.get_settlements.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.GET_ORDER:
            performative = orders_pb2.OrdersMessage.Get_Order_Performative()  # type: ignore
            order = msg.order
            Order.encode(performative.order, order)
            if msg.is_set("exchange_id"):
                performative.exchange_id_is_set = True
                exchange_id = msg.exchange_id
                performative.exchange_id = exchange_id
            if msg.is_set("ledger_id"):
                performative.ledger_id_is_set = True
                ledger_id = msg.ledger_id
                performative.ledger_id = ledger_id
            orders_msg.get_order.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.ORDER:
            performative = orders_pb2.OrdersMessage.Order_Performative()  # type: ignore
            order = msg.order
            Order.encode(performative.order, order)
            orders_msg.order.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.ORDERS:
            performative = orders_pb2.OrdersMessage.Orders_Performative()  # type: ignore
            orders = msg.orders
            Orders.encode(performative.orders, orders)
            orders_msg.orders.CopyFrom(performative)
        elif performative_id == OrdersMessage.Performative.ERROR:
            performative = orders_pb2.OrdersMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            orders_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = orders_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Orders' message.

        :param obj: the bytes object.
        :return: the 'Orders' message.
        """
        message_pb = ProtobufMessage()
        orders_pb = orders_pb2.OrdersMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        orders_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = orders_pb.WhichOneof("performative")
        performative_id = OrdersMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == OrdersMessage.Performative.CREATE_ORDER:
            pb2_order = orders_pb.create_order.order
            order = Order.decode(pb2_order)
            performative_content["order"] = order
            if orders_pb.create_order.exchange_id_is_set:
                exchange_id = orders_pb.create_order.exchange_id
                performative_content["exchange_id"] = exchange_id
            if orders_pb.create_order.ledger_id_is_set:
                ledger_id = orders_pb.create_order.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == OrdersMessage.Performative.ORDER_CREATED:
            pb2_order = orders_pb.order_created.order
            order = Order.decode(pb2_order)
            performative_content["order"] = order
        elif performative_id == OrdersMessage.Performative.CANCEL_ORDER:
            pb2_order = orders_pb.cancel_order.order
            order = Order.decode(pb2_order)
            performative_content["order"] = order
            if orders_pb.cancel_order.exchange_id_is_set:
                exchange_id = orders_pb.cancel_order.exchange_id
                performative_content["exchange_id"] = exchange_id
            if orders_pb.cancel_order.ledger_id_is_set:
                ledger_id = orders_pb.cancel_order.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == OrdersMessage.Performative.ORDER_CANCELLED:
            pb2_order = orders_pb.order_cancelled.order
            order = Order.decode(pb2_order)
            performative_content["order"] = order
        elif performative_id == OrdersMessage.Performative.GET_ORDERS:
            if orders_pb.get_orders.symbol_is_set:
                symbol = orders_pb.get_orders.symbol
                performative_content["symbol"] = symbol
            if orders_pb.get_orders.currency_is_set:
                currency = orders_pb.get_orders.currency
                performative_content["currency"] = currency
            if orders_pb.get_orders.order_type_is_set:
                pb2_order_type = orders_pb.get_orders.order_type
                order_type = OrderType.decode(pb2_order_type)
                performative_content["order_type"] = order_type
            if orders_pb.get_orders.side_is_set:
                pb2_side = orders_pb.get_orders.side
                side = OrderSide.decode(pb2_side)
                performative_content["side"] = side
            if orders_pb.get_orders.status_is_set:
                pb2_status = orders_pb.get_orders.status
                status = OrderStatus.decode(pb2_status)
                performative_content["status"] = status
            if orders_pb.get_orders.exchange_id_is_set:
                exchange_id = orders_pb.get_orders.exchange_id
                performative_content["exchange_id"] = exchange_id
            if orders_pb.get_orders.ledger_id_is_set:
                ledger_id = orders_pb.get_orders.ledger_id
                performative_content["ledger_id"] = ledger_id
            if orders_pb.get_orders.account_is_set:
                account = orders_pb.get_orders.account
                performative_content["account"] = account
        elif performative_id == OrdersMessage.Performative.GET_SETTLEMENTS:
            if orders_pb.get_settlements.currency_is_set:
                currency = orders_pb.get_settlements.currency
                performative_content["currency"] = currency
            if orders_pb.get_settlements.end_timestamp_is_set:
                end_timestamp = orders_pb.get_settlements.end_timestamp
                performative_content["end_timestamp"] = end_timestamp
            if orders_pb.get_settlements.start_timestamp_is_set:
                start_timestamp = orders_pb.get_settlements.start_timestamp
                performative_content["start_timestamp"] = start_timestamp
            if orders_pb.get_settlements.ledger_id_is_set:
                ledger_id = orders_pb.get_settlements.ledger_id
                performative_content["ledger_id"] = ledger_id
            if orders_pb.get_settlements.exchange_id_is_set:
                exchange_id = orders_pb.get_settlements.exchange_id
                performative_content["exchange_id"] = exchange_id
        elif performative_id == OrdersMessage.Performative.GET_ORDER:
            pb2_order = orders_pb.get_order.order
            order = Order.decode(pb2_order)
            performative_content["order"] = order
            if orders_pb.get_order.exchange_id_is_set:
                exchange_id = orders_pb.get_order.exchange_id
                performative_content["exchange_id"] = exchange_id
            if orders_pb.get_order.ledger_id_is_set:
                ledger_id = orders_pb.get_order.ledger_id
                performative_content["ledger_id"] = ledger_id
        elif performative_id == OrdersMessage.Performative.ORDER:
            pb2_order = orders_pb.order.order
            order = Order.decode(pb2_order)
            performative_content["order"] = order
        elif performative_id == OrdersMessage.Performative.ORDERS:
            pb2_orders = orders_pb.orders.orders
            orders = Orders.decode(pb2_orders)
            performative_content["orders"] = orders
        elif performative_id == OrdersMessage.Performative.ERROR:
            pb2_error_code = orders_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = orders_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = orders_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return OrdersMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
