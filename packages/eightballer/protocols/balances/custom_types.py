# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
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

"""This module contains class representations corresponding to every custom type in the protocol specification."""
# pylint: disable=C0103,R0902,C0301,R1735

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNKNOWN_EXCHANGE = 0
    UNKNOWN_ASSET = 1
    API_ERROR = 2

    @staticmethod
    def encode(error_code_protobuf_object, error_code_object: "ErrorCode") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the error_code_protobuf_object argument is matched with the instance of this class in the 'error_code_object' argument.

        :param error_code_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param error_code_object: an instance of this class to be encoded in the protocol buffer object.
        """
        error_code_protobuf_object.error_code = error_code_object.value

    @classmethod
    def decode(cls, error_code_protobuf_object) -> "ErrorCode":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'error_code_protobuf_object' argument.

        :param error_code_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'error_code_protobuf_object' argument.
        """
        enum_value_from_pb2 = error_code_protobuf_object.error_code
        return ErrorCode(enum_value_from_pb2)


@dataclass
class Balance:
    """This class represents an instance of Balance."""

    asset_id: str
    free: float
    used: float
    total: float
    exchange_id: Optional[str] = None

    @staticmethod
    def encode(balance_protobuf_object, balance_object: "Balance") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the balance_protobuf_object argument is matched with the instance of this class in the 'balance_object' argument.

        :param balance_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param balance_object: an instance of this class to be encoded in the protocol buffer object.
        """
        balance_protobuf_object.Balance.asset_id = balance_object.asset_id
        balance_protobuf_object.Balance.free = balance_object.free
        balance_protobuf_object.Balance.used = balance_object.used
        balance_protobuf_object.Balance.total = balance_object.total

    @classmethod
    def decode(cls, balance_protobuf_object) -> "Balance":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'balance_protobuf_object' argument.

        :param balance_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'balance_protobuf_object' argument.
        """
        asset_id = balance_protobuf_object.Balance.asset_id
        free = balance_protobuf_object.Balance.free
        used = balance_protobuf_object.Balance.used
        total = balance_protobuf_object.Balance.total
        return Balance(asset_id, free, used, total)

    def __eq__(self, other):
        return (
            isinstance(other, Balance)
            and self.asset_id == other.asset_id
            and self.free == other.free
            and self.used == other.used
            and self.total == other.total
        )

    def as_json(self):
        """Return the json representation."""
        return {
            "asset_id": self.asset_id,
            "free": self.free,
            "used": self.used,
            "total": self.total,
        }


@dataclass
class Balances:
    """This class represents an instance of Balances."""

    balances: List[Balance]

    @staticmethod
    def encode(balances_protobuf_object, balances_object: "Balances") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the balances_protobuf_object argument is matched with the instance of this class in the 'balances_object' argument.

        :param balances_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param balances_object: an instance of this class to be encoded in the protocol buffer object.
        """
        if balances_object is None:
            raise ValueError("balances_object must not be None")
        balances_protobuf_object.Balances.balances = balances_object.balances

    @classmethod
    def decode(cls, balances_protobuf_object) -> "Balances":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'balances_protobuf_object' argument.

        :param balances_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'balances_protobuf_object' argument.
        """
        return cls(balances_protobuf_object.Balances.balances)

    def __eq__(self, other):
        return isinstance(other, Balances) and self.balances == other.balances
