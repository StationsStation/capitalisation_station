# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
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
from typing import List


@dataclass
class OrderBook:
    """This class represents an instance of OrderBook."""

    exchange_id: str = None
    symbol: str = None
    asks: List[List[float]] = None
    bids: List[List[float]] = None
    timestamp: int = None
    nonce: int = None
    datetime: str = None

    @staticmethod
    def encode(order_book_protobuf_object, order_book_object: "OrderBook") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the order_book_protobuf_object argument is matched with the instance of this class in the 'order_book_object' argument.

        :param order_book_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param order_book_object: an instance of this class to be encoded in the protocol buffer object.
        """
        order_book_protobuf_object.exchange_id = order_book_object.exchange_id
        order_book_protobuf_object.symbol = order_book_object.symbol
        order_book_protobuf_object.asks = order_book_object.asks
        order_book_protobuf_object.bids = order_book_object.bids
        order_book_protobuf_object.timestamp = order_book_object.timestamp
        order_book_protobuf_object.nonce = order_book_object.nonce
        order_book_protobuf_object.datetime = order_book_object.datetime

    @classmethod
    def decode(cls, order_book_protobuf_object) -> "OrderBook":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the 'order_book_protobuf_object' argument.

        :param order_book_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the 'order_book_protobuf_object' argument.
        """
        order_book = cls()
        order_book.exchange_id = order_book_protobuf_object.exchange_id
        order_book.symbol = order_book_protobuf_object.symbol
        order_book.asks = order_book_protobuf_object.asks
        order_book.bids = order_book_protobuf_object.bids
        order_book.timestamp = order_book_protobuf_object.timestamp
        order_book.nonce = order_book_protobuf_object.nonce
        order_book.datetime = order_book_protobuf_object.datetime
        return order_book

    def __eq__(self, other):
        return (
            self.exchange_id == other.exchange_id
            and self.symbol == other.symbol
            and self.asks == other.asks
            and self.bids == other.bids
            and self.timestamp == other.timestamp
            and self.nonce == other.nonce
        )
