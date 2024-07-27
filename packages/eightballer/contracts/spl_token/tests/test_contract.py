# -*- coding: utf-8 -*-
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
# type: ignore # noqa: E800
# pylint: skip-file

from pathlib import Path
from typing import cast

import pytest
from aea.configurations.loader import (
    ComponentType,
    ContractConfig,
    load_component_configuration,
)
from aea.contracts.base import Contract, contract_registry
from aea_ledger_solana import SolanaApi, SolanaCrypto

from packages.eightballer.contracts.spl_token.contract import SplToken

PACKAGE_DIR = Path(__file__).parent.parent

DEFAULT_ADDRESS = "https://belita-kndiva-fast-mainnet.helius-rpc.com/"

SOL_ADDDRESS = "So11111111111111111111111111111111111111112"
OLAS_ADDRESS = "Ez3nzG9ofodYCvEmw73XhQ87LWNYVRM2s7diB5tBZPyM"


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
        configuration._directory = (  # pylint: disable=protected-access
            cls.path_to_contract
        )
        if str(configuration.public_id) not in contract_registry.specs:
            # load contract into sys modules
            Contract.from_config(configuration)
        cls.contract = contract_registry.make(str(configuration.public_id))

        CONFIG = {
            "address": DEFAULT_ADDRESS,
        }
        cls.ledger_api = SolanaApi(**CONFIG)

    @pytest.mark.parametrize(
        "address, symbol, expected_decimals",
        [
            (SOL_ADDDRESS, "SOL", 9),
            (OLAS_ADDRESS, "OLAS", 8),
        ],
    )
    def test_get_token(self, address, symbol, expected_decimals):
        """Test the get_token method."""

        token_data = self.contract.get_token(self.ledger_api, address, symbol)
        spl_token = SplToken(**token_data)
        assert (
            spl_token.decimals == expected_decimals
        ), f"Token {spl_token.symbol} has {spl_token.decimals} decimals, expected {expected_decimals}"

    @pytest.mark.parametrize(
        "contract_address",
        [
            SOL_ADDDRESS,
            OLAS_ADDRESS,
        ],
    )
    def test_get_balance(self, contract_address):
        """Test the get_balance method."""

        crypto = SolanaCrypto("solana_private_key.txt")
        balance = self.contract.get_balance(
            self.ledger_api, contract_address, crypto.address
        )
        assert (
            balance >= 0
        ), f"Balance of {contract_address} is {balance}, expected >= 0"
