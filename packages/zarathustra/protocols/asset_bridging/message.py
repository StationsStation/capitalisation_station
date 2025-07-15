# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2025 zarathustra
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

"""This module contains asset_bridging's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.zarathustra.protocols.asset_bridging.custom_types import (
    BridgeRequest as CustomBridgeRequest,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    BridgeResult as CustomBridgeResult,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    ErrorInfo as CustomErrorInfo,
)


_default_logger = logging.getLogger("aea.packages.zarathustra.protocols.asset_bridging.message")

DEFAULT_BODY_SIZE = 4


class AssetBridgingMessage(Message):
    """A minimal, atomic request-response protocol for cross-chain asset bridging."""

    protocol_id = PublicId.from_str("zarathustra/asset_bridging:0.1.0")
    protocol_specification_id = PublicId.from_str("zarathustra/asset_bridging:0.1.0")

    BridgeRequest = CustomBridgeRequest

    BridgeResult = CustomBridgeResult

    ErrorInfo = CustomErrorInfo

    class Performative(Message.Performative):
        """Performatives for the asset_bridging protocol."""

        BRIDGE_STATUS = "bridge_status"
        ERROR = "error"
        REQUEST_BRIDGE = "request_bridge"
        REQUEST_STATUS = "request_status"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"bridge_status", "error", "request_bridge", "request_status"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "dialogue_reference",
            "info",
            "message_id",
            "performative",
            "request",
            "result",
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
        Initialise an instance of AssetBridgingMessage.

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
            performative=AssetBridgingMessage.Performative(performative),
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
        return cast(AssetBridgingMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def info(self) -> CustomErrorInfo:
        """Get the 'info' content from the message."""
        enforce(self.is_set("info"), "'info' content is not set.")
        return cast(CustomErrorInfo, self.get("info"))

    @property
    def request(self) -> CustomBridgeRequest:
        """Get the 'request' content from the message."""
        enforce(self.is_set("request"), "'request' content is not set.")
        return cast(CustomBridgeRequest, self.get("request"))

    @property
    def result(self) -> CustomBridgeResult:
        """Get the 'result' content from the message."""
        enforce(self.is_set("result"), "'result' content is not set.")
        return cast(CustomBridgeResult, self.get("result"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the asset_bridging protocol."""
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
                isinstance(self.performative, AssetBridgingMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == AssetBridgingMessage.Performative.REQUEST_BRIDGE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.request, CustomBridgeRequest),
                    "Invalid type for content 'request'. Expected 'BridgeRequest'. Found '{}'.".format(
                        type(self.request)
                    ),
                )
            elif self.performative == AssetBridgingMessage.Performative.BRIDGE_STATUS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.result, CustomBridgeResult),
                    "Invalid type for content 'result'. Expected 'BridgeResult'. Found '{}'.".format(type(self.result)),
                )
            elif self.performative == AssetBridgingMessage.Performative.REQUEST_STATUS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.result, CustomBridgeResult),
                    "Invalid type for content 'result'. Expected 'BridgeResult'. Found '{}'.".format(type(self.result)),
                )
            elif self.performative == AssetBridgingMessage.Performative.ERROR:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.info, CustomErrorInfo),
                    "Invalid type for content 'info'. Expected 'ErrorInfo'. Found '{}'.".format(type(self.info)),
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
