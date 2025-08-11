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

"""This module contains orders's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.orders.custom_types import (
    ErrorCode as CustomErrorCode,
)
from packages.eightballer.protocols.orders.custom_types import Order as CustomOrder
from packages.eightballer.protocols.orders.custom_types import (
    OrderSide as CustomOrderSide,
)
from packages.eightballer.protocols.orders.custom_types import (
    OrderStatus as CustomOrderStatus,
)
from packages.eightballer.protocols.orders.custom_types import (
    OrderType as CustomOrderType,
)
from packages.eightballer.protocols.orders.custom_types import Orders as CustomOrders


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.orders.message")

DEFAULT_BODY_SIZE = 4


class OrdersMessage(Message):
    """A protocol for representing orders."""

    protocol_id = PublicId.from_str("eightballer/orders:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/orders:0.1.0")

    ErrorCode = CustomErrorCode

    Order = CustomOrder

    OrderSide = CustomOrderSide

    OrderStatus = CustomOrderStatus

    OrderType = CustomOrderType

    Orders = CustomOrders

    class Performative(Message.Performative):
        """Performatives for the orders protocol."""

        CANCEL_ORDER = "cancel_order"
        CREATE_ORDER = "create_order"
        ERROR = "error"
        GET_ORDER = "get_order"
        GET_ORDERS = "get_orders"
        GET_SETTLEMENTS = "get_settlements"
        ORDER = "order"
        ORDER_CANCELLED = "order_cancelled"
        ORDER_CREATED = "order_created"
        ORDERS = "orders"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "cancel_order",
        "create_order",
        "error",
        "get_order",
        "get_orders",
        "get_settlements",
        "order",
        "order_cancelled",
        "order_created",
        "orders",
    }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "account",
            "currency",
            "dialogue_reference",
            "end_timestamp",
            "error_code",
            "error_data",
            "error_msg",
            "exchange_id",
            "ledger_id",
            "message_id",
            "order",
            "order_type",
            "orders",
            "performative",
            "side",
            "start_timestamp",
            "status",
            "symbol",
            "target",
        )

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs: Any,
    ):
        """
        Initialise an instance of OrdersMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        :param **kwargs: extra options.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=OrdersMessage.Performative(performative),
            **kwargs,
        )

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        enforce(self.is_set("dialogue_reference"), "dialogue_reference is not set.")
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        enforce(self.is_set("message_id"), "message_id is not set.")
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        enforce(self.is_set("performative"), "performative is not set.")
        return cast(OrdersMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def account(self) -> Optional[str]:
        """Get the 'account' content from the message."""
        return cast(Optional[str], self.get("account"))

    @property
    def currency(self) -> Optional[str]:
        """Get the 'currency' content from the message."""
        return cast(Optional[str], self.get("currency"))

    @property
    def end_timestamp(self) -> Optional[float]:
        """Get the 'end_timestamp' content from the message."""
        return cast(Optional[float], self.get("end_timestamp"))

    @property
    def error_code(self) -> CustomErrorCode:
        """Get the 'error_code' content from the message."""
        enforce(self.is_set("error_code"), "'error_code' content is not set.")
        return cast(CustomErrorCode, self.get("error_code"))

    @property
    def error_data(self) -> Dict[str, bytes]:
        """Get the 'error_data' content from the message."""
        enforce(self.is_set("error_data"), "'error_data' content is not set.")
        return cast(Dict[str, bytes], self.get("error_data"))

    @property
    def error_msg(self) -> str:
        """Get the 'error_msg' content from the message."""
        enforce(self.is_set("error_msg"), "'error_msg' content is not set.")
        return cast(str, self.get("error_msg"))

    @property
    def exchange_id(self) -> Optional[str]:
        """Get the 'exchange_id' content from the message."""
        return cast(Optional[str], self.get("exchange_id"))

    @property
    def ledger_id(self) -> Optional[str]:
        """Get the 'ledger_id' content from the message."""
        return cast(Optional[str], self.get("ledger_id"))

    @property
    def order(self) -> CustomOrder:
        """Get the 'order' content from the message."""
        enforce(self.is_set("order"), "'order' content is not set.")
        return cast(CustomOrder, self.get("order"))

    @property
    def order_type(self) -> Optional[CustomOrderType]:
        """Get the 'order_type' content from the message."""
        return cast(Optional[CustomOrderType], self.get("order_type"))

    @property
    def orders(self) -> CustomOrders:
        """Get the 'orders' content from the message."""
        enforce(self.is_set("orders"), "'orders' content is not set.")
        return cast(CustomOrders, self.get("orders"))

    @property
    def side(self) -> Optional[CustomOrderSide]:
        """Get the 'side' content from the message."""
        return cast(Optional[CustomOrderSide], self.get("side"))

    @property
    def start_timestamp(self) -> Optional[float]:
        """Get the 'start_timestamp' content from the message."""
        return cast(Optional[float], self.get("start_timestamp"))

    @property
    def status(self) -> Optional[CustomOrderStatus]:
        """Get the 'status' content from the message."""
        return cast(Optional[CustomOrderStatus], self.get("status"))

    @property
    def symbol(self) -> Optional[str]:
        """Get the 'symbol' content from the message."""
        return cast(Optional[str], self.get("symbol"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the orders protocol."""
        try:
            enforce(
                isinstance(self.dialogue_reference, tuple),
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[0], str),
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[1], str),
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) is int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(type(self.message_id)),
            )
            enforce(
                type(self.target) is int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(type(self.target)),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                isinstance(self.performative, OrdersMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == OrdersMessage.Performative.CREATE_ORDER:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.order, CustomOrder),
                    "Invalid type for content 'order'. Expected 'Order'. Found '{}'.".format(type(self.order)),
                )
                if self.is_set("exchange_id"):
                    expected_nb_of_contents += 1
                    exchange_id = cast(str, self.exchange_id)
                    enforce(
                        isinstance(exchange_id, str),
                        "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(type(exchange_id)),
                    )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
            elif self.performative == OrdersMessage.Performative.ORDER_CREATED:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.order, CustomOrder),
                    "Invalid type for content 'order'. Expected 'Order'. Found '{}'.".format(type(self.order)),
                )
            elif self.performative == OrdersMessage.Performative.CANCEL_ORDER:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.order, CustomOrder),
                    "Invalid type for content 'order'. Expected 'Order'. Found '{}'.".format(type(self.order)),
                )
                if self.is_set("exchange_id"):
                    expected_nb_of_contents += 1
                    exchange_id = cast(str, self.exchange_id)
                    enforce(
                        isinstance(exchange_id, str),
                        "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(type(exchange_id)),
                    )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
            elif self.performative == OrdersMessage.Performative.ORDER_CANCELLED:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.order, CustomOrder),
                    "Invalid type for content 'order'. Expected 'Order'. Found '{}'.".format(type(self.order)),
                )
            elif self.performative == OrdersMessage.Performative.GET_ORDERS:
                expected_nb_of_contents = 0
                if self.is_set("symbol"):
                    expected_nb_of_contents += 1
                    symbol = cast(str, self.symbol)
                    enforce(
                        isinstance(symbol, str),
                        "Invalid type for content 'symbol'. Expected 'str'. Found '{}'.".format(type(symbol)),
                    )
                if self.is_set("currency"):
                    expected_nb_of_contents += 1
                    currency = cast(str, self.currency)
                    enforce(
                        isinstance(currency, str),
                        "Invalid type for content 'currency'. Expected 'str'. Found '{}'.".format(type(currency)),
                    )
                if self.is_set("order_type"):
                    expected_nb_of_contents += 1
                    order_type = cast(CustomOrderType, self.order_type)
                    enforce(
                        isinstance(order_type, CustomOrderType),
                        "Invalid type for content 'order_type'. Expected 'OrderType'. Found '{}'.".format(
                            type(order_type)
                        ),
                    )
                if self.is_set("side"):
                    expected_nb_of_contents += 1
                    side = cast(CustomOrderSide, self.side)
                    enforce(
                        isinstance(side, CustomOrderSide),
                        "Invalid type for content 'side'. Expected 'OrderSide'. Found '{}'.".format(type(side)),
                    )
                if self.is_set("status"):
                    expected_nb_of_contents += 1
                    status = cast(CustomOrderStatus, self.status)
                    enforce(
                        isinstance(status, CustomOrderStatus),
                        "Invalid type for content 'status'. Expected 'OrderStatus'. Found '{}'.".format(type(status)),
                    )
                if self.is_set("exchange_id"):
                    expected_nb_of_contents += 1
                    exchange_id = cast(str, self.exchange_id)
                    enforce(
                        isinstance(exchange_id, str),
                        "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(type(exchange_id)),
                    )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
                if self.is_set("account"):
                    expected_nb_of_contents += 1
                    account = cast(str, self.account)
                    enforce(
                        isinstance(account, str),
                        "Invalid type for content 'account'. Expected 'str'. Found '{}'.".format(type(account)),
                    )
            elif self.performative == OrdersMessage.Performative.GET_SETTLEMENTS:
                expected_nb_of_contents = 0
                if self.is_set("currency"):
                    expected_nb_of_contents += 1
                    currency = cast(str, self.currency)
                    enforce(
                        isinstance(currency, str),
                        "Invalid type for content 'currency'. Expected 'str'. Found '{}'.".format(type(currency)),
                    )
                if self.is_set("end_timestamp"):
                    expected_nb_of_contents += 1
                    end_timestamp = cast(float, self.end_timestamp)
                    enforce(
                        isinstance(end_timestamp, float),
                        "Invalid type for content 'end_timestamp'. Expected 'float'. Found '{}'.".format(
                            type(end_timestamp)
                        ),
                    )
                if self.is_set("start_timestamp"):
                    expected_nb_of_contents += 1
                    start_timestamp = cast(float, self.start_timestamp)
                    enforce(
                        isinstance(start_timestamp, float),
                        "Invalid type for content 'start_timestamp'. Expected 'float'. Found '{}'.".format(
                            type(start_timestamp)
                        ),
                    )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
                if self.is_set("exchange_id"):
                    expected_nb_of_contents += 1
                    exchange_id = cast(str, self.exchange_id)
                    enforce(
                        isinstance(exchange_id, str),
                        "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(type(exchange_id)),
                    )
            elif self.performative == OrdersMessage.Performative.GET_ORDER:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.order, CustomOrder),
                    "Invalid type for content 'order'. Expected 'Order'. Found '{}'.".format(type(self.order)),
                )
                if self.is_set("exchange_id"):
                    expected_nb_of_contents += 1
                    exchange_id = cast(str, self.exchange_id)
                    enforce(
                        isinstance(exchange_id, str),
                        "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(type(exchange_id)),
                    )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
            elif self.performative == OrdersMessage.Performative.ORDER:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.order, CustomOrder),
                    "Invalid type for content 'order'. Expected 'Order'. Found '{}'.".format(type(self.order)),
                )
            elif self.performative == OrdersMessage.Performative.ORDERS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.orders, CustomOrders),
                    "Invalid type for content 'orders'. Expected 'Orders'. Found '{}'.".format(type(self.orders)),
                )
            elif self.performative == OrdersMessage.Performative.ERROR:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.error_code, CustomErrorCode),
                    "Invalid type for content 'error_code'. Expected 'ErrorCode'. Found '{}'.".format(
                        type(self.error_code)
                    ),
                )
                enforce(
                    isinstance(self.error_msg, str),
                    "Invalid type for content 'error_msg'. Expected 'str'. Found '{}'.".format(type(self.error_msg)),
                )
                enforce(
                    isinstance(self.error_data, dict),
                    "Invalid type for content 'error_data'. Expected 'dict'. Found '{}'.".format(type(self.error_data)),
                )
                for key_of_error_data, value_of_error_data in self.error_data.items():
                    enforce(
                        isinstance(key_of_error_data, str),
                        "Invalid type for dictionary keys in content 'error_data'. Expected 'str'. Found '{}'.".format(
                            type(key_of_error_data)
                        ),
                    )
                    enforce(
                        isinstance(value_of_error_data, bytes),
                        "Invalid type for dictionary values in content 'error_data'. Expected 'bytes'. Found '{}'.".format(
                            type(value_of_error_data)
                        ),
                    )

            # Check correct content count
            enforce(
                expected_nb_of_contents == actual_nb_of_contents,
                "Incorrect number of contents. Expected {}. Found {}".format(
                    expected_nb_of_contents, actual_nb_of_contents
                ),
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                enforce(
                    self.target == 0,
                    "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(self.target),
                )
        except (AEAEnforceError, ValueError, KeyError) as e:
            _default_logger.error(str(e))
            return False

        return True
