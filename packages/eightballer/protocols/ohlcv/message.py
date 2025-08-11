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

"""This module contains ohlcv's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.ohlcv.custom_types import (
    ErrorCode as CustomErrorCode,
)


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.ohlcv.message")

DEFAULT_BODY_SIZE = 4


class OhlcvMessage(Message):
    """A protocol for passing ohlcv data between compoents."""

    protocol_id = PublicId.from_str("eightballer/ohlcv:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/ohlcv:0.1.0")

    ErrorCode = CustomErrorCode

    class Performative(Message.Performative):
        """Performatives for the ohlcv protocol."""

        CANDLESTICK = "candlestick"
        END = "end"
        ERROR = "error"
        HISTORY = "history"
        SUBSCRIBE = "subscribe"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"candlestick", "end", "error", "history", "subscribe"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "close",
            "dialogue_reference",
            "end_timestamp",
            "error_code",
            "error_data",
            "error_msg",
            "exchange_id",
            "high",
            "interval",
            "low",
            "market_name",
            "message_id",
            "open",
            "performative",
            "start_timestamp",
            "target",
            "timestamp",
            "volume",
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
        Initialise an instance of OhlcvMessage.

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
            performative=OhlcvMessage.Performative(performative),
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
        return cast(OhlcvMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def close(self) -> float:
        """Get the 'close' content from the message."""
        enforce(self.is_set("close"), "'close' content is not set.")
        return cast(float, self.get("close"))

    @property
    def end_timestamp(self) -> int:
        """Get the 'end_timestamp' content from the message."""
        enforce(self.is_set("end_timestamp"), "'end_timestamp' content is not set.")
        return cast(int, self.get("end_timestamp"))

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
    def high(self) -> float:
        """Get the 'high' content from the message."""
        enforce(self.is_set("high"), "'high' content is not set.")
        return cast(float, self.get("high"))

    @property
    def interval(self) -> int:
        """Get the 'interval' content from the message."""
        enforce(self.is_set("interval"), "'interval' content is not set.")
        return cast(int, self.get("interval"))

    @property
    def low(self) -> float:
        """Get the 'low' content from the message."""
        enforce(self.is_set("low"), "'low' content is not set.")
        return cast(float, self.get("low"))

    @property
    def market_name(self) -> str:
        """Get the 'market_name' content from the message."""
        enforce(self.is_set("market_name"), "'market_name' content is not set.")
        return cast(str, self.get("market_name"))

    @property
    def open(self) -> float:
        """Get the 'open' content from the message."""
        enforce(self.is_set("open"), "'open' content is not set.")
        return cast(float, self.get("open"))

    @property
    def start_timestamp(self) -> int:
        """Get the 'start_timestamp' content from the message."""
        enforce(self.is_set("start_timestamp"), "'start_timestamp' content is not set.")
        return cast(int, self.get("start_timestamp"))

    @property
    def timestamp(self) -> int:
        """Get the 'timestamp' content from the message."""
        enforce(self.is_set("timestamp"), "'timestamp' content is not set.")
        return cast(int, self.get("timestamp"))

    @property
    def volume(self) -> float:
        """Get the 'volume' content from the message."""
        enforce(self.is_set("volume"), "'volume' content is not set.")
        return cast(float, self.get("volume"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the ohlcv protocol."""
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
                isinstance(self.performative, OhlcvMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == OhlcvMessage.Performative.SUBSCRIBE:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                enforce(
                    isinstance(self.market_name, str),
                    "Invalid type for content 'market_name'. Expected 'str'. Found '{}'.".format(
                        type(self.market_name)
                    ),
                )
                enforce(
                    type(self.interval) is int,
                    "Invalid type for content 'interval'. Expected 'int'. Found '{}'.".format(type(self.interval)),
                )
            elif self.performative == OhlcvMessage.Performative.CANDLESTICK:
                expected_nb_of_contents = 9
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                enforce(
                    isinstance(self.market_name, str),
                    "Invalid type for content 'market_name'. Expected 'str'. Found '{}'.".format(
                        type(self.market_name)
                    ),
                )
                enforce(
                    type(self.interval) is int,
                    "Invalid type for content 'interval'. Expected 'int'. Found '{}'.".format(type(self.interval)),
                )
                enforce(
                    isinstance(self.open, float),
                    "Invalid type for content 'open'. Expected 'float'. Found '{}'.".format(type(self.open)),
                )
                enforce(
                    isinstance(self.high, float),
                    "Invalid type for content 'high'. Expected 'float'. Found '{}'.".format(type(self.high)),
                )
                enforce(
                    isinstance(self.low, float),
                    "Invalid type for content 'low'. Expected 'float'. Found '{}'.".format(type(self.low)),
                )
                enforce(
                    isinstance(self.close, float),
                    "Invalid type for content 'close'. Expected 'float'. Found '{}'.".format(type(self.close)),
                )
                enforce(
                    isinstance(self.volume, float),
                    "Invalid type for content 'volume'. Expected 'float'. Found '{}'.".format(type(self.volume)),
                )
                enforce(
                    type(self.timestamp) is int,
                    "Invalid type for content 'timestamp'. Expected 'int'. Found '{}'.".format(type(self.timestamp)),
                )
            elif self.performative == OhlcvMessage.Performative.HISTORY:
                expected_nb_of_contents = 5
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                enforce(
                    isinstance(self.market_name, str),
                    "Invalid type for content 'market_name'. Expected 'str'. Found '{}'.".format(
                        type(self.market_name)
                    ),
                )
                enforce(
                    type(self.start_timestamp) is int,
                    "Invalid type for content 'start_timestamp'. Expected 'int'. Found '{}'.".format(
                        type(self.start_timestamp)
                    ),
                )
                enforce(
                    type(self.end_timestamp) is int,
                    "Invalid type for content 'end_timestamp'. Expected 'int'. Found '{}'.".format(
                        type(self.end_timestamp)
                    ),
                )
                enforce(
                    type(self.interval) is int,
                    "Invalid type for content 'interval'. Expected 'int'. Found '{}'.".format(type(self.interval)),
                )
            elif self.performative == OhlcvMessage.Performative.ERROR:
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
            elif self.performative == OhlcvMessage.Performative.END:
                expected_nb_of_contents = 0

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
