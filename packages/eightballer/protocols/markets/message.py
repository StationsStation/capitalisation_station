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

"""This module contains markets's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.markets.custom_types import (
    ErrorCode as CustomErrorCode,
)
from packages.eightballer.protocols.markets.custom_types import Market as CustomMarket
from packages.eightballer.protocols.markets.custom_types import Markets as CustomMarkets


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.markets.message")

DEFAULT_BODY_SIZE = 4


class MarketsMessage(Message):
    """A protocol for passing ohlcv data between compoents."""

    protocol_id = PublicId.from_str("eightballer/markets:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/markets:0.1.0")

    ErrorCode = CustomErrorCode

    Market = CustomMarket

    Markets = CustomMarkets

    class Performative(Message.Performative):
        """Performatives for the markets protocol."""

        ALL_MARKETS = "all_markets"
        ERROR = "error"
        GET_ALL_MARKETS = "get_all_markets"
        GET_MARKET = "get_market"
        MARKET = "market"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"all_markets", "error", "get_all_markets", "get_market", "market"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "currency",
            "dialogue_reference",
            "error_code",
            "error_data",
            "error_msg",
            "exchange_id",
            "id",
            "market",
            "markets",
            "message_id",
            "performative",
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
        Initialise an instance of MarketsMessage.

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
            performative=MarketsMessage.Performative(performative),
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
        return cast(MarketsMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def currency(self) -> Optional[str]:
        """Get the 'currency' content from the message."""
        return cast(Optional[str], self.get("currency"))

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
    def exchange_id(self) -> str:
        """Get the 'exchange_id' content from the message."""
        enforce(self.is_set("exchange_id"), "'exchange_id' content is not set.")
        return cast(str, self.get("exchange_id"))

    @property
    def id(self) -> str:
        """Get the 'id' content from the message."""
        enforce(self.is_set("id"), "'id' content is not set.")
        return cast(str, self.get("id"))

    @property
    def market(self) -> CustomMarket:
        """Get the 'market' content from the message."""
        enforce(self.is_set("market"), "'market' content is not set.")
        return cast(CustomMarket, self.get("market"))

    @property
    def markets(self) -> CustomMarkets:
        """Get the 'markets' content from the message."""
        enforce(self.is_set("markets"), "'markets' content is not set.")
        return cast(CustomMarkets, self.get("markets"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the markets protocol."""
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
                isinstance(self.performative, MarketsMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == MarketsMessage.Performative.GET_ALL_MARKETS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                if self.is_set("currency"):
                    expected_nb_of_contents += 1
                    currency = cast(str, self.currency)
                    enforce(
                        isinstance(currency, str),
                        "Invalid type for content 'currency'. Expected 'str'. Found '{}'.".format(type(currency)),
                    )
            elif self.performative == MarketsMessage.Performative.GET_MARKET:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.id, str),
                    "Invalid type for content 'id'. Expected 'str'. Found '{}'.".format(type(self.id)),
                )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
            elif self.performative == MarketsMessage.Performative.ALL_MARKETS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.markets, CustomMarkets),
                    "Invalid type for content 'markets'. Expected 'Markets'. Found '{}'.".format(type(self.markets)),
                )
            elif self.performative == MarketsMessage.Performative.MARKET:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.market, CustomMarket),
                    "Invalid type for content 'market'. Expected 'Market'. Found '{}'.".format(type(self.market)),
                )
            elif self.performative == MarketsMessage.Performative.ERROR:
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
