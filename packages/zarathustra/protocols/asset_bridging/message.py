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
from typing import Any, Dict, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.zarathustra.protocols.asset_bridging.custom_types import (
    BridgeStatus as CustomBridgeStatus,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    ErrorCode as CustomErrorCode,
)


_default_logger = logging.getLogger("aea.packages.zarathustra.protocols.asset_bridging.message")

DEFAULT_BODY_SIZE = 4


class AssetBridgingMessage(Message):
    """A minimal, atomic request-response protocol for cross‑chain asset bridging."""

    protocol_id = PublicId.from_str("zarathustra/asset_bridging:0.0.1")
    protocol_specification_id = PublicId.from_str("zarathustra/asset_bridging:0.0.1")

    BridgeStatus = CustomBridgeStatus

    ErrorCode = CustomErrorCode

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
            "amount",
            "bridge",
            "code",
            "dialogue_reference",
            "kwargs",
            "message",
            "message_id",
            "performative",
            "receiver",
            "source_chain",
            "source_token",
            "status",
            "target",
            "target_chain",
            "target_token",
            "tx_hash",
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
    def amount(self) -> int:
        """Get the 'amount' content from the message."""
        enforce(self.is_set("amount"), "'amount' content is not set.")
        return cast(int, self.get("amount"))

    @property
    def bridge(self) -> str:
        """Get the 'bridge' content from the message."""
        enforce(self.is_set("bridge"), "'bridge' content is not set.")
        return cast(str, self.get("bridge"))

    @property
    def code(self) -> CustomErrorCode:
        """Get the 'code' content from the message."""
        enforce(self.is_set("code"), "'code' content is not set.")
        return cast(CustomErrorCode, self.get("code"))

    @property
    def kwargs(self) -> Optional[Dict[str, str]]:
        """Get the 'kwargs' content from the message."""
        return cast(Optional[Dict[str, str]], self.get("kwargs"))

    @property
    def message(self) -> str:
        """Get the 'message' content from the message."""
        enforce(self.is_set("message"), "'message' content is not set.")
        return cast(str, self.get("message"))

    @property
    def receiver(self) -> Optional[str]:
        """Get the 'receiver' content from the message."""
        return cast(Optional[str], self.get("receiver"))

    @property
    def source_chain(self) -> str:
        """Get the 'source_chain' content from the message."""
        enforce(self.is_set("source_chain"), "'source_chain' content is not set.")
        return cast(str, self.get("source_chain"))

    @property
    def source_token(self) -> str:
        """Get the 'source_token' content from the message."""
        enforce(self.is_set("source_token"), "'source_token' content is not set.")
        return cast(str, self.get("source_token"))

    @property
    def status(self) -> CustomBridgeStatus:
        """Get the 'status' content from the message."""
        enforce(self.is_set("status"), "'status' content is not set.")
        return cast(CustomBridgeStatus, self.get("status"))

    @property
    def target_chain(self) -> str:
        """Get the 'target_chain' content from the message."""
        enforce(self.is_set("target_chain"), "'target_chain' content is not set.")
        return cast(str, self.get("target_chain"))

    @property
    def target_token(self) -> Optional[str]:
        """Get the 'target_token' content from the message."""
        return cast(Optional[str], self.get("target_token"))

    @property
    def tx_hash(self) -> str:
        """Get the 'tx_hash' content from the message."""
        enforce(self.is_set("tx_hash"), "'tx_hash' content is not set.")
        return cast(str, self.get("tx_hash"))

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
                expected_nb_of_contents = 5
                enforce(
                    isinstance(self.source_chain, str),
                    "Invalid type for content 'source_chain'. Expected 'str'. Found '{}'.".format(
                        type(self.source_chain)
                    ),
                )
                enforce(
                    isinstance(self.target_chain, str),
                    "Invalid type for content 'target_chain'. Expected 'str'. Found '{}'.".format(
                        type(self.target_chain)
                    ),
                )
                enforce(
                    isinstance(self.source_token, str),
                    "Invalid type for content 'source_token'. Expected 'str'. Found '{}'.".format(
                        type(self.source_token)
                    ),
                )
                if self.is_set("target_token"):
                    expected_nb_of_contents += 1
                    target_token = cast(str, self.target_token)
                    enforce(
                        isinstance(target_token, str),
                        "Invalid type for content 'target_token'. Expected 'str'. Found '{}'.".format(
                            type(target_token)
                        ),
                    )
                enforce(
                    type(self.amount) is int,
                    "Invalid type for content 'amount'. Expected 'int'. Found '{}'.".format(type(self.amount)),
                )
                enforce(
                    isinstance(self.bridge, str),
                    "Invalid type for content 'bridge'. Expected 'str'. Found '{}'.".format(type(self.bridge)),
                )
                if self.is_set("receiver"):
                    expected_nb_of_contents += 1
                    receiver = cast(str, self.receiver)
                    enforce(
                        isinstance(receiver, str),
                        "Invalid type for content 'receiver'. Expected 'str'. Found '{}'.".format(type(receiver)),
                    )
                if self.is_set("kwargs"):
                    expected_nb_of_contents += 1
                    kwargs = cast(Dict[str, str], self.kwargs)
                    enforce(
                        isinstance(kwargs, dict),
                        "Invalid type for content 'kwargs'. Expected 'dict'. Found '{}'.".format(type(kwargs)),
                    )
                    for key_of_kwargs, value_of_kwargs in kwargs.items():
                        enforce(
                            isinstance(key_of_kwargs, str),
                            "Invalid type for dictionary keys in content 'kwargs'. Expected 'str'. Found '{}'.".format(
                                type(key_of_kwargs)
                            ),
                        )
                        enforce(
                            isinstance(value_of_kwargs, str),
                            "Invalid type for dictionary values in content 'kwargs'. Expected 'str'. Found '{}'.".format(
                                type(value_of_kwargs)
                            ),
                        )
            elif self.performative == AssetBridgingMessage.Performative.BRIDGE_STATUS:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.status, CustomBridgeStatus),
                    "Invalid type for content 'status'. Expected 'BridgeStatus'. Found '{}'.".format(type(self.status)),
                )
                enforce(
                    isinstance(self.tx_hash, str),
                    "Invalid type for content 'tx_hash'. Expected 'str'. Found '{}'.".format(type(self.tx_hash)),
                )
            elif self.performative == AssetBridgingMessage.Performative.REQUEST_STATUS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.tx_hash, str),
                    "Invalid type for content 'tx_hash'. Expected 'str'. Found '{}'.".format(type(self.tx_hash)),
                )
            elif self.performative == AssetBridgingMessage.Performative.ERROR:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.code, CustomErrorCode),
                    "Invalid type for content 'code'. Expected 'ErrorCode'. Found '{}'.".format(type(self.code)),
                )
                enforce(
                    isinstance(self.message, str),
                    "Invalid type for content 'message'. Expected 'str'. Found '{}'.".format(type(self.message)),
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
