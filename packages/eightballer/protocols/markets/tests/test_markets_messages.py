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

"""Test messages module for markets protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import List

from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.markets.custom_types import (
    ErrorCode,
    Market,
    Markets,
)
from packages.eightballer.protocols.markets.message import MarketsMessage

TEST_MARKET_CASE = {
    "id": "ETHBTC",
    "lowercaseId": "ethbtc",
    "symbol": "ETH/BTC",
    "base": "ETH",
    "quote": "BTC",
    "settle": None,
    "baseId": "ETH",
    "quoteId": "BTC",
    "settleId": None,
    "type": "spot",
    "spot": True,
    "margin": True,
    "swap": False,
    "future": False,
    "option": False,
    "active": True,
    "contract": False,
    "linear": None,
    "inverse": None,
    "taker": 0.001,
    "maker": 0.001,
    "contractSize": None,
    "expiry": None,
    "expiryDatetime": None,
    "strike": None,
    "optionType": None,
    "precision": {"amount": 4, "price": 5, "base": 8, "quote": 8},
    "limits": {
        "leverage": {"min": None, "max": None},
        "amount": {"min": 0.0001, "max": 100000.0},
        "price": {"min": 1e-05, "max": 922327.0},
        "cost": {"min": 0.0001, "max": 9000000.0},
        "market": {"min": 0.0, "max": 3832.38128875},
    },
    "info": {
        "symbol": "ETHBTC",
        "status": "TRADING",
        "baseAsset": "ETH",
        "baseAssetPrecision": "8",
        "quoteAsset": "BTC",
        "quotePrecision": "8",
        "quoteAssetPrecision": "8",
        "baseCommissionPrecision": "8",
        "quoteCommissionPrecision": "8",
        "orderTypes": [
            "LIMIT",
            "LIMIT_MAKER",
            "MARKET",
            "STOP_LOSS_LIMIT",
            "TAKE_PROFIT_LIMIT",
        ],
        "icebergAllowed": True,
        "ocoAllowed": True,
        "quoteOrderQtyMarketAllowed": True,
        "allowTrailingStop": True,
        "cancelReplaceAllowed": True,
        "isSpotTradingAllowed": True,
        "isMarginTradingAllowed": True,
        "filters": [
            {
                "filterType": "PRICE_FILTER",
                "minPrice": "0.00001000",
                "maxPrice": "922327.00000000",
                "tickSize": "0.00001000",
            },
            {
                "filterType": "LOT_SIZE",
                "minQty": "0.00010000",
                "maxQty": "100000.00000000",
                "stepSize": "0.00010000",
            },
            {"filterType": "ICEBERG_PARTS", "limit": "10"},
            {
                "filterType": "MARKET_LOT_SIZE",
                "minQty": "0.00000000",
                "maxQty": "3832.38128875",
                "stepSize": "0.00000000",
            },
            {
                "filterType": "TRAILING_DELTA",
                "minTrailingAboveDelta": "10",
                "maxTrailingAboveDelta": "2000",
                "minTrailingBelowDelta": "10",
                "maxTrailingBelowDelta": "2000",
            },
            {
                "filterType": "PERCENT_PRICE_BY_SIDE",
                "bidMultiplierUp": "5",
                "bidMultiplierDown": "0.2",
                "askMultiplierUp": "5",
                "askMultiplierDown": "0.2",
                "avgPriceMins": "5",
            },
            {
                "filterType": "NOTIONAL",
                "minNotional": "0.00010000",
                "applyMinToMarket": True,
                "maxNotional": "9000000.00000000",
                "applyMaxToMarket": False,
                "avgPriceMins": "5",
            },
            {"filterType": "MAX_NUM_ORDERS", "maxNumOrders": "200"},
            {"filterType": "MAX_NUM_ALGO_ORDERS", "maxNumAlgoOrders": "5"},
        ],
        "permissions": [
            "SPOT",
            "MARGIN",
            "TRD_GRP_004",
            "TRD_GRP_005",
            "TRD_GRP_006",
            "TRD_GRP_008",
            "TRD_GRP_009",
            "TRD_GRP_010",
            "TRD_GRP_011",
            "TRD_GRP_012",
            "TRD_GRP_013",
        ],
        "defaultSelfTradePreventionMode": "NONE",
        "allowedSelfTradePreventionModes": [
            "NONE",
            "EXPIRE_TAKER",
            "EXPIRE_MAKER",
            "EXPIRE_BOTH",
        ],
    },
}


class TestMessageMarkets(BaseProtocolMessagesTestCase):
    """Test for the 'markets' protocol message."""

    MESSAGE_CLASS = MarketsMessage

    def build_messages(self) -> List[MarketsMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            MarketsMessage(
                performative=MarketsMessage.Performative.GET_ALL_MARKETS,
                exchange_id="some str",
                currency="some str",
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.GET_MARKET,
                id="some str",
                exchange_id="some str",
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.ALL_MARKETS,
                markets=Markets([Market(**TEST_MARKET_CASE)]),  # check it please!
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.MARKET,
                market=Market(**TEST_MARKET_CASE),  # check it please!
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.ERROR,
                error_code=ErrorCode.INVALID_MESSAGE,  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.END,
            ),
        ]

    def build_inconsistent(self) -> List[MarketsMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            MarketsMessage(
                performative=MarketsMessage.Performative.GET_ALL_MARKETS,
                # skip content: exchange_id
                currency="some str",
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.GET_MARKET,
                # skip content: id
                exchange_id="some str",
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.ALL_MARKETS,
                # skip content: markets
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.MARKET,
                # skip content: market
            ),
            MarketsMessage(
                performative=MarketsMessage.Performative.ERROR,
                # skip content: error_code
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]
