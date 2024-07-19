# -*- coding: utf-8 -*-
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

from packages.eightballer.protocols.balances.dialogues import BalancesDialogue as BaseBalancesDialogue
from packages.eightballer.protocols.balances.dialogues import BalancesDialogues as BaseBalancesDialogues
from packages.eightballer.protocols.markets.dialogues import MarketsDialogue as BaseMarketsDialogue
from packages.eightballer.protocols.markets.dialogues import MarketsDialogues as BaseMarketsDialogues
from packages.eightballer.protocols.orders.dialogues import OrdersDialogue as BaseOrderDialogue
from packages.eightballer.protocols.orders.dialogues import OrdersDialogues as BaseOrderDialogues
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue as BasePositionsDialogue
from packages.eightballer.protocols.positions.dialogues import PositionsDialogues as BasePositionsDialogues
from packages.eightballer.protocols.tickers.dialogues import TickersDialogue as BaseTickersDialogue
from packages.eightballer.protocols.tickers.dialogues import TickersDialogues as BaseTickersDialogues
from packages.valory.skills.abstract_round_abci.dialogues import AbciDialogue as BaseAbciDialogue
from packages.valory.skills.abstract_round_abci.dialogues import AbciDialogues as BaseAbciDialogues
from packages.valory.skills.abstract_round_abci.dialogues import ContractApiDialogue as BaseContractApiDialogue
from packages.valory.skills.abstract_round_abci.dialogues import ContractApiDialogues as BaseContractApiDialogues
from packages.valory.skills.abstract_round_abci.dialogues import HttpDialogue as BaseHttpDialogue
from packages.valory.skills.abstract_round_abci.dialogues import HttpDialogues as BaseHttpDialogues
from packages.valory.skills.abstract_round_abci.dialogues import IpfsDialogue as BaseIpfsDialogue
from packages.valory.skills.abstract_round_abci.dialogues import IpfsDialogues as BaseIpfsDialogues
from packages.valory.skills.abstract_round_abci.dialogues import LedgerApiDialogue as BaseLedgerApiDialogue
from packages.valory.skills.abstract_round_abci.dialogues import LedgerApiDialogues as BaseLedgerApiDialogues
from packages.valory.skills.abstract_round_abci.dialogues import SigningDialogue as BaseSigningDialogue
from packages.valory.skills.abstract_round_abci.dialogues import SigningDialogues as BaseSigningDialogues
from packages.valory.skills.abstract_round_abci.dialogues import TendermintDialogue as BaseTendermintDialogue
from packages.valory.skills.abstract_round_abci.dialogues import TendermintDialogues as BaseTendermintDialogues

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
