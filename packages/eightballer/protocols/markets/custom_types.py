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
# pylint: disable=C0103,R0902,C0301,R1735

"""This module contains class representations corresponding to every custom type in the protocol specification."""


from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNSUPPORTED_PROTOCOL = 0
    DECODING_ERROR = 1
    INVALID_MESSAGE = 2
    UNSUPPORTED_SKILL = 3
    INVALID_DIALOGUE = 4

    @staticmethod
    def encode(error_code_protobuf_object: Any, error_code_object: "ErrorCode") -> None:
        """
        Encode an instance of this class into the protocol buffer object.
        The protocol buffer object in the error_code_protobuf_object argument is matched with the instance of this class in the 'error_code_object' argument.
        :param error_code_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param error_code_object: an instance of this class to be encoded in the protocol buffer object.
        """
        error_code_protobuf_object.error_code = error_code_object.value

    @classmethod
    def decode(cls, error_code_protobuf_object: Any) -> "ErrorCode":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.
        A new instance of this class is created that matches the protocol buffer object in the 'error_code_protobuf_object' argument.
        :param error_code_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'error_code_protobuf_object' argument.
        """
        enum_value_from_pb2 = error_code_protobuf_object.error_code
        return ErrorCode(enum_value_from_pb2)


@dataclass
class Market:
    """
    This class represents an instance of Market.
    """

    id: str
    lowercaseId: Optional[str] = None
    symbol: Optional[str] = None
    base: Optional[str] = None
    quote: Optional[str] = None
    settle: Optional[str] = None
    baseId: Optional[str] = None
    quoteId: Optional[str] = None
    settleId: Optional[str] = None
    type: Optional[str] = None
    spot: Optional[bool] = None
    margin: Optional[bool] = None
    swap: Optional[bool] = None
    future: Optional[bool] = None
    option: Optional[bool] = None
    active: Optional[bool] = None
    contract: Optional[bool] = None
    linear: Optional[bool] = None
    inverse: Optional[bool] = None
    taker: Optional[float] = None
    maker: Optional[float] = None
    contractSize: Optional[float] = None
    expiry: Optional[float] = None
    expiryDatetime: Optional[str] = None
    strike: Optional[float] = None
    optionType: Optional[str] = None
    precision: Optional[float] = None
    limits: Optional[str] = None
    info: Optional[Dict[str, Any]] = None
    exchange_id: Optional[str] = None
    created: Optional[str] = None

    @staticmethod
    def encode(market_protobuf_object, market_object: "Market") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the market_protobuf_object argument is matched with the instance of this class in the 'market_object' argument.

        :param market_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param market_object: an instance of this class to be encoded in the protocol buffer object.
        """
        for attribute in Market.__dataclass_fields__.keys():  # pylint: disable=no-member
            if hasattr(market_object, attribute):
                value = getattr(market_object, attribute)
                setattr(market_protobuf_object.Market, attribute, value)
            else:
                setattr(market_protobuf_object.Market, attribute, None)

    @classmethod
    def decode(cls, market_protobuf_object) -> "Market":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'market_protobuf_object' argument.

        :param market_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'market_protobuf_object' argument.
        """
        attribute_dict = dict()
        for attribute in Market.__dataclass_fields__.keys():  # pylint: disable=no-member
            if hasattr(market_protobuf_object.Market, attribute):
                if getattr(market_protobuf_object.Market, attribute) is not None:
                    attribute_dict[attribute] = getattr(market_protobuf_object.Market, attribute)
        return cls(**attribute_dict)

    def __eq__(self, other):
        if isinstance(other, Market):
            set_of_self_attributue = set(
                i
                for i in Market.__dataclass_fields__.keys()  # pylint: disable=no-member
                if getattr(self, i) is not None
            )
            set_of_other_attributue = set(
                i
                for i in Market.__dataclass_fields__.keys()  # pylint: disable=no-member
                if getattr(other, i) is not None
            )
            return set_of_self_attributue == set_of_other_attributue
        return False

    def to_json(self):
        """TO a pretty dictionary string."""
        result = {}
        for attribute in Market.__dataclass_fields__.keys():  # pylint: disable=no-member
            if hasattr(self, attribute):
                value = getattr(self, attribute)
                if value is not None:
                    result[attribute] = value
        return result


@dataclass
class Markets:
    """This class represents an instance of Markets."""

    markets: List[Market]

    @staticmethod
    def encode(markets_protobuf_object, markets_object: "Markets") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the markets_protobuf_object argument is matched with the instance of this class in the 'markets_object' argument.

        :param markets_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param markets_object: an instance of this class to be encoded in the protocol buffer object.
        """
        if markets_protobuf_object is None:
            raise ValueError("The protocol buffer object 'markets_protobuf_object' is not initialized.")
        markets_protobuf_object.Markets.markets = markets_object.markets

    @classmethod
    def decode(cls, markets_protobuf_object) -> "Markets":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'markets_protobuf_object' argument.

        :param markets_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'markets_protobuf_object' argument.
        """
        return cls(markets_protobuf_object.Markets.markets)

    def __eq__(self, other):
        if isinstance(other, Markets):
            set_of_self_attributue = set(
                i
                for i in Markets.__dataclass_fields__.keys()  # pylint: disable=no-member
                if getattr(self, i) is not None
            )
            set_of_other_attributue = set(
                i
                for i in Markets.__dataclass_fields__.keys()  # pylint: disable=no-member
                if getattr(other, i) is not None
            )
            return set_of_self_attributue == set_of_other_attributue
        return False
