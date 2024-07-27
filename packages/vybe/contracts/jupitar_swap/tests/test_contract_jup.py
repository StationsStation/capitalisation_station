# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
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

import json
import time
from pathlib import Path
from typing import Optional, Tuple, Union, cast

import pytest
from aea.common import JSONLike
from aea.configurations.loader import (
    ComponentType,
    ContractConfig,
    load_component_configuration,
)
from aea.contracts.base import Contract, contract_registry
from aea_ledger_solana import SolanaApi, SolanaCrypto, SolanaFaucetApi
from solders.message import MessageV0
from solders.transaction import VersionedTransaction

from packages.eightballer.contracts.spl_token.contract import (
    SolanaProgramLibraryToken,
    SplToken,
)

PACKAGE_DIR = Path(__file__).parent.parent
MAX_FLAKY_RERUNS = 3

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
        cls.faucet = SolanaFaucetApi()

    @staticmethod
    def retry_airdrop_if_result_none(faucet, address, amount=None):
        cnt = 0
        tx = None
        while tx is None and cnt < 10:
            tx = faucet.get_wealth(address, amount, url=DEFAULT_ADDRESS)
            cnt += 1
            time.sleep(2)
        return tx

    def _generate_wealth_if_needed(self, api, address, amount=None) -> Union[str, None]:
        balance = api.get_balance(address)

        if balance >= 1000000000:
            return "not required"
        else:
            faucet = SolanaFaucetApi()
            cnt = 0
            transaction_digest = None
            while transaction_digest is None and cnt < 10:
                transaction_digest = faucet.get_wealth(address, amount)
                cnt += 1
                time.sleep(2)

            if transaction_digest == None:
                return "failed"
            else:
                transaction_receipt, is_settled = self._wait_get_receipt(
                    api, transaction_digest
                )
                if is_settled is True:
                    return "success"
                else:
                    return "failed"

    @staticmethod
    def _wait_get_receipt(
        solana_api: SolanaApi, transaction_digest: str
    ) -> Tuple[Optional[JSONLike], bool]:
        transaction_receipt = None
        is_settled = False
        elapsed_time = 0
        time_to_wait = 40
        sleep_time = 0.25

        while not is_settled and elapsed_time < time_to_wait:
            elapsed_time += sleep_time
            time.sleep(sleep_time)
            transaction_receipt = solana_api.get_transaction_receipt(transaction_digest)
            is_settled = solana_api.is_transaction_settled(transaction_receipt)
        return transaction_receipt, is_settled

    def json_to_versioned_tx(tx):
        pass

    def _sign_and_settle(
        self, solana_api: SolanaApi, txn: dict, payer
    ) -> Tuple[str, JSONLike]:
        recent_blockhash = self.ledger_api.api.get_latest_blockhash().value.blockhash
        txn["message"][1]["recentBlockhash"] = json.loads(recent_blockhash.to_json())
        msg = MessageV0.from_json(json.dumps(txn["message"][1]))
        signed_transaction = VersionedTransaction(msg, [payer.entity])
        transaction_digest = self.ledger_api.api.send_transaction(signed_transaction)
        transaction_receipt, is_settled = self._wait_get_receipt(
            self.ledger_api, str(transaction_digest.value)
        )
        assert is_settled is True
        return [str(transaction_digest.value), transaction_receipt]

    @pytest.mark.ledger
    @pytest.mark.parametrize(
        "input_mint, output_mint, amount",
        [
            (SOL_ADDDRESS, OLAS_ADDRESS, 88888),
            (OLAS_ADDRESS, SOL_ADDDRESS, 15555),
        ],
    )
    def test_get_swap_tx(self, input_mint, output_mint, amount) -> None:
        """Test get swap transaction."""

        payer = SolanaCrypto("./solana_private_key.txt")

        txn = self.contract.get_swap_transaction(
            ledger_api=self.ledger_api,
            authority=payer.address,
            input_mint=input_mint,
            output_mint=output_mint,
            amount=amount,
            slippage_bps=10,
        )

        transaction_digest, is_settled = self._sign_and_settle(
            self.ledger_api, txn, payer
        )

        assert transaction_digest is not None
        assert is_settled

    @pytest.mark.ledger
    @pytest.mark.parametrize(
        "input_mint, output_mint, amount",
        [
            ((SOL_ADDDRESS, "SOL"), (OLAS_ADDRESS, "OLAS"), 0.001),
            ((OLAS_ADDRESS, "OLAS"), (SOL_ADDDRESS, "SOL"), 1),
        ],
    )
    def test_get_swap_quote(self, input_mint, output_mint, amount) -> None:
        """Test get swap transaction."""

        # we first need to retrieve the token info
        input_token = SplToken(
            **SolanaProgramLibraryToken.get_token(self.ledger_api, *input_mint)
        )
        output_token = SplToken(
            **SolanaProgramLibraryToken.get_token(self.ledger_api, *output_mint)
        )
        quote = self.contract.get_swap_quote(
            ledger_api=self.ledger_api,
            input_mint=input_token.address,
            output_mint=output_token.address,
            amount=input_token.to_machine(amount),
            slippage_bps=10,
        )
        rate = amount / output_token.to_human(int(quote["outAmount"]))
        assert rate > 0
