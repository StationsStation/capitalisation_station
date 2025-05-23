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

"""This module contains order_book's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.order_book.custom_types import (
    OrderBook as CustomOrderBook,
)


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.order_book.message")

DEFAULT_BODY_SIZE = 4


class OrderBookMessage(Message):
    """A protocol to enable agents to subscribe to order books and receive updates in real-time. This protocol facilitates monitoring changes in bid and ask prices along with their volumes for given trading pairs on specified exchanges."""

    protocol_id = PublicId.from_str("eightballer/order_book:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/order_book:0.1.0")

    OrderBook = CustomOrderBook

    class Performative(Message.Performative):
        """Performatives for the order_book protocol."""

        ERROR = "error"
        ORDER_BOOK_UPDATE = "order_book_update"
        SUBSCRIBE = "subscribe"
        UNSUBSCRIBE = "unsubscribe"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"error", "order_book_update", "subscribe", "unsubscribe"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "dialogue_reference",
            "error_msg",
            "exchange_id",
            "interval",
            "message_id",
            "order_book",
            "performative",
            "precision",
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
        Initialise an instance of OrderBookMessage.

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
            performative=OrderBookMessage.Performative(performative),
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
        return cast(OrderBookMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def error_msg(self) -> str:
        """Get the 'error_msg' content from the message."""
        enforce(self.is_set("error_msg"), "'error_msg' content is not set.")
        return cast(str, self.get("error_msg"))

    @property
    def exchange_id(self) -> str:
        """Get the 'exchange_id' content from the message."""
        enforce(self.is_set("exchange_id"), "'exchange_id' content is not set.")
        return cast(str, self.get("exchange_id"))

    @property
    def interval(self) -> Optional[int]:
        """Get the 'interval' content from the message."""
        return cast(Optional[int], self.get("interval"))

    @property
    def order_book(self) -> CustomOrderBook:
        """Get the 'order_book' content from the message."""
        enforce(self.is_set("order_book"), "'order_book' content is not set.")
        return cast(CustomOrderBook, self.get("order_book"))

    @property
    def precision(self) -> Optional[str]:
        """Get the 'precision' content from the message."""
        return cast(Optional[str], self.get("precision"))

    @property
    def symbol(self) -> str:
        """Get the 'symbol' content from the message."""
        enforce(self.is_set("symbol"), "'symbol' content is not set.")
        return cast(str, self.get("symbol"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the order_book protocol."""
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
                isinstance(self.performative, OrderBookMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == OrderBookMessage.Performative.SUBSCRIBE:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                enforce(
                    isinstance(self.symbol, str),
                    "Invalid type for content 'symbol'. Expected 'str'. Found '{}'.".format(type(self.symbol)),
                )
                if self.is_set("precision"):
                    expected_nb_of_contents += 1
                    precision = cast(str, self.precision)
                    enforce(
                        isinstance(precision, str),
                        "Invalid type for content 'precision'. Expected 'str'. Found '{}'.".format(type(precision)),
                    )
                if self.is_set("interval"):
                    expected_nb_of_contents += 1
                    interval = cast(int, self.interval)
                    enforce(
                        type(interval) is int,
                        "Invalid type for content 'interval'. Expected 'int'. Found '{}'.".format(type(interval)),
                    )
            elif self.performative == OrderBookMessage.Performative.UNSUBSCRIBE:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                enforce(
                    isinstance(self.symbol, str),
                    "Invalid type for content 'symbol'. Expected 'str'. Found '{}'.".format(type(self.symbol)),
                )
            elif self.performative == OrderBookMessage.Performative.ORDER_BOOK_UPDATE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.order_book, CustomOrderBook),
                    "Invalid type for content 'order_book'. Expected 'OrderBook'. Found '{}'.".format(
                        type(self.order_book)
                    ),
                )
            elif self.performative == OrderBookMessage.Performative.ERROR:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.error_msg, str),
                    "Invalid type for content 'error_msg'. Expected 'str'. Found '{}'.".format(type(self.error_msg)),
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
