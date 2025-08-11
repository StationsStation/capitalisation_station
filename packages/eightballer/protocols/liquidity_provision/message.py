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

"""This module contains liquidity_provision's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.liquidity_provision.custom_types import (
    ErrorCode as CustomErrorCode,
)


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.liquidity_provision.message")

DEFAULT_BODY_SIZE = 4


class LiquidityProvisionMessage(Message):
    """This protocol specifies interactions for managing liquidity in DeFi platforms, including adding and removing liquidity, and querying liquidity conditions."""

    protocol_id = PublicId.from_str("eightballer/liquidity_provision:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/liquidity_provision:0.1.0")

    ErrorCode = CustomErrorCode

    class Performative(Message.Performative):
        """Performatives for the liquidity_provision protocol."""

        ADD_LIQUIDITY = "add_liquidity"
        ERROR = "error"
        LIQUIDITY_ADDED = "liquidity_added"
        LIQUIDITY_REMOVED = "liquidity_removed"
        LIQUIDITY_STATUS = "liquidity_status"
        QUERY_LIQUIDITY = "query_liquidity"
        REMOVE_LIQUIDITY = "remove_liquidity"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "add_liquidity",
        "error",
        "liquidity_added",
        "liquidity_removed",
        "liquidity_status",
        "query_liquidity",
        "remove_liquidity",
    }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "amounts",
            "available_tokens",
            "burn_amount",
            "current_liquidity",
            "deadline",
            "description",
            "dialogue_reference",
            "error_code",
            "exchange_id",
            "ledger_id",
            "message_id",
            "min_amounts",
            "min_mint_amount",
            "minted_tokens",
            "performative",
            "pool_id",
            "received_amounts",
            "target",
            "token_ids",
            "user_data",
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
        Initialise an instance of LiquidityProvisionMessage.

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
            performative=LiquidityProvisionMessage.Performative(performative),
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
        return cast(LiquidityProvisionMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def amounts(self) -> Tuple[int, ...]:
        """Get the 'amounts' content from the message."""
        enforce(self.is_set("amounts"), "'amounts' content is not set.")
        return cast(Tuple[int, ...], self.get("amounts"))

    @property
    def available_tokens(self) -> Tuple[int, ...]:
        """Get the 'available_tokens' content from the message."""
        enforce(self.is_set("available_tokens"), "'available_tokens' content is not set.")
        return cast(Tuple[int, ...], self.get("available_tokens"))

    @property
    def burn_amount(self) -> int:
        """Get the 'burn_amount' content from the message."""
        enforce(self.is_set("burn_amount"), "'burn_amount' content is not set.")
        return cast(int, self.get("burn_amount"))

    @property
    def current_liquidity(self) -> int:
        """Get the 'current_liquidity' content from the message."""
        enforce(self.is_set("current_liquidity"), "'current_liquidity' content is not set.")
        return cast(int, self.get("current_liquidity"))

    @property
    def deadline(self) -> int:
        """Get the 'deadline' content from the message."""
        enforce(self.is_set("deadline"), "'deadline' content is not set.")
        return cast(int, self.get("deadline"))

    @property
    def description(self) -> str:
        """Get the 'description' content from the message."""
        enforce(self.is_set("description"), "'description' content is not set.")
        return cast(str, self.get("description"))

    @property
    def error_code(self) -> CustomErrorCode:
        """Get the 'error_code' content from the message."""
        enforce(self.is_set("error_code"), "'error_code' content is not set.")
        return cast(CustomErrorCode, self.get("error_code"))

    @property
    def exchange_id(self) -> str:
        """Get the 'exchange_id' content from the message."""
        enforce(self.is_set("exchange_id"), "'exchange_id' content is not set.")
        return cast(str, self.get("exchange_id"))

    @property
    def ledger_id(self) -> Optional[str]:
        """Get the 'ledger_id' content from the message."""
        return cast(Optional[str], self.get("ledger_id"))

    @property
    def min_amounts(self) -> Tuple[int, ...]:
        """Get the 'min_amounts' content from the message."""
        enforce(self.is_set("min_amounts"), "'min_amounts' content is not set.")
        return cast(Tuple[int, ...], self.get("min_amounts"))

    @property
    def min_mint_amount(self) -> int:
        """Get the 'min_mint_amount' content from the message."""
        enforce(self.is_set("min_mint_amount"), "'min_mint_amount' content is not set.")
        return cast(int, self.get("min_mint_amount"))

    @property
    def minted_tokens(self) -> int:
        """Get the 'minted_tokens' content from the message."""
        enforce(self.is_set("minted_tokens"), "'minted_tokens' content is not set.")
        return cast(int, self.get("minted_tokens"))

    @property
    def pool_id(self) -> str:
        """Get the 'pool_id' content from the message."""
        enforce(self.is_set("pool_id"), "'pool_id' content is not set.")
        return cast(str, self.get("pool_id"))

    @property
    def received_amounts(self) -> Tuple[int, ...]:
        """Get the 'received_amounts' content from the message."""
        enforce(self.is_set("received_amounts"), "'received_amounts' content is not set.")
        return cast(Tuple[int, ...], self.get("received_amounts"))

    @property
    def token_ids(self) -> Tuple[str, ...]:
        """Get the 'token_ids' content from the message."""
        enforce(self.is_set("token_ids"), "'token_ids' content is not set.")
        return cast(Tuple[str, ...], self.get("token_ids"))

    @property
    def user_data(self) -> Optional[bytes]:
        """Get the 'user_data' content from the message."""
        return cast(Optional[bytes], self.get("user_data"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the liquidity_provision protocol."""
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
                isinstance(self.performative, LiquidityProvisionMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == LiquidityProvisionMessage.Performative.ADD_LIQUIDITY:
                expected_nb_of_contents = 6
                enforce(
                    isinstance(self.pool_id, str),
                    "Invalid type for content 'pool_id'. Expected 'str'. Found '{}'.".format(type(self.pool_id)),
                )
                enforce(
                    isinstance(self.token_ids, tuple),
                    "Invalid type for content 'token_ids'. Expected 'tuple'. Found '{}'.".format(type(self.token_ids)),
                )
                enforce(
                    all(isinstance(element, str) for element in self.token_ids),
                    "Invalid type for tuple elements in content 'token_ids'. Expected 'str'.",
                )
                enforce(
                    isinstance(self.amounts, tuple),
                    "Invalid type for content 'amounts'. Expected 'tuple'. Found '{}'.".format(type(self.amounts)),
                )
                enforce(
                    all(type(element) is int for element in self.amounts),
                    "Invalid type for tuple elements in content 'amounts'. Expected 'int'.",
                )
                enforce(
                    type(self.min_mint_amount) is int,
                    "Invalid type for content 'min_mint_amount'. Expected 'int'. Found '{}'.".format(
                        type(self.min_mint_amount)
                    ),
                )
                enforce(
                    type(self.deadline) is int,
                    "Invalid type for content 'deadline'. Expected 'int'. Found '{}'.".format(type(self.deadline)),
                )
                if self.is_set("user_data"):
                    expected_nb_of_contents += 1
                    user_data = cast(bytes, self.user_data)
                    enforce(
                        isinstance(user_data, bytes),
                        "Invalid type for content 'user_data'. Expected 'bytes'. Found '{}'.".format(type(user_data)),
                    )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
            elif self.performative == LiquidityProvisionMessage.Performative.REMOVE_LIQUIDITY:
                expected_nb_of_contents = 6
                enforce(
                    isinstance(self.pool_id, str),
                    "Invalid type for content 'pool_id'. Expected 'str'. Found '{}'.".format(type(self.pool_id)),
                )
                enforce(
                    isinstance(self.token_ids, tuple),
                    "Invalid type for content 'token_ids'. Expected 'tuple'. Found '{}'.".format(type(self.token_ids)),
                )
                enforce(
                    all(isinstance(element, str) for element in self.token_ids),
                    "Invalid type for tuple elements in content 'token_ids'. Expected 'str'.",
                )
                enforce(
                    type(self.burn_amount) is int,
                    "Invalid type for content 'burn_amount'. Expected 'int'. Found '{}'.".format(
                        type(self.burn_amount)
                    ),
                )
                enforce(
                    isinstance(self.min_amounts, tuple),
                    "Invalid type for content 'min_amounts'. Expected 'tuple'. Found '{}'.".format(
                        type(self.min_amounts)
                    ),
                )
                enforce(
                    all(type(element) is int for element in self.min_amounts),
                    "Invalid type for tuple elements in content 'min_amounts'. Expected 'int'.",
                )
                enforce(
                    type(self.deadline) is int,
                    "Invalid type for content 'deadline'. Expected 'int'. Found '{}'.".format(type(self.deadline)),
                )
                if self.is_set("user_data"):
                    expected_nb_of_contents += 1
                    user_data = cast(bytes, self.user_data)
                    enforce(
                        isinstance(user_data, bytes),
                        "Invalid type for content 'user_data'. Expected 'bytes'. Found '{}'.".format(type(user_data)),
                    )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
            elif self.performative == LiquidityProvisionMessage.Performative.QUERY_LIQUIDITY:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.pool_id, str),
                    "Invalid type for content 'pool_id'. Expected 'str'. Found '{}'.".format(type(self.pool_id)),
                )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
                if self.is_set("ledger_id"):
                    expected_nb_of_contents += 1
                    ledger_id = cast(str, self.ledger_id)
                    enforce(
                        isinstance(ledger_id, str),
                        "Invalid type for content 'ledger_id'. Expected 'str'. Found '{}'.".format(type(ledger_id)),
                    )
            elif self.performative == LiquidityProvisionMessage.Performative.LIQUIDITY_ADDED:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.pool_id, str),
                    "Invalid type for content 'pool_id'. Expected 'str'. Found '{}'.".format(type(self.pool_id)),
                )
                enforce(
                    type(self.minted_tokens) is int,
                    "Invalid type for content 'minted_tokens'. Expected 'int'. Found '{}'.".format(
                        type(self.minted_tokens)
                    ),
                )
            elif self.performative == LiquidityProvisionMessage.Performative.LIQUIDITY_REMOVED:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.pool_id, str),
                    "Invalid type for content 'pool_id'. Expected 'str'. Found '{}'.".format(type(self.pool_id)),
                )
                enforce(
                    isinstance(self.received_amounts, tuple),
                    "Invalid type for content 'received_amounts'. Expected 'tuple'. Found '{}'.".format(
                        type(self.received_amounts)
                    ),
                )
                enforce(
                    all(type(element) is int for element in self.received_amounts),
                    "Invalid type for tuple elements in content 'received_amounts'. Expected 'int'.",
                )
            elif self.performative == LiquidityProvisionMessage.Performative.LIQUIDITY_STATUS:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.pool_id, str),
                    "Invalid type for content 'pool_id'. Expected 'str'. Found '{}'.".format(type(self.pool_id)),
                )
                enforce(
                    type(self.current_liquidity) is int,
                    "Invalid type for content 'current_liquidity'. Expected 'int'. Found '{}'.".format(
                        type(self.current_liquidity)
                    ),
                )
                enforce(
                    isinstance(self.available_tokens, tuple),
                    "Invalid type for content 'available_tokens'. Expected 'tuple'. Found '{}'.".format(
                        type(self.available_tokens)
                    ),
                )
                enforce(
                    all(type(element) is int for element in self.available_tokens),
                    "Invalid type for tuple elements in content 'available_tokens'. Expected 'int'.",
                )
            elif self.performative == LiquidityProvisionMessage.Performative.ERROR:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.error_code, CustomErrorCode),
                    "Invalid type for content 'error_code'. Expected 'ErrorCode'. Found '{}'.".format(
                        type(self.error_code)
                    ),
                )
                enforce(
                    isinstance(self.description, str),
                    "Invalid type for content 'description'. Expected 'str'. Found '{}'.".format(
                        type(self.description)
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
