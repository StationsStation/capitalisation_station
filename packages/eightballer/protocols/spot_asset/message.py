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

"""This module contains spot_asset's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.spot_asset.custom_types import (
    Decimal as CustomDecimal,
)
from packages.eightballer.protocols.spot_asset.custom_types import (
    ErrorCode as CustomErrorCode,
)


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.spot_asset.message")

DEFAULT_BODY_SIZE = 4


class SpotAssetMessage(Message):
    """A protocol for representing spot_assets."""

    protocol_id = PublicId.from_str("eightballer/spot_asset:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/spot_asset:0.1.0")

    Decimal = CustomDecimal

    ErrorCode = CustomErrorCode

    class Performative(Message.Performative):
        """Performatives for the spot_asset protocol."""

        END = "end"
        ERROR = "error"
        GET_SPOT_ASSET = "get_spot_asset"
        GET_SPOT_ASSETS = "get_spot_assets"
        SPOT_ASSET = "spot_asset"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"end", "error", "get_spot_asset", "get_spot_assets", "spot_asset"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "available_without_borrow",
            "decimal",
            "dialogue_reference",
            "error_code",
            "error_msg",
            "exchange_id",
            "free",
            "message_id",
            "name",
            "performative",
            "target",
            "total",
            "usd_value",
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
        Initialise an instance of SpotAssetMessage.

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
            performative=SpotAssetMessage.Performative(performative),
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
        return cast(SpotAssetMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def available_without_borrow(self) -> CustomDecimal:
        """Get the 'available_without_borrow' content from the message."""
        enforce(self.is_set("available_without_borrow"), "'available_without_borrow' content is not set.")
        return cast(CustomDecimal, self.get("available_without_borrow"))

    @property
    def decimal(self) -> Optional[CustomDecimal]:
        """Get the 'decimal' content from the message."""
        return cast(Optional[CustomDecimal], self.get("decimal"))

    @property
    def error_code(self) -> CustomErrorCode:
        """Get the 'error_code' content from the message."""
        enforce(self.is_set("error_code"), "'error_code' content is not set.")
        return cast(CustomErrorCode, self.get("error_code"))

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
    def free(self) -> CustomDecimal:
        """Get the 'free' content from the message."""
        enforce(self.is_set("free"), "'free' content is not set.")
        return cast(CustomDecimal, self.get("free"))

    @property
    def name(self) -> str:
        """Get the 'name' content from the message."""
        enforce(self.is_set("name"), "'name' content is not set.")
        return cast(str, self.get("name"))

    @property
    def total(self) -> CustomDecimal:
        """Get the 'total' content from the message."""
        enforce(self.is_set("total"), "'total' content is not set.")
        return cast(CustomDecimal, self.get("total"))

    @property
    def usd_value(self) -> Optional[CustomDecimal]:
        """Get the 'usd_value' content from the message."""
        return cast(Optional[CustomDecimal], self.get("usd_value"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the spot_asset protocol."""
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
                isinstance(self.performative, SpotAssetMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == SpotAssetMessage.Performative.GET_SPOT_ASSET:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.name, str),
                    "Invalid type for content 'name'. Expected 'str'. Found '{}'.".format(type(self.name)),
                )
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
            elif self.performative == SpotAssetMessage.Performative.SPOT_ASSET:
                expected_nb_of_contents = 4
                enforce(
                    isinstance(self.name, str),
                    "Invalid type for content 'name'. Expected 'str'. Found '{}'.".format(type(self.name)),
                )
                enforce(
                    isinstance(self.total, CustomDecimal),
                    "Invalid type for content 'total'. Expected 'Decimal'. Found '{}'.".format(type(self.total)),
                )
                enforce(
                    isinstance(self.free, CustomDecimal),
                    "Invalid type for content 'free'. Expected 'Decimal'. Found '{}'.".format(type(self.free)),
                )
                enforce(
                    isinstance(self.available_without_borrow, CustomDecimal),
                    "Invalid type for content 'available_without_borrow'. Expected 'Decimal'. Found '{}'.".format(
                        type(self.available_without_borrow)
                    ),
                )
                if self.is_set("usd_value"):
                    expected_nb_of_contents += 1
                    usd_value = cast(CustomDecimal, self.usd_value)
                    enforce(
                        isinstance(usd_value, CustomDecimal),
                        "Invalid type for content 'usd_value'. Expected 'Decimal'. Found '{}'.".format(type(usd_value)),
                    )
                if self.is_set("decimal"):
                    expected_nb_of_contents += 1
                    decimal = cast(CustomDecimal, self.decimal)
                    enforce(
                        isinstance(decimal, CustomDecimal),
                        "Invalid type for content 'decimal'. Expected 'Decimal'. Found '{}'.".format(type(decimal)),
                    )
            elif self.performative == SpotAssetMessage.Performative.GET_SPOT_ASSETS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.exchange_id, str),
                    "Invalid type for content 'exchange_id'. Expected 'str'. Found '{}'.".format(
                        type(self.exchange_id)
                    ),
                )
            elif self.performative == SpotAssetMessage.Performative.ERROR:
                expected_nb_of_contents = 2
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
            elif self.performative == SpotAssetMessage.Performative.END:
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
