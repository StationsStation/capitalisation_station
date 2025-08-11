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

"""This module contains positions's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.positions.custom_types import (
    ErrorCode as CustomErrorCode,
)
from packages.eightballer.protocols.positions.custom_types import (
    Position as CustomPosition,
)
from packages.eightballer.protocols.positions.custom_types import (
    PositionSide as CustomPositionSide,
)
from packages.eightballer.protocols.positions.custom_types import (
    Positions as CustomPositions,
)


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.positions.message")

DEFAULT_BODY_SIZE = 4


class PositionsMessage(Message):
    """A protocol for passing position data between agent components."""

    protocol_id = PublicId.from_str("eightballer/positions:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/positions:0.1.0")

    ErrorCode = CustomErrorCode

    Position = CustomPosition

    PositionSide = CustomPositionSide

    Positions = CustomPositions

    class Performative(Message.Performative):
        """Performatives for the positions protocol."""

        ALL_POSITIONS = "all_positions"
        ERROR = "error"
        GET_ALL_POSITIONS = "get_all_positions"
        GET_POSITION = "get_position"
        POSITION = "position"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"all_positions", "error", "get_all_positions", "get_position", "position"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "dialogue_reference",
            "error_code",
            "error_data",
            "error_msg",
            "exchange_id",
            "message_id",
            "params",
            "performative",
            "position",
            "position_id",
            "positions",
            "side",
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
        Initialise an instance of PositionsMessage.

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
            performative=PositionsMessage.Performative(performative),
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
        return cast(PositionsMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

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
    def params(self) -> Optional[Dict[str, bytes]]:
        """Get the 'params' content from the message."""
        return cast(Optional[Dict[str, bytes]], self.get("params"))

    @property
    def position(self) -> CustomPosition:
        """Get the 'position' content from the message."""
        enforce(self.is_set("position"), "'position' content is not set.")
        return cast(CustomPosition, self.get("position"))

    @property
    def position_id(self) -> str:
        """Get the 'position_id' content from the message."""
        enforce(self.is_set("position_id"), "'position_id' content is not set.")
        return cast(str, self.get("position_id"))

    @property
    def positions(self) -> CustomPositions:
        """Get the 'positions' content from the message."""
        enforce(self.is_set("positions"), "'positions' content is not set.")
        return cast(CustomPositions, self.get("positions"))

    @property
    def side(self) -> Optional[CustomPositionSide]:
        """Get the 'side' content from the message."""
        return cast(Optional[CustomPositionSide], self.get("side"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the positions protocol."""
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
                isinstance(self.performative, PositionsMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == PositionsMessage.Performative.GET_ALL_POSITIONS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                if self.is_set("params"):
                    expected_nb_of_contents += 1
                    params = cast(Dict[str, bytes], self.params)
                    enforce(
                        isinstance(params, dict),
                        "Invalid type for content 'params'. Expected 'dict'. Found '{}'.".format(type(params)),
                    )
                    for key_of_params, value_of_params in params.items():
                        enforce(
                            isinstance(key_of_params, str),
                            "Invalid type for dictionary keys in content 'params'. Expected 'str'. Found '{}'.".format(
                                type(key_of_params)
                            ),
                        )
                        enforce(
                            isinstance(value_of_params, bytes),
                            "Invalid type for dictionary values in content 'params'. Expected 'bytes'. Found '{}'.".format(
                                type(value_of_params)
                            ),
                        )
                if self.is_set("side"):
                    expected_nb_of_contents += 1
                    side = cast(CustomPositionSide, self.side)
                    enforce(
                        isinstance(side, CustomPositionSide),
                        "Invalid type for content 'side'. Expected 'PositionSide'. Found '{}'.".format(type(side)),
                    )
            elif self.performative == PositionsMessage.Performative.GET_POSITION:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.position_id, str),
                    "Invalid type for content 'position_id'. Expected 'str'. Found '{}'.".format(
                        type(self.position_id)
                    ),
                )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
            elif self.performative == PositionsMessage.Performative.ALL_POSITIONS:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.positions, CustomPositions),
                    "Invalid type for content 'positions'. Expected 'Positions'. Found '{}'.".format(
                        type(self.positions)
                    ),
                )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
            elif self.performative == PositionsMessage.Performative.POSITION:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.position, CustomPosition),
                    "Invalid type for content 'position'. Expected 'Position'. Found '{}'.".format(type(self.position)),
                )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
            elif self.performative == PositionsMessage.Performative.ERROR:
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
