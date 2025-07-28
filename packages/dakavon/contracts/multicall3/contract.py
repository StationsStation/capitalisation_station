"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class Multicall3(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def get_basefee(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_basefee' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getBasefee().call()
        return {"basefee": result}

    @classmethod
    def get_block_hash(cls, ledger_api: LedgerApi, contract_address: str, block_number: int) -> JSONLike:
        """Handler method for the 'get_block_hash' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getBlockHash(blockNumber=block_number).call()
        return {"blockHash": result}

    @classmethod
    def get_block_number(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_block_number' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getBlockNumber().call()
        return {"blockNumber": result}

    @classmethod
    def get_chain_id(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_chain_id' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getChainId().call()
        return {"chainid": result}

    @classmethod
    def get_current_block_coinbase(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_current_block_coinbase' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentBlockCoinbase().call()
        return {"coinbase": result}

    @classmethod
    def get_current_block_difficulty(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_current_block_difficulty' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentBlockDifficulty().call()
        return {"difficulty": result}

    @classmethod
    def get_current_block_gas_limit(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_current_block_gas_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentBlockGasLimit().call()
        return {"gaslimit": result}

    @classmethod
    def get_current_block_timestamp(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_current_block_timestamp' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentBlockTimestamp().call()
        return {"timestamp": result}

    @classmethod
    def get_eth_balance(cls, ledger_api: LedgerApi, contract_address: str, addr: Address) -> JSONLike:
        """Handler method for the 'get_eth_balance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getEthBalance(addr=addr).call()
        return {"balance": result}

    @classmethod
    def get_last_block_hash(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_last_block_hash' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getLastBlockHash().call()
        return {"blockHash": result}

    @classmethod
    def aggregate(cls, ledger_api: LedgerApi, contract_address: str, calls: tuple[...]) -> JSONLike:
        """Handler method for the 'aggregate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.aggregate(calls=calls)

    @classmethod
    def aggregate3(cls, ledger_api: LedgerApi, contract_address: str, calls: tuple[...]) -> JSONLike:
        """Handler method for the 'aggregate3' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.aggregate3(calls=calls)

    @classmethod
    def aggregate3_value(cls, ledger_api: LedgerApi, contract_address: str, calls: tuple[...]) -> JSONLike:
        """Handler method for the 'aggregate3_value' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.aggregate3Value(calls=calls)

    @classmethod
    def block_and_aggregate(cls, ledger_api: LedgerApi, contract_address: str, calls: tuple[...]) -> JSONLike:
        """Handler method for the 'block_and_aggregate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.blockAndAggregate(calls=calls)

    @classmethod
    def try_aggregate(
        cls, ledger_api: LedgerApi, contract_address: str, require_success: bool, calls: tuple[...]
    ) -> JSONLike:
        """Handler method for the 'try_aggregate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.tryAggregate(requireSuccess=require_success, calls=calls)

    @classmethod
    def try_block_and_aggregate(
        cls, ledger_api: LedgerApi, contract_address: str, require_success: bool, calls: tuple[...]
    ) -> JSONLike:
        """Handler method for the 'try_block_and_aggregate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.tryBlockAndAggregate(requireSuccess=require_success, calls=calls)
