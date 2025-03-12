"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class AmbMainnet(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def transaction_hash(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'transaction_hash' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.transactionHash().call()
        return {"str": result}

    @classmethod
    def source_chain_id(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'source_chain_id' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.sourceChainId().call()
        return {"int": result}

    @classmethod
    def hashi_is_mandatory(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'hashi_is_mandatory' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.HASHI_IS_MANDATORY().call()
        return {"bool": result}

    @classmethod
    def relayed_messages(cls, ledger_api: LedgerApi, contract_address: str, tx_hash: str) -> JSONLike:
        """Handler method for the 'relayed_messages' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.relayedMessages(_txHash=tx_hash).call()
        return {"bool": result}

    @classmethod
    def is_initialized(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'is_initialized' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isInitialized().call()
        return {"bool": result}

    @classmethod
    def required_block_confirmations(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'required_block_confirmations' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.requiredBlockConfirmations().call()
        return {"int": result}

    @classmethod
    def failed_message_receiver(cls, ledger_api: LedgerApi, contract_address: str, message_id: str) -> JSONLike:
        """Handler method for the 'failed_message_receiver' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.failedMessageReceiver(_messageId=message_id).call()
        return {"address": result}

    @classmethod
    def get_bridge_mode(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_bridge_mode' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getBridgeMode().call()
        return {"_data": result}

    @classmethod
    def failed_message_sender(cls, ledger_api: LedgerApi, contract_address: str, message_id: str) -> JSONLike:
        """Handler method for the 'failed_message_sender' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.failedMessageSender(_messageId=message_id).call()
        return {"address": result}

    @classmethod
    def allow_reentrant_requests(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'allow_reentrant_requests' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.allowReentrantRequests().call()
        return {"bool": result}

    @classmethod
    def message_id(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'message_id' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.messageId().call()
        return {"id": result}

    @classmethod
    def hashi_manager(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'hashi_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.hashiManager().call()
        return {"address": result}

    @classmethod
    def hashi_is_enabled(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'hashi_is_enabled' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.HASHI_IS_ENABLED().call()
        return {"bool": result}

    @classmethod
    def required_signatures(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'required_signatures' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.requiredSignatures().call()
        return {"int": result}

    @classmethod
    def owner(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'owner' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.owner().call()
        return {"address": result}

    @classmethod
    def is_approved_by_hashi(cls, ledger_api: LedgerApi, contract_address: str, hash_msg: str) -> JSONLike:
        """Handler method for the 'is_approved_by_hashi' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isApprovedByHashi(hashMsg=hash_msg).call()
        return {"bool": result}

    @classmethod
    def validator_contract(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'validator_contract' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.validatorContract().call()
        return {"address": result}

    @classmethod
    def deployed_at_block(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'deployed_at_block' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.deployedAtBlock().call()
        return {"int": result}

    @classmethod
    def get_bridge_interfaces_version(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_bridge_interfaces_version' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getBridgeInterfacesVersion().call()
        return {"major": result, "minor": result, "patch": result}

    @classmethod
    def message_source_chain_id(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'message_source_chain_id' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.messageSourceChainId().call()
        return {"id": result}

    @classmethod
    def destination_chain_id(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'destination_chain_id' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.destinationChainId().call()
        return {"int": result}

    @classmethod
    def message_call_status(cls, ledger_api: LedgerApi, contract_address: str, message_id: str) -> JSONLike:
        """Handler method for the 'message_call_status' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.messageCallStatus(_messageId=message_id).call()
        return {"bool": result}

    @classmethod
    def message_sender(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'message_sender' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.messageSender().call()
        return {"sender": result}

    @classmethod
    def decimal_shift(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'decimal_shift' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.decimalShift().call()
        return {"int": result}

    @classmethod
    def failed_message_data_hash(cls, ledger_api: LedgerApi, contract_address: str, message_id: str) -> JSONLike:
        """Handler method for the 'failed_message_data_hash' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.failedMessageDataHash(_messageId=message_id).call()
        return {"str": result}

    @classmethod
    def max_gas_per_tx(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'max_gas_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.maxGasPerTx().call()
        return {"int": result}

    @classmethod
    def gas_price(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'gas_price' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.gasPrice().call()
        return {"int": result}

    @classmethod
    def safe_execute_signatures_with_auto_gas_limit(
        cls, ledger_api: LedgerApi, contract_address: str, data: str, signatures: str
    ) -> JSONLike:
        """Handler method for the 'safe_execute_signatures_with_auto_gas_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.safeExecuteSignaturesWithAutoGasLimit(_data=data, _signatures=signatures)

    @classmethod
    def initialize(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        source_chain_id: int,
        destination_chain_id: int,
        validator_contract: Address,
        max_gas_per_tx: int,
        gas_price: int,
        required_block_confirmations: int,
        owner: Address,
    ) -> JSONLike:
        """Handler method for the 'initialize' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.initialize(
            _sourceChainId=source_chain_id,
            _destinationChainId=destination_chain_id,
            _validatorContract=validator_contract,
            _maxGasPerTx=max_gas_per_tx,
            _gasPrice=gas_price,
            _requiredBlockConfirmations=required_block_confirmations,
            _owner=owner,
        )

    @classmethod
    def execute_signatures(cls, ledger_api: LedgerApi, contract_address: str, data: str, signatures: str) -> JSONLike:
        """Handler method for the 'execute_signatures' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.executeSignatures(_data=data, _signatures=signatures)

    @classmethod
    def set_chain_ids(
        cls, ledger_api: LedgerApi, contract_address: str, source_chain_id: int, destination_chain_id: int
    ) -> JSONLike:
        """Handler method for the 'set_chain_ids' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setChainIds(_sourceChainId=source_chain_id, _destinationChainId=destination_chain_id)

    @classmethod
    def claim_tokens(cls, ledger_api: LedgerApi, contract_address: str, token: Address, to: Address) -> JSONLike:
        """Handler method for the 'claim_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.claimTokens(_token=token, _to=to)

    @classmethod
    def resend_data_with_hashi(cls, ledger_api: LedgerApi, contract_address: str, data: str) -> JSONLike:
        """Handler method for the 'resend_data_with_hashi' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.resendDataWithHashi(data=data)

    @classmethod
    def set_max_gas_per_tx(cls, ledger_api: LedgerApi, contract_address: str, max_gas_per_tx: int) -> JSONLike:
        """Handler method for the 'set_max_gas_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setMaxGasPerTx(_maxGasPerTx=max_gas_per_tx)

    @classmethod
    def set_required_block_confirmations(
        cls, ledger_api: LedgerApi, contract_address: str, block_confirmations: int
    ) -> JSONLike:
        """Handler method for the 'set_required_block_confirmations' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setRequiredBlockConfirmations(_blockConfirmations=block_confirmations)

    @classmethod
    def set_hashi_manager(cls, ledger_api: LedgerApi, contract_address: str, hashi_manager: Address) -> JSONLike:
        """Handler method for the 'set_hashi_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setHashiManager(_hashiManager=hashi_manager)

    @classmethod
    def set_gas_price(cls, ledger_api: LedgerApi, contract_address: str, gas_price: int) -> JSONLike:
        """Handler method for the 'set_gas_price' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setGasPrice(_gasPrice=gas_price)

    @classmethod
    def set_allow_reentrant_requests(cls, ledger_api: LedgerApi, contract_address: str, enable: bool) -> JSONLike:
        """Handler method for the 'set_allow_reentrant_requests' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setAllowReentrantRequests(_enable=enable)

    @classmethod
    def on_message(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        var_0: int,
        chain_id: int,
        sender: Address,
        threshold: int,
        adapters: list[Address],
        data: str,
    ) -> JSONLike:
        """Handler method for the 'on_message' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.onMessage(
            var_0, chainId=chain_id, sender=sender, threshold=threshold, adapters=adapters, data=data
        )

    @classmethod
    def require_to_pass_message(
        cls, ledger_api: LedgerApi, contract_address: str, contract: Address, data: str, gas: int
    ) -> JSONLike:
        """Handler method for the 'require_to_pass_message' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.requireToPassMessage(_contract=contract, _data=data, _gas=gas)

    @classmethod
    def safe_execute_signatures_with_gas_limit(
        cls, ledger_api: LedgerApi, contract_address: str, data: str, signatures: str, gas: int
    ) -> JSONLike:
        """Handler method for the 'safe_execute_signatures_with_gas_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.safeExecuteSignaturesWithGasLimit(_data=data, _signatures=signatures, _gas=gas)

    @classmethod
    def safe_execute_signatures(
        cls, ledger_api: LedgerApi, contract_address: str, data: str, signatures: str
    ) -> JSONLike:
        """Handler method for the 'safe_execute_signatures' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.safeExecuteSignatures(_data=data, _signatures=signatures)

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

    @classmethod
    def get_user_request_for_affirmation_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        message_id: str | None = None,
        encoded_data: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'UserRequestForAffirmation' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("messageId", message_id), ("encodedData", encoded_data)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.UserRequestForAffirmation().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_relayed_message_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        executor: Address = None,
        message_id: str | None = None,
        status: bool | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'RelayedMessage' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("executor", executor),
                ("messageId", message_id),
                ("status", status),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.RelayedMessage().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_gas_price_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        gas_price: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'GasPriceChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("gasPrice", gas_price)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.GasPriceChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_required_block_confirmation_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        required_block_confirmations: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'RequiredBlockConfirmationChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("requiredBlockConfirmations", required_block_confirmations))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.RequiredBlockConfirmationChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_ownership_transferred_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        previous_owner: Address = None,
        new_owner: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OwnershipTransferred' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("previousOwner", previous_owner), ("newOwner", new_owner))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.OwnershipTransferred().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }
