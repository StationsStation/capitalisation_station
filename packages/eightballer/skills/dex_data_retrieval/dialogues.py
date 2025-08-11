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

"""This module contains the dialogues of the AbciApp."""

from packages.eightballer.protocols.orders.dialogues import (
    OrdersDialogue as BaseOrderDialogue,
    OrdersDialogues as BaseOrderDialogues,
)
from packages.eightballer.protocols.markets.dialogues import (
    MarketsDialogue as BaseMarketsDialogue,
    MarketsDialogues as BaseMarketsDialogues,
)
from packages.eightballer.protocols.tickers.dialogues import (
    TickersDialogue as BaseTickersDialogue,
    TickersDialogues as BaseTickersDialogues,
)
from packages.eightballer.protocols.balances.dialogues import (
    BalancesDialogue as BaseBalancesDialogue,
    BalancesDialogues as BaseBalancesDialogues,
)
from packages.eightballer.protocols.positions.dialogues import (
    PositionsDialogue as BasePositionsDialogue,
    PositionsDialogues as BasePositionsDialogues,
)
from packages.valory.skills.abstract_round_abci.dialogues import (
    AbciDialogue as BaseAbciDialogue,
    HttpDialogue as BaseHttpDialogue,
    IpfsDialogue as BaseIpfsDialogue,
    AbciDialogues as BaseAbciDialogues,
    HttpDialogues as BaseHttpDialogues,
    IpfsDialogues as BaseIpfsDialogues,
    SigningDialogue as BaseSigningDialogue,
    SigningDialogues as BaseSigningDialogues,
    LedgerApiDialogue as BaseLedgerApiDialogue,
    LedgerApiDialogues as BaseLedgerApiDialogues,
    TendermintDialogue as BaseTendermintDialogue,
    ContractApiDialogue as BaseContractApiDialogue,
    TendermintDialogues as BaseTendermintDialogues,
    ContractApiDialogues as BaseContractApiDialogues,
)


AbciDialogue = BaseAbciDialogue
AbciDialogues = BaseAbciDialogues


HttpDialogue = BaseHttpDialogue
HttpDialogues = BaseHttpDialogues


SigningDialogue = BaseSigningDialogue
SigningDialogues = BaseSigningDialogues


LedgerApiDialogue = BaseLedgerApiDialogue
LedgerApiDialogues = BaseLedgerApiDialogues


ContractApiDialogue = BaseContractApiDialogue
ContractApiDialogues = BaseContractApiDialogues


TendermintDialogue = BaseTendermintDialogue
TendermintDialogues = BaseTendermintDialogues


IpfsDialogue = BaseIpfsDialogue
IpfsDialogues = BaseIpfsDialogues


MarketsDialogue = BaseMarketsDialogue
MarketsDialogues = BaseMarketsDialogues

OrdersDialogues = BaseOrderDialogues
OrdersDialogue = BaseOrderDialogue

BalancesDialogues = BaseBalancesDialogues
BalancesDialogue = BaseBalancesDialogue

PositionsDialogue = BasePositionsDialogue
PositionsDialogues = BasePositionsDialogues

TickersDialogue = BaseTickersDialogue
TickersDialogues = BaseTickersDialogues
