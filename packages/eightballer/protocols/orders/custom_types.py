# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
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

"""This module contains class representations corresponding to every custom type in the protocol specification."""
# pylint: disable=C0301,R0902,C0103
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNKNOWN_MARKET = 0
    INSUFFICIENT_FUNDS = 1
    UNKNOWN_ORDER = 2
    API_ERROR = 3

    @staticmethod
    def encode(error_code_protobuf_object: Any, error_code_object: "ErrorCode") -> None:
        """
        Encode an instance of this class into the protocol buffer object.
        The protocol buffer object in the error_code_protobuf_object argument is matched with the instance of this class in the 'error_code_object' argument.
        :param error_code_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param error_code_object: an instance of this class to be encoded in the protocol buffer object.
        """
        error_code_protobuf_object.error_code = error_code_object.value

    @classmethod
    def decode(cls, error_code_protobuf_object: Any) -> "ErrorCode":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.
        A new instance of this class is created that matches the protocol buffer object in the 'error_code_protobuf_object' argument.
        :param error_code_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'error_code_protobuf_object' argument.
        """
        enum_value_from_pb2 = error_code_protobuf_object.error_code
        return ErrorCode(enum_value_from_pb2)


class OrderSide(Enum):
    """This class represents an instance of OrderSide."""

    BUY = 1
    SELL = 2

    @staticmethod
    def encode(order_side_protobuf_object, order_side_object: "OrderSide") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the order_side_protobuf_object argument is matched with the instance of this class in the 'order_side_object' argument.

        :param order_side_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param order_side_object: an instance of this class to be encoded in the protocol buffer object.
        """
        order_side_protobuf_object.order_side = order_side_object.value

    @classmethod
    def decode(cls, order_side_protobuf_object) -> "OrderSide":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'order_side_protobuf_object' argument.

        :param order_side_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'order_side_protobuf_object' argument.
        """
        enum_value_from_pb2 = order_side_protobuf_object.order_side
        return OrderSide(enum_value_from_pb2)

    def __eq__(self, other):
        return self.order_side == other.order_side  # noqa: E1101


class OrderStatus(Enum):
    """This class represents an instance of OrderStatus."""

    SUBMITTED = 0
    OPEN = 1
    PARTIALLY_FILLED = 2
    CANCELLED = 3
    FILLED = 4
    CLOSED = 5
    EXPIRED = 6
    FAILED = 7

    @staticmethod
    def encode(order_status_protobuf_object, order_status_object: "OrderStatus") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the order_status_protobuf_object argument is matched with the instance of this class in the 'order_status_object' argument.

        :param order_status_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param order_status_object: an instance of this class to be encoded in the protocol buffer object.
        """
        order_status_protobuf_object.order_status = order_status_object.value

    @classmethod
    def decode(cls, order_status_protobuf_object) -> "OrderStatus":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'order_status_protobuf_object' argument.

        :param order_status_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'order_status_protobuf_object' argument.
        """
        enum_value_from_pb2 = order_status_protobuf_object.order_status
        return cls(enum_value_from_pb2)

    def __eq__(self, other):
        return self.status == other.status  # noqa: E1101


class OrderType(Enum):
    """This class represents an instance of OrderType."""

    LIMIT = 0
    MARKET = 1

    @staticmethod
    def encode(order_type_protobuf_object, order_type_object: "OrderType") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the order_type_protobuf_object argument is matched with the instance of this class in the 'order_type_object' argument.

        :param order_type_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param order_type_object: an instance of this class to be encoded in the protocol buffer object.
        """
        order_type_protobuf_object.order_type = order_type_object.value

    @classmethod
    def decode(cls, order_type_protobuf_object) -> "OrderType":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'order_type_protobuf_object' argument.

        :param order_type_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'order_type_protobuf_object' argument.
        """
        enum_value_from_pb2 = order_type_protobuf_object.order_type
        return cls(enum_value_from_pb2)

    def __eq__(self, other):
        return self.order_type == other.order_type  # noqa: E1101


@dataclass
class Order:
    """This class represents an instance of Orders."""

    id: Optional[str] = None
    exchange_id: Optional[str] = None
    client_order_id: Optional[str] = None
    timestamp: Optional[float] = None
    datetime: Optional[str] = None
    last_trade_timestamp: Optional[float] = None
    status: Optional[OrderStatus] = None
    symbol: Optional[str] = None
    type: Optional[OrderType] = None
    time_in_force: Optional[str] = None
    post_only: Optional[bool] = None
    side: Optional[OrderSide] = None
    price: Optional[float] = None
    stop_price: Optional[float] = None
    trigger_price: Optional[float] = None
    cost: Optional[float] = None
    amount: Optional[float] = None
    filled: Optional[float] = None
    remaining: Optional[float] = None
    fee: Optional[float] = None
    average: Optional[float] = None
    trades: Optional[str] = None
    fees: Optional[str] = None
    last_update_timestamp: Optional[float] = None
    reduce_only: Optional[bool] = None
    take_profit_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    data: Optional[str] = None

    @staticmethod
    def encode(orders_protobuf_object, orders_object: "Order") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the orders_protobuf_object argument is matched with the instance of this class in the 'orders_object' argument.

        :param orders_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param orders_object: an instance of this class to be encoded in the protocol buffer object.
        """
        for attribute in Order.__dataclass_fields__.keys():  # pylint: disable=no-member
            if hasattr(orders_object, attribute):
                attribute_value = getattr(orders_object, attribute)
                if attribute_value is not None:
                    setattr(orders_protobuf_object.Order, attribute, attribute_value)
                else:
                    setattr(orders_protobuf_object.Order, attribute, None)

    @classmethod
    def decode(cls, orders_protobuf_object) -> "Order":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'orders_protobuf_object' argument.

        :param orders_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'orders_protobuf_object' argument.
        """
        orders_object = {}
        for attribute in Order.__dataclass_fields__.keys():  # pylint: disable=no-member
            if hasattr(orders_protobuf_object.Order, attribute):
                attribute_value = getattr(orders_protobuf_object.Order, attribute)
                if attribute_value is not None:
                    orders_object[attribute] = attribute_value
        return cls(**orders_object)

    def __eq__(self, other):
        if isinstance(other, Order):
            return self.__dict__ == other.__dict__
        return False

    def update(self, new):
        """Update the order with new values."""
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def as_json(self):
        """Convert the order to a json compatible object, converting the enums to their names."""
        json_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Enum):
                json_dict[key] = value.name
            else:
                json_dict[key] = value
        return json_dict


@dataclass
class Orders:
    """
    This class represents an instance of Markets.
    """

    orders: List[Order]

    @staticmethod
    def encode(orders_protobuf_object, orders_object: "Orders") -> None:
        """
        Encode an instance of this class into the protocol buffer object.
        """
        orders_protobuf_object.Orders.orders = orders_object.order

    @classmethod
    def decode(cls, orders_protobuf_object) -> "Orders":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.
        """
        return cls(orders_protobuf_object.Orders.orders)

    def __eq__(self, other):
        if isinstance(other, Orders):
            return self.__dict__ == other.__dict__
        return False
