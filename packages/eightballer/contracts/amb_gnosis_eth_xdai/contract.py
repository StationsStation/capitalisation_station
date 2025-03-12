"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class AmbGnosisEthXdai(Contract):
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
    def num_messages_signed(cls, ledger_api: LedgerApi, contract_address: str, message: str) -> JSONLike:
        """Handler method for the 'num_messages_signed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.numMessagesSigned(_message=message).call()
        return {"int": result}

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
    def signature(cls, ledger_api: LedgerApi, contract_address: str, hash: str, index: int) -> JSONLike:
        """Handler method for the 'signature' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.signature(_hash=hash, _index=index).call()
        return {"str": result}

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
    def message(cls, ledger_api: LedgerApi, contract_address: str, hash: str) -> JSONLike:
        """Handler method for the 'message' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.message(_hash=hash).call()
        return {"str": result}

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
    def num_affirmations_signed(cls, ledger_api: LedgerApi, contract_address: str, hash: str) -> JSONLike:
        """Handler method for the 'num_affirmations_signed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.numAffirmationsSigned(_hash=hash).call()
        return {"int": result}

    @classmethod
    def affirmations_signed(cls, ledger_api: LedgerApi, contract_address: str, hash: str) -> JSONLike:
        """Handler method for the 'affirmations_signed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.affirmationsSigned(_hash=hash).call()
        return {"bool": result}

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
    def messages_signed(cls, ledger_api: LedgerApi, contract_address: str, message: str) -> JSONLike:
        """Handler method for the 'messages_signed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.messagesSigned(_message=message).call()
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
    def is_async_request_selector_enabled(
        cls, ledger_api: LedgerApi, contract_address: str, request_selector: str
    ) -> JSONLike:
        """Handler method for the 'is_async_request_selector_enabled' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isAsyncRequestSelectorEnabled(_requestSelector=request_selector).call()
        return {"bool": result}

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
    def is_already_processed(cls, ledger_api: LedgerApi, contract_address: str, number: int) -> JSONLike:
        """Handler method for the 'is_already_processed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isAlreadyProcessed(_number=number).call()
        return {"bool": result}

    @classmethod
    def confirm_information(
        cls, ledger_api: LedgerApi, contract_address: str, message_id: str, status: bool, result: str
    ) -> JSONLike:
        """Handler method for the 'confirm_information' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.confirmInformation(_messageId=message_id, _status=status, _result=result)

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
    def set_chain_ids(
        cls, ledger_api: LedgerApi, contract_address: str, source_chain_id: int, destination_chain_id: int
    ) -> JSONLike:
        """Handler method for the 'set_chain_ids' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setChainIds(_sourceChainId=source_chain_id, _destinationChainId=destination_chain_id)

    @classmethod
    def require_to_get_information(
        cls, ledger_api: LedgerApi, contract_address: str, request_selector: str, data: str
    ) -> JSONLike:
        """Handler method for the 'require_to_get_information' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.requireToGetInformation(_requestSelector=request_selector, _data=data)

    @classmethod
    def submit_signature(cls, ledger_api: LedgerApi, contract_address: str, signature: str, message: str) -> JSONLike:
        """Handler method for the 'submit_signature' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.submitSignature(signature=signature, message=message)

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
    def require_to_confirm_message(
        cls, ledger_api: LedgerApi, contract_address: str, contract: Address, data: str, gas: int
    ) -> JSONLike:
        """Handler method for the 'require_to_confirm_message' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.requireToConfirmMessage(_contract=contract, _data=data, _gas=gas)

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
    def enable_async_request_selector(
        cls, ledger_api: LedgerApi, contract_address: str, request_selector: str, enable: bool
    ) -> JSONLike:
        """Handler method for the 'enable_async_request_selector' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.enableAsyncRequestSelector(_requestSelector=request_selector, _enable=enable)

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
    def execute_affirmation(cls, ledger_api: LedgerApi, contract_address: str, message: str) -> JSONLike:
        """Handler method for the 'execute_affirmation' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.executeAffirmation(message=message)

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

    @classmethod
    def get_user_request_for_signature_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        message_id: str | None = None,
        encoded_data: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'UserRequestForSignature' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("messageId", message_id), ("encodedData", encoded_data)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.UserRequestForSignature().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_affirmation_completed_events(
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
        """Handler method for the 'AffirmationCompleted' events ."""

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
        result = instance.events.AffirmationCompleted().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_user_request_for_information_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        message_id: str | None = None,
        request_selector: str | None = None,
        sender: Address = None,
        data: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'UserRequestForInformation' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("messageId", message_id),
                ("requestSelector", request_selector),
                ("sender", sender),
                ("data", data),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.UserRequestForInformation().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_signed_for_information_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        signer: Address = None,
        message_id: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'SignedForInformation' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("signer", signer), ("messageId", message_id)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.SignedForInformation().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_information_retrieved_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        message_id: str | None = None,
        status: bool | None = None,
        callback_status: bool | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'InformationRetrieved' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("messageId", message_id), ("status", status), ("callbackStatus", callback_status))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.InformationRetrieved().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_enabled_async_request_selector_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        request_selector: str | None = None,
        enable: bool | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'EnabledAsyncRequestSelector' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("requestSelector", request_selector), ("enable", enable))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.EnabledAsyncRequestSelector().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_signed_for_user_request_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        signer: Address = None,
        message_hash: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'SignedForUserRequest' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("signer", signer), ("messageHash", message_hash)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.SignedForUserRequest().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_signed_for_affirmation_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        signer: Address = None,
        message_hash: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'SignedForAffirmation' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("signer", signer), ("messageHash", message_hash)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.SignedForAffirmation().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_collected_signatures_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        authority_responsible_for_relay: Address = None,
        message_hash: str | None = None,
        number_of_collected_signatures: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'CollectedSignatures' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("authorityResponsibleForRelay", authority_responsible_for_relay),
                ("messageHash", message_hash),
                ("NumberOfCollectedSignatures", number_of_collected_signatures),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.CollectedSignatures().get_logs(
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
