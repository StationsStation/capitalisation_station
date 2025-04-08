# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 Valory AG
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

"""This module contains the handler for the 'price_estimation_abci' skill."""

from packages.eightballer.skills.dex_data_retrieval.handlers import (
    DexOrdersHandler as BaseDexOrdersHandler,
    DexMarketsHandler as BaseDexMarketsHandler,
    DexTickersHandler as BaseDexTickersHandler,
    DexBalancesHandler as BaseDexBalancesHandler,
    DexPositionsHandler as BaseDexPositionsHandler,
)
from packages.eightballer.skills.abstract_round_abci.handlers import (
    HttpHandler as BaseHttpHandler,
    IpfsHandler as BaseIpfsHandler,
    SigningHandler as BaseSigningHandler,
    ABCIRoundHandler,
    LedgerApiHandler as BaseLedgerApiHandler,
    TendermintHandler as BaseTendermintHandler,
    ContractApiHandler as BaseContractApiHandler,
)


ABCIPriceEstimationHandler = ABCIRoundHandler
HttpHandler = BaseHttpHandler
SigningHandler = BaseSigningHandler
LedgerApiHandler = BaseLedgerApiHandler
ContractApiHandler = BaseContractApiHandler
TendermintHandler = BaseTendermintHandler
IpfsHandler = BaseIpfsHandler
DexMarketsHandler = BaseDexMarketsHandler
DexOrdersHandler = BaseDexOrdersHandler
DexBalancesHandler = BaseDexBalancesHandler
DexPositionsHandler = BaseDexPositionsHandler
DexTickersHandler = BaseDexTickersHandler
