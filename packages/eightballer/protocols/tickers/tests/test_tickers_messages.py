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

"""Test messages module for tickers protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
# pylint: disable=R1735
from typing import List

from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers, ErrorCode


RAW_TICKER = {
    "symbol": "ETH/BTC",
    "timestamp": 1689259137293,
    "datetime": "2023-07-13T14:38:57.293Z",
    "high": 0.0619,
    "low": 0.0615,
    "bid": 0.0615,
    "bidVolume": None,
    "ask": 0.0617,
    "askVolume": None,
    "vwap": None,
    "open": None,
    "close": 0.0616,
    "last": 0.0616,
    "previousClose": None,
    "change": None,
    "percentage": None,
    "average": None,
    "baseVolume": None,
    "quoteVolume": 51.5065,
    "info": {
        "volume_usd": "96891.66",
        "volume_notional": "3.17716209",
        "volume": "51.5065",
        "quote_currency": "BTC",
        "price_change": "0.0",
    },
}


class TestMessageTickers(BaseProtocolMessagesTestCase):
    """Test for the 'tickers' protocol message."""

    MESSAGE_CLASS = TickersMessage

    def build_messages(self) -> List[TickersMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            TickersMessage(
                performative=TickersMessage.Performative.GET_ALL_TICKERS,
                exchange_id="some str",
                params={"some str": b"some_bytes"},
            ),
            TickersMessage(
                performative=TickersMessage.Performative.GET_TICKER,
                asset_id="some str",
                exchange_id="some str",
            ),
            TickersMessage(
                performative=TickersMessage.Performative.ALL_TICKERS,
                tickers=Tickers(tickers=[]),
            ),
            TickersMessage(
                performative=TickersMessage.Performative.TICKER,
                ticker=Ticker(**RAW_TICKER),
            ),
            TickersMessage(
                performative=TickersMessage.Performative.ERROR,
                error_code=ErrorCode.API_ERROR,  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self) -> List[TickersMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            TickersMessage(
                performative=TickersMessage.Performative.GET_ALL_TICKERS,
                # skip content: exchange_id
                params={"some str": b"some_bytes"},
            ),
            TickersMessage(
                performative=TickersMessage.Performative.GET_TICKER,
                # skip content: asset_id
                exchange_id="some str",
            ),
            TickersMessage(
                performative=TickersMessage.Performative.ALL_TICKERS,
                # skip content: tickers
            ),
            TickersMessage(
                performative=TickersMessage.Performative.TICKER,
                # skip content: ticker
            ),
            TickersMessage(
                performative=TickersMessage.Performative.ERROR,
                # skip content: error_code
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]
