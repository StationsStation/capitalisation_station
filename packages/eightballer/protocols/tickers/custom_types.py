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
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ErrorCode(Enum):
    """This class represents an instance of ErrorCode."""

    UNKNOWN_EXCHANGE = 0
    UNKNOWN_TICKER = 1
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
class Ticker:
    """This class represents an instance of Ticker.
       {'symbol': 'ETH/BTC',
    'timestamp': 1689259137293,
    'datetime': '2023-07-13T14:38:57.293Z',
    'high': 0.0619,
    'low': 0.0615,
    'bid': 0.0615,
    'bidVolume': None,
    'ask': 0.0617,
    'askVolume': None,
    'vwap': None,
    'open': None,
    'close': 0.0616,
    'last': 0.0616,
    'previousClose': None,
    'change': None,
    'percentage': None,
    'average': None,
    'baseVolume': None,
    'quoteVolume': 51.5065,
    'info': {'volume_usd': '96891.66',
     'volume_notional': '3.17716209',
     'volume': '51.5065',
     'quote_currency': 'BTC',
     'price_change': '0.0',
     'mid_price': '0.0616',
     'mark_price': '0.061577',
     'low': '0.0615',
     'last': '0.0616',
     'instrument_name': 'ETH_BTC',
     'high': '0.0619',
     'estimated_delivery_price': '0.061577',
     'creation_timestamp': '1689259137293',
     'bid_price': '0.0615',
     'base_currency': 'ETH',
     'ask_price': '0.0617'}}"""

    symbol: Optional[str] = None
    high: Optional[float] = None
    low: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    close: Optional[float] = None
    last: Optional[float] = None
    datetime: Optional[str] = None
    timestamp: Optional[int] = None
    quoteVolume: Optional[float] = None
    info: Optional[dict] = None
    bidVolume: Optional[float] = None
    askVolume: Optional[float] = None
    vwap: Optional[float] = None
    open: Optional[float] = None
    previousClose: Optional[float] = None
    change: Optional[float] = None
    percentage: Optional[float] = None
    average: Optional[float] = None
    baseVolume: Optional[float] = None

    @staticmethod
    def encode(ticker_protobuf_object, ticker_object: "Ticker") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the ticker_protobuf_object argument is matched with the instance of this class in the 'ticker_object' argument.

        :param ticker_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param ticker_object: an instance of this class to be encoded in the protocol buffer object.
        """
        for (
            attribute
        ) in Ticker.__dataclass_fields__.keys():  # pylint: disable=no-member
            attribute_value = getattr(ticker_object, attribute)
            if attribute_value is not None:
                setattr(ticker_protobuf_object.Ticker, attribute, attribute_value)

    @classmethod
    def decode(cls, ticker_protobuf_object) -> "Ticker":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'ticker_protobuf_object' argument.

        :param ticker_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'ticker_protobuf_object' argument.
        """
        params = {}
        for (
            attribute
        ) in Ticker.__dataclass_fields__.keys():  # pylint: disable=no-member
            attribute_value = getattr(ticker_protobuf_object.Ticker, attribute, None)
            if attribute_value is not None:
                params[attribute] = attribute_value
        return cls(**params)

    def __eq__(self, other):
        if isinstance(other, Ticker):
            return all(
                getattr(self, field) == getattr(other, field)
                for field in Ticker.__dataclass_fields__.keys()  # pylint: disable=no-member
                if self
                and other
                and getattr(self, field) is not None
                and getattr(other, field) is not None
            )
        return False

    def as_json(self):
        """
        returns the json representation of the ticker
        """
        json = {}
        for key, value in self.__dict__.items():
            if value is not None:
                json[key] = value
        return json


@dataclass
class Tickers:
    """This class represents an instance of Tickers."""

    tickers: List[Ticker]

    @staticmethod
    def encode(tickers_protobuf_object, tickers_object: "Tickers") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the tickers_protobuf_object argument is matched with the instance of this class in the 'tickers_object' argument.

        :param tickers_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param tickers_object: an instance of this class to be encoded in the protocol buffer object.
        """
        if tickers_object.tickers is None:
            raise ValueError("tickers cannot be None!")
        tickers_protobuf_object.Tickers.tickers = tickers_object.tickers

    @classmethod
    def decode(cls, tickers_protobuf_object) -> "Tickers":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'tickers_protobuf_object' argument.

        :param tickers_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'tickers_protobuf_object' argument.
        """
        return cls(tickers=tickers_protobuf_object.Tickers.tickers)

    def __eq__(self, other):
        if isinstance(other, Tickers):
            return all(
                getattr(self, field) == getattr(other, field)
                for field in Tickers.__dataclass_fields__.keys()  # pylint: disable=no-member
                if self
                and other
                and getattr(self, field) is not None
                and getattr(other, field) is not None
            )
        return False
