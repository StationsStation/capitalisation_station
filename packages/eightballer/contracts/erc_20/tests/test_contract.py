# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
#   Copyright 2021-2022 Valory AG
#   Copyright 2018-2020 Fetch.AI Limited
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

"""The tests module contains the tests of the packages/contracts/orca_whirlpool dir."""
# type: ignore
# pylint: skip-file

from typing import cast
from pathlib import Path

import pytest
from aea.contracts.base import Contract, contract_registry
from aea_ledger_ethereum import EthereumApi, EthereumCrypto
from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration

from packages.eightballer.contracts.erc_20.contract import Erc20Token


PACKAGE_DIR = Path(__file__).parent.parent

DEFAULT_ADDRESS = "http://eth.chains.wtf:8545"

DAI_ADDRESS = "0x6b175474e89094c44da98b954eedeac495271d0f"
OLAS_ADDRESS = "0x0001a500a6b18995b03f44bb040a5ffc28e45cb0"


class TestContractCommon:
    """Other tests for the contract."""

    @classmethod
    def setup(cls) -> None:
        """Setup."""

        # Register smart contract used for testing
        cls.path_to_contract = PACKAGE_DIR

        # register contract
        configuration = cast(
            ContractConfig,
            load_component_configuration(ComponentType.CONTRACT, cls.path_to_contract),
        )
        configuration._directory = cls.path_to_contract  # noqa
        if str(configuration.public_id) not in contract_registry.specs:
            # load contract into sys modules
            Contract.from_config(configuration)
        cls.contract = contract_registry.make(str(configuration.public_id))

        config = {
            "address": DEFAULT_ADDRESS,
        }
        cls.ledger_api = EthereumApi(**config)

    @pytest.mark.parametrize(
        ("address", "expected_decimals"),
        [
            (DAI_ADDRESS, 18),
            (OLAS_ADDRESS, 18),
        ],
    )
    @pytest.mark.skip("This test is not is only for local testing.")
    def test_get_token(self, address, expected_decimals):
        """Test the get_token method."""

        token_data = self.contract.get_token(self.ledger_api, address)
        token = Erc20Token(**token_data)
        assert (
            token.decimals == expected_decimals
        ), f"Token {token.symbol} has {token.decimals} decimals, expected {expected_decimals}"

    @pytest.mark.parametrize(
        "contract_address",
        [
            DAI_ADDRESS,
            OLAS_ADDRESS,
        ],
    )
    @pytest.mark.skip("This test is not is only for local testing.")
    def test_get_balance(self, contract_address):
        """Test the get_balance method."""

        crypto = EthereumCrypto("ethereum_private_key.txt")
        balance = self.contract.get_balance(self.ledger_api, contract_address, crypto.address)
        assert balance >= 0, f"Balance of {contract_address} is {balance}, expected >= 0"
