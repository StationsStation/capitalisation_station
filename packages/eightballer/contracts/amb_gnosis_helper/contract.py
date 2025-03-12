"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class AmbGnosisHelper(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def a_m_bcontract(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'a_m_bcontract' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.AMBcontract().call()
        return {"address": result}

    @classmethod
    def get_signatures(cls, ledger_api: LedgerApi, contract_address: str, message: str) -> JSONLike:
        """Handler method for the 'get_signatures' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getSignatures(_message=message).call()
        return {"str": result}

    @classmethod
    def clean(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'clean' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.clean()
