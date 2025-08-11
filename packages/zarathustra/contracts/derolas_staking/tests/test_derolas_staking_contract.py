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

"""The tests module contains the tests of the Derolas staking contract."""
# type: ignore
# pylint: skip-file

from typing import cast
from pathlib import Path

from aea.contracts.base import Contract, contract_registry
from aea.configurations.loader import (
    ComponentType,
    ContractConfig,
    load_component_configuration,
)


PACKAGE_DIR = Path(__file__).parent.parent


class TestContractCommon:
    """Tests for the Derolas contract."""

    @classmethod
    def setup_method(cls) -> None:
        """Setup."""

        cls.path_to_contract = PACKAGE_DIR

        configuration = cast(
            ContractConfig,
            load_component_configuration(ComponentType.CONTRACT, cls.path_to_contract),
        )
        configuration._directory = cls.path_to_contract  # noqa
        if str(configuration.public_id) not in contract_registry.specs:
            # load contract into sys modules
            Contract.from_config(configuration)
        cls.contract = contract_registry.make(str(configuration.public_id))

    def test_contract_creation(self) -> None:
        """Test the creation of the contract."""
        assert self.contract is not None
        assert isinstance(self.contract, Contract)
        assert self.contract.contract_id == self.contract.contract_id
