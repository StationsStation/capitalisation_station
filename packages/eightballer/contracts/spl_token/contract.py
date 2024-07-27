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

"""This module contains the scaffold contract definition."""

from dataclasses import dataclass

from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from aea_ledger_solana import Pubkey
from solana.rpc.types import TokenAccountOpts

PUBLIC_ID = PublicId.from_str("eightballer/spl_token:0.1.0")
SOL_ADDDRESS = "So11111111111111111111111111111111111111112"


@dataclass
class SplToken:
    """Class to represent a token."""

    address: str
    symbol: str
    decimals: int

    def to_human(self, amount):
        """Return an amount in human readable format."""
        return amount / 10**self.decimals

    def to_machine(self, amount):
        """Return an amount in machine readable format."""
        return int(amount * 10**self.decimals)


class SolanaProgramLibraryToken(Contract):
    """The class to allow the retrieveal of decimals for a Solana token."""

    contract_id = PUBLIC_ID

    @classmethod
    def get_token(
        cls,  # noqa
        ledger_api: LedgerApi,
        contract_address: str,
        symbol: str,
    ) -> JSONLike:  # pylint: disable=unused-argument
        """
        Handler method for the 'get_token' requests.

        Implement this method in the sub class if you want
        to handle the contract requests manually.

        :param ledger_api: the ledger apis.
        :param contract_address: the contract address.
        :param symbol: the symbol of the token.
        :return: token_data # noqa: DAR202
        """

        decimals = ledger_api.get_state(contract_address).data.parsed["info"][
            "decimals"
        ]
        token = SplToken(address=contract_address, symbol=symbol, decimals=decimals)
        return token.__dict__

    @classmethod
    def get_balance(
        cls,  # noqa
        ledger_api: LedgerApi,
        contract_address: str,
        address: str,
    ) -> JSONLike:
        """
        Handler method for the 'get_balance' requests.

        Implement this method in the sub class if you want
        to handle the contract requests manually.

        :param ledger_api: the ledger apis.
        :param contract_address: the contract address.
        :param address: the address of the account.
        :return: balance
        """
        if contract_address == SOL_ADDDRESS:
            return ledger_api.get_balance(address)
        address_pubkey = Pubkey.from_string(address)
        opts = TokenAccountOpts(
            mint=Pubkey.from_string(contract_address),
        )
        raw_res = ledger_api.api.get_token_accounts_by_owner_json_parsed(
            owner=address_pubkey, opts=opts
        )
        return int(
            raw_res.value[0].account.data.parsed["info"]["tokenAmount"]["amount"]
        )
