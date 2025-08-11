# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""This module contains the transaction payloads of the DexDataRetrieval."""

from dataclasses import dataclass

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload


@dataclass(frozen=True)
class FetchDexBalancesPayload(BaseTxPayload):
    """Represent a transaction payload for the FetchDexBalancesRound."""

    balances: dict


@dataclass(frozen=True)
class FetchDexMarketsPayload(BaseTxPayload):
    """Represent a transaction payload for the FetchDexMarketsRound."""

    markets: dict


@dataclass(frozen=True)
class FetchDexOrdersPayload(BaseTxPayload):
    """Represent a transaction payload for the FetchDexOrdersRound."""

    orders: dict


@dataclass(frozen=True)
class FetchDexPositionsPayload(BaseTxPayload):
    """Represent a transaction payload for the FetchDexPositionsRound."""

    positions: dict


@dataclass(frozen=True)
class FetchDexTickersPayload(BaseTxPayload):
    """Represent a transaction payload for the FetchDexTickersRound."""

    tickers: dict
