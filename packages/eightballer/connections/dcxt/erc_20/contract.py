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
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract

from packages.eightballer.connections.dcxt.erc_20 import PUBLIC_ID


@dataclass
class Erc20Token:
    """Class to represent a token."""

    address: str
    symbol: str
    decimals: int
    name: str = ""

    def to_human(self, amount):
        """Return an amount in human readable format."""
        return amount / 10**self.decimals

    def to_machine(self, amount):
        """Return an amount in machine readable format."""
        return int(amount * 10**self.decimals)


class Erc20(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PUBLIC_ID

    @classmethod
    def allowance(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        owner: Address,
        spender: Address,
    ) -> JSONLike:
        """Handler method for the 'allowance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.allowance(owner=owner, spender=spender).call()
        return {"int": result}

    @classmethod
    def balance_of(cls, ledger_api: LedgerApi, contract_address: str, account: Address) -> JSONLike:
        """Handler method for the 'balance_of' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.balanceOf(account=account).call()
        return {"int": result}

    @classmethod
    def decimals(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'decimals' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.decimals().call()
        return {"int": result}

    @classmethod
    def name(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'name' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.name().call()
        return {"str": result}

    @classmethod
    def symbol(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'symbol' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.symbol().call()
        return {"str": result}

    @classmethod
    def total_supply(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'total_supply' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.totalSupply().call()
        return {"int": result}

    @classmethod
    def get_token(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_token' requests.

        Implement this method in the sub class if you want
        to handle the contract requests manually.

        """

        decimals = cls.decimals(ledger_api, contract_address)["int"]
        symbol = cls.symbol(ledger_api, contract_address)["str"]
        token = Erc20Token(address=contract_address, symbol=symbol, decimals=decimals)
        return token.__dict__

    @classmethod
    def approve(cls, ledger_api: LedgerApi, contract_address: str, to: Address, value: int) -> JSONLike:
        """Handler method for the 'approve' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.approve(to, value)
