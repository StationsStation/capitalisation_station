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
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNKNOWN_EXHANGE = 0
    UNKNOWN_POSITION = 1
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


class PositionSide(Enum):
    """Represents the position side."""

    LONG = 0
    SHORT = 1

    @staticmethod
    def encode(position_side_protobuf_object, position_side_object: "PositionSide") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the position_side_protobuf_object argument is matched with the instance of this class in the 'position_side_object' argument.

        :param position_side_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param position_side_object: an instance of this class to be encoded in the protocol buffer object.
        """
        value = position_side_object.value
        position_side_protobuf_object.position_side = value

    @classmethod
    def decode(cls, position_side_protobuf_object) -> "PositionSide":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'position_side_protobuf_object' argument.

        :param position_side_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'position_side_protobuf_object' argument.
        """
        enum_value_from_pb2 = position_side_protobuf_object.position_side
        return PositionSide(enum_value_from_pb2)

    @classmethod
    def from_string(cls, string: str) -> "PositionSide":
        """
        Get the enum value from a string.

        :param string: the string to convert.
        """
        if string == "long":
            return cls.LONG
        if string == "short":
            return cls.SHORT
        raise ValueError(f"String '{string}' does not correspond to any enum value.")


@dataclass
class Position:
    """This class represents an instance of Position.
    message Position {
    string id = 1;
    string symbol = 2;
    int64 timestamp = 3;
    string datetime = 4;
    int64 lastUpdateTimestamp = 5;
    float initialMargin = 6;
    float initialMarginPercentage = 7;
    float maintenanceMargin = 8;
    float maintenanceMarginPercentage = 9;
    float entryPrice = 10;
    float notional = 11;
    float leverage = 12;
    float unrealizedPnl = 13;
    float contracts = 14;
    float contractSize = 15;
    float marginRatio = 16;
    float liquidationPrice = 17;
    float markPrice = 18;
    float lastPrice = 19;
    float collateral = 20;
    string marginMode = 21;
    PositionSide side = 22;
    float percentage = 23;
    }

    """

    id: Optional[str] = None
    symbol: Optional[str] = None
    timestamp: Optional[int] = None
    datetime: Optional[str] = None
    last_update_timestamp: Optional[int] = None
    initial_margin: Optional[float] = None
    initial_margin_percentage: Optional[float] = None
    maintenance_margin: Optional[float] = None
    maintenance_margin_percentage: Optional[float] = None
    entry_price: Optional[float] = None
    notional: Optional[float] = None
    leverage: Optional[float] = None
    unrealized_pnl: Optional[float] = None
    realized_pnl: Optional[float] = None
    contracts: Optional[float] = None
    contract_size: Optional[float] = None
    margin_ratio: Optional[float] = None
    liquidation_price: Optional[float] = None
    mark_price: Optional[float] = None
    last_price: Optional[float] = None
    collateral: Optional[float] = None
    margin_mode: Optional[str] = None
    side: Optional[PositionSide] = None
    size: Optional[float] = None
    percentage: Optional[float] = None
    info: Optional[dict] = None
    exchange_id: Optional[str] = None
    hedged: Optional[bool] = None
    stop_loss_price: Optional[float] = None
    take_profit_price: Optional[float] = None

    @staticmethod
    def encode(position_protobuf_object, position_object: "Position") -> None:
        """Encode an instance of this class into the protocol buffer object."""
        for attribute in Position.__dataclass_fields__.keys():  # pylint: disable=no-member
            attribute_value = getattr(position_object, attribute)
            if attribute_value is not None:
                setattr(position_protobuf_object.Position, attribute, attribute_value)

    @classmethod
    def decode(cls, position_protobuf_object) -> "Position":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class."""
        position_object = cls()
        for attribute in Position.__dataclass_fields__.keys():  # pylint: disable=no-member
            attribute_value = getattr(position_protobuf_object.Position, attribute, None)
            if attribute_value is not None:
                setattr(position_object, attribute, attribute_value)
        return position_object

    def __eq__(self, other):
        if isinstance(other, Position):
            return all(
                getattr(self, field) == getattr(other, field)
                for field in Position.__dataclass_fields__.keys()  # pylint: disable=no-member
                if self and other and getattr(self, field) is not None and getattr(other, field) is not None
            )
        return False

    @classmethod
    def from_api_call(cls, api_call):
        """
        Parse a position from a ccxt api call.
        """

        def _from_camel_case(name):
            return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")

        args = {}
        for key, value in api_call.items():
            new_key = _from_camel_case(key)
            if new_key == "side":
                args["side"] = PositionSide.from_string(value)
            args[new_key] = value
        return cls(**args)

    def as_json(self):
        """
        returns the json representation of the position ensuring to get the correct side
        """
        json = {}
        for key, value in self.__dict__.items():
            json[key] = value
        return json


@dataclass
class Positions:
    """This class represents an instance of Positions."""

    positions: List[Position]

    @staticmethod
    def encode(positions_protobuf_object, positions_object: "Positions") -> None:
        """Encode an instance of this class into the protocol buffer object."""
        if positions_protobuf_object is None:
            raise ValueError("Protobuf object for Positions is None.")
        positions_protobuf_object.Positions.positions = positions_object.positions

    @classmethod
    def decode(cls, positions_protobuf_object) -> "Positions":
        """Decode a protocol buffer object that corresponds with this class into an instance of this class."""
        return cls(positions_protobuf_object.Positions.positions)

    def __eq__(self, other):
        if isinstance(other, Positions):
            return all(
                getattr(self, field) == getattr(other, field)
                for field in Positions.__dataclass_fields__.keys()  # pylint: disable=no-member
                if self and other and getattr(self, field) is not None and getattr(other, field) is not None
            )
        return False
