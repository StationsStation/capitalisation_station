"""Utils for the DCXT package."""

from typing import cast
from pathlib import Path

from aea.contracts.base import Contract, contract_registry
from aea.configurations.base import PublicId
from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration
from aea.configurations.constants import CONTRACTS


def load_contract(public_id: PublicId):
    """Load the contract from the path."""
    is_built = Path("vendor").exists()
    contract_path = (
        (Path("packages") / public_id.author / CONTRACTS / public_id.name)
        if not is_built
        else Path("vendor") / public_id.author / CONTRACTS / public_id.name
    )
    configuration = cast(
        ContractConfig,
        load_component_configuration(ComponentType.CONTRACT, contract_path),
    )
    configuration._directory = contract_path  # noqa
    if str(configuration.public_id) not in contract_registry.specs:
        Contract.from_config(configuration)
    return contract_registry.make(str(configuration.public_id))
