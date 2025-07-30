# ------------------------------------------------------------------------------
#
#   Copyright 2025 zarathustra
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

"""This module contains the models for the 'derolas_automator_abci_app' skill."""

from typing import Any
from pathlib import Path

from aea.skills.base import Model
from aea.contracts.base import Contract, contract_registry
from aea_ledger_ethereum import EthereumApi, EthereumCrypto
from aea.configurations.loader import ComponentType, load_component_configuration

from packages.valory.connections.ledger.connection import PUBLIC_ID as LEDGER_PUBLIC_ID
from packages.zarathustra.contracts.derolas_staking import (
    PUBLIC_ID as DEROLAS_PUBLIC_ID,
)


ROOT = Path(__file__).parent.parent.parent.parent


_TMP = LEDGER_PUBLIC_ID


def load_contract(contract_path: Path) -> Contract:
    """Helper function to load a contract."""
    configuration = load_component_configuration(ComponentType.CONTRACT, contract_path)
    configuration._directory = contract_path  # noqa
    if str(configuration.public_id) not in contract_registry.specs:
        # load contract into sys modules
        Contract.from_config(configuration)
    return contract_registry.make(str(configuration.public_id))


class DerolasState(Model):
    """Derolas Stare."""

    def __init__(self, **kwargs: dict[str, Any]):
        author = DEROLAS_PUBLIC_ID.author
        name = DEROLAS_PUBLIC_ID.name
        contract = load_contract(ROOT / author / "contracts" / name)
        self.derolas_staking_contract = contract
        self.derolas_contract_address = "0x2216ebB7f5f983b1D15713F90556edd56EB88DeE"
        super().__init__(**kwargs)

    @property
    def base_ledger_api(self) -> EthereumApi:
        """Get the Base ledger api."""
        return EthereumApi(address="https://base.llamarpc.com", chain_id=str(8453))

    @property
    def crypto(self) -> EthereumCrypto:
        """Get EthereumCrypto."""
        return EthereumCrypto(private_key_path="ethereum_private_key.txt")
