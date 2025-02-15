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

"""This module contains tickers's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.tickers.custom_types import (
    ErrorCode as CustomErrorCode,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker as CustomTicker
from packages.eightballer.protocols.tickers.custom_types import Tickers as CustomTickers


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.tickers.message")

DEFAULT_BODY_SIZE = 4


class TickersMessage(Message):
    """A protocol for passing ticker data between agent components."""

    protocol_id = PublicId.from_str("eightballer/tickers:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/tickers:0.1.0")

    ErrorCode = CustomErrorCode

    Ticker = CustomTicker

    Tickers = CustomTickers

    class Performative(Message.Performative):
        """Performatives for the tickers protocol."""

        ALL_TICKERS = "all_tickers"
        ERROR = "error"
        GET_ALL_TICKERS = "get_all_tickers"
        GET_TICKER = "get_ticker"
        TICKER = "ticker"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"all_tickers", "error", "get_all_tickers", "get_ticker", "ticker"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "asset_a",
            "asset_b",
            "dialogue_reference",
            "error_code",
            "error_data",
            "error_msg",
            "exchange_id",
            "ledger_id",
            "message_id",
            "params",
            "performative",
            "symbol",
            "target",
            "ticker",
            "tickers",
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
        Initialise an instance of TickersMessage.

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
            performative=TickersMessage.Performative(performative),
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
        return cast(TickersMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def asset_a(self) -> Optional[str]:
        """Get the 'asset_a' content from the message."""
        return cast(Optional[str], self.get("asset_a"))

    @property
    def asset_b(self) -> Optional[str]:
        """Get the 'asset_b' content from the message."""
        return cast(Optional[str], self.get("asset_b"))

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
    def params(self) -> Optional[bytes]:
        """Get the 'params' content from the message."""
        return cast(Optional[bytes], self.get("params"))

    @property
    def symbol(self) -> Optional[str]:
        """Get the 'symbol' content from the message."""
        return cast(Optional[str], self.get("symbol"))

    @property
    def ticker(self) -> CustomTicker:
        """Get the 'ticker' content from the message."""
        enforce(self.is_set("ticker"), "'ticker' content is not set.")
        return cast(CustomTicker, self.get("ticker"))

    @property
    def tickers(self) -> CustomTickers:
        """Get the 'tickers' content from the message."""
        enforce(self.is_set("tickers"), "'tickers' content is not set.")
        return cast(CustomTickers, self.get("tickers"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the tickers protocol."""
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
                isinstance(self.performative, TickersMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == TickersMessage.Performative.GET_ALL_TICKERS:
                expected_nb_of_contents = 0
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
                if self.is_set("params"):
                    expected_nb_of_contents += 1
                    params = cast(bytes, self.params)
                    enforce(
                        isinstance(params, bytes),
                        "Invalid type for content 'params'. Expected 'bytes'. Found '{}'.".format(type(params)),
                    )
            elif self.performative == TickersMessage.Performative.GET_TICKER:
                expected_nb_of_contents = 0
                if self.is_set("symbol"):
                    expected_nb_of_contents += 1
                    symbol = cast(str, self.symbol)
                    enforce(
                        isinstance(symbol, str),
                        "Invalid type for content 'symbol'. Expected 'str'. Found '{}'.".format(type(symbol)),
                    )
                if self.is_set("asset_a"):
                    expected_nb_of_contents += 1
                    asset_a = cast(str, self.asset_a)
                    enforce(
                        isinstance(asset_a, str),
                        "Invalid type for content 'asset_a'. Expected 'str'. Found '{}'.".format(type(asset_a)),
                    )
                if self.is_set("asset_b"):
                    expected_nb_of_contents += 1
                    asset_b = cast(str, self.asset_b)
                    enforce(
                        isinstance(asset_b, str),
                        "Invalid type for content 'asset_b'. Expected 'str'. Found '{}'.".format(type(asset_b)),
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
                if self.is_set("params"):
                    expected_nb_of_contents += 1
                    params = cast(bytes, self.params)
                    enforce(
                        isinstance(params, bytes),
                        "Invalid type for content 'params'. Expected 'bytes'. Found '{}'.".format(type(params)),
                    )
            elif self.performative == TickersMessage.Performative.ALL_TICKERS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.tickers, CustomTickers),
                    "Invalid type for content 'tickers'. Expected 'Tickers'. Found '{}'.".format(type(self.tickers)),
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
            elif self.performative == TickersMessage.Performative.TICKER:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.ticker, CustomTicker),
                    "Invalid type for content 'ticker'. Expected 'Ticker'. Found '{}'.".format(type(self.ticker)),
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
            elif self.performative == TickersMessage.Performative.ERROR:
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
