"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class AmbGnosis(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def bridge_contract(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'bridge_contract' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.bridgeContract().call()
        return {"address": result}

    @classmethod
    def bridged_token_address(cls, ledger_api: LedgerApi, contract_address: str, native_token: Address) -> JSONLike:
        """Handler method for the 'bridged_token_address' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.bridgedTokenAddress(_nativeToken=native_token).call()
        return {"address": result}

    @classmethod
    def daily_limit(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'daily_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.dailyLimit(_token=token).call()
        return {"int": result}

    @classmethod
    def execution_daily_limit(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'execution_daily_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.executionDailyLimit(_token=token).call()
        return {"int": result}

    @classmethod
    def execution_max_per_tx(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'execution_max_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.executionMaxPerTx(_token=token).call()
        return {"int": result}

    @classmethod
    def fee_manager(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'fee_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.feeManager().call()
        return {"address": result}

    @classmethod
    def foreign_token_address(cls, ledger_api: LedgerApi, contract_address: str, home_token: Address) -> JSONLike:
        """Handler method for the 'foreign_token_address' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.foreignTokenAddress(_homeToken=home_token).call()
        return {"address": result}

    @classmethod
    def forwarding_rules_manager(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'forwarding_rules_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.forwardingRulesManager().call()
        return {"address": result}

    @classmethod
    def gas_limit_manager(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'gas_limit_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.gasLimitManager().call()
        return {"address": result}

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
    def get_current_day(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_current_day' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentDay().call()
        return {"int": result}

    @classmethod
    def home_token_address(cls, ledger_api: LedgerApi, contract_address: str, foreign_token: Address) -> JSONLike:
        """Handler method for the 'home_token_address' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.homeTokenAddress(_foreignToken=foreign_token).call()
        return {"address": result}

    @classmethod
    def is_bridged_token_deploy_acknowledged(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address
    ) -> JSONLike:
        """Handler method for the 'is_bridged_token_deploy_acknowledged' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isBridgedTokenDeployAcknowledged(_token=token).call()
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
    def is_registered_as_native_token(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'is_registered_as_native_token' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isRegisteredAsNativeToken(_token=token).call()
        return {"bool": result}

    @classmethod
    def is_token_registered(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'is_token_registered' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isTokenRegistered(_token=token).call()
        return {"bool": result}

    @classmethod
    def max_available_per_tx(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'max_available_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.maxAvailablePerTx(_token=token).call()
        return {"int": result}

    @classmethod
    def max_per_tx(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'max_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.maxPerTx(_token=token).call()
        return {"int": result}

    @classmethod
    def mediator_balance(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'mediator_balance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.mediatorBalance(_token=token).call()
        return {"int": result}

    @classmethod
    def mediator_contract_on_other_side(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'mediator_contract_on_other_side' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.mediatorContractOnOtherSide().call()
        return {"address": result}

    @classmethod
    def message_fixed(cls, ledger_api: LedgerApi, contract_address: str, message_id: str) -> JSONLike:
        """Handler method for the 'message_fixed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.messageFixed(_messageId=message_id).call()
        return {"bool": result}

    @classmethod
    def min_per_tx(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'min_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.minPerTx(_token=token).call()
        return {"int": result}

    @classmethod
    def native_token_address(cls, ledger_api: LedgerApi, contract_address: str, bridged_token: Address) -> JSONLike:
        """Handler method for the 'native_token_address' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.nativeTokenAddress(_bridgedToken=bridged_token).call()
        return {"address": result}

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
    def token_factory(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'token_factory' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.tokenFactory().call()
        return {"address": result}

    @classmethod
    def total_executed_per_day(cls, ledger_api: LedgerApi, contract_address: str, token: Address, day: int) -> JSONLike:
        """Handler method for the 'total_executed_per_day' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.totalExecutedPerDay(_token=token, _day=day).call()
        return {"int": result}

    @classmethod
    def total_spent_per_day(cls, ledger_api: LedgerApi, contract_address: str, token: Address, day: int) -> JSONLike:
        """Handler method for the 'total_spent_per_day' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.totalSpentPerDay(_token=token, _day=day).call()
        return {"int": result}

    @classmethod
    def within_execution_limit(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, amount: int
    ) -> JSONLike:
        """Handler method for the 'within_execution_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.withinExecutionLimit(_token=token, _amount=amount).call()
        return {"bool": result}

    @classmethod
    def within_limit(cls, ledger_api: LedgerApi, contract_address: str, token: Address, amount: int) -> JSONLike:
        """Handler method for the 'within_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.withinLimit(_token=token, _amount=amount).call()
        return {"bool": result}

    @classmethod
    def claim_tokens(cls, ledger_api: LedgerApi, contract_address: str, token: Address, to: Address) -> JSONLike:
        """Handler method for the 'claim_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.claimTokens(_token=token, _to=to)

    @classmethod
    def claim_tokens_from_token_contract(
        cls, ledger_api: LedgerApi, contract_address: str, bridged_token: Address, token: Address, to: Address
    ) -> JSONLike:
        """Handler method for the 'claim_tokens_from_token_contract' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.claimTokensFromTokenContract(_bridgedToken=bridged_token, _token=token, _to=to)

    @classmethod
    def deploy_and_handle_bridged_tokens(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token: Address,
        name: str,
        symbol: str,
        decimals: int,
        recipient: Address,
        value: int,
    ) -> JSONLike:
        """Handler method for the 'deploy_and_handle_bridged_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.deployAndHandleBridgedTokens(
            _token=token, _name=name, _symbol=symbol, _decimals=decimals, _recipient=recipient, _value=value
        )

    @classmethod
    def deploy_and_handle_bridged_tokens_and_call(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token: Address,
        name: str,
        symbol: str,
        decimals: int,
        recipient: Address,
        value: int,
        data: str,
    ) -> JSONLike:
        """Handler method for the 'deploy_and_handle_bridged_tokens_and_call' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.deployAndHandleBridgedTokensAndCall(
            _token=token, _name=name, _symbol=symbol, _decimals=decimals, _recipient=recipient, _value=value, _data=data
        )

    @classmethod
    def fix_failed_message(cls, ledger_api: LedgerApi, contract_address: str, message_id: str) -> JSONLike:
        """Handler method for the 'fix_failed_message' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.fixFailedMessage(_messageId=message_id)

    @classmethod
    def fix_mediator_balance(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, receiver: Address
    ) -> JSONLike:
        """Handler method for the 'fix_mediator_balance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.fixMediatorBalance(_token=token, _receiver=receiver)

    @classmethod
    def handle_bridged_tokens(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, recipient: Address, value: int
    ) -> JSONLike:
        """Handler method for the 'handle_bridged_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.handleBridgedTokens(_token=token, _recipient=recipient, _value=value)

    @classmethod
    def handle_bridged_tokens_and_call(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, recipient: Address, value: int, data: str
    ) -> JSONLike:
        """Handler method for the 'handle_bridged_tokens_and_call' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.handleBridgedTokensAndCall(
            _token=token, _recipient=recipient, _value=value, _data=data
        )

    @classmethod
    def handle_native_tokens(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, recipient: Address, value: int
    ) -> JSONLike:
        """Handler method for the 'handle_native_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.handleNativeTokens(_token=token, _recipient=recipient, _value=value)

    @classmethod
    def handle_native_tokens_and_call(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, recipient: Address, value: int, data: str
    ) -> JSONLike:
        """Handler method for the 'handle_native_tokens_and_call' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.handleNativeTokensAndCall(
            _token=token, _recipient=recipient, _value=value, _data=data
        )

    @classmethod
    def initialize(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        bridge_contract: Address,
        mediator_contract: Address,
        daily_limit_max_per_tx_min_per_tx_array: list[int],
        execution_daily_limit_execution_max_per_tx_array: list[int],
        gas_limit_manager: Address,
        owner: Address,
        token_factory: Address,
        fee_manager: Address,
        forwarding_rules_manager: Address,
    ) -> JSONLike:
        """Handler method for the 'initialize' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.initialize(
            _bridgeContract=bridge_contract,
            _mediatorContract=mediator_contract,
            _dailyLimitMaxPerTxMinPerTxArray=daily_limit_max_per_tx_min_per_tx_array,
            _executionDailyLimitExecutionMaxPerTxArray=execution_daily_limit_execution_max_per_tx_array,
            _gasLimitManager=gas_limit_manager,
            _owner=owner,
            _tokenFactory=token_factory,
            _feeManager=fee_manager,
            _forwardingRulesManager=forwarding_rules_manager,
        )

    @classmethod
    def migrate_to_3_3_0(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token_factory: Address,
        forwarding_rules_manager: Address,
        gas_limit_manager: Address,
        fee_manager: Address,
    ) -> JSONLike:
        """Handler method for the 'migrate_to_3_3_0' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.migrateTo_3_3_0(
            _tokenFactory=token_factory,
            _forwardingRulesManager=forwarding_rules_manager,
            _gasLimitManager=gas_limit_manager,
            _feeManager=fee_manager,
        )

    @classmethod
    def on_token_transfer(
        cls, ledger_api: LedgerApi, contract_address: str, from_: Address, value: int, data: str
    ) -> JSONLike:
        """Handler method for the 'on_token_transfer' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.onTokenTransfer(_from=from_, _value=value, _data=data)

    @classmethod
    def relay_tokens(cls, ledger_api: LedgerApi, contract_address: str, token: Address, value: int) -> JSONLike:
        """Handler method for the 'relay_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.relayTokens(token=token, _value=value)

    @classmethod
    def relay_tokens_1(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, receiver: Address, value: int
    ) -> JSONLike:
        """Handler method for the 'relay_tokens_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.relayTokens_1(token=token, _receiver=receiver, _value=value)

    @classmethod
    def relay_tokens_and_call(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, receiver: Address, value: int, data: str
    ) -> JSONLike:
        """Handler method for the 'relay_tokens_and_call' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.relayTokensAndCall(token=token, _receiver=receiver, _value=value, _data=data)

    @classmethod
    def request_failed_message_fix(cls, ledger_api: LedgerApi, contract_address: str, message_id: str) -> JSONLike:
        """Handler method for the 'request_failed_message_fix' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.requestFailedMessageFix(_messageId=message_id)

    @classmethod
    def set_bridge_contract(cls, ledger_api: LedgerApi, contract_address: str, bridge_contract: Address) -> JSONLike:
        """Handler method for the 'set_bridge_contract' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setBridgeContract(_bridgeContract=bridge_contract)

    @classmethod
    def set_custom_token_address_pair(
        cls, ledger_api: LedgerApi, contract_address: str, native_token: Address, bridged_token: Address
    ) -> JSONLike:
        """Handler method for the 'set_custom_token_address_pair' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setCustomTokenAddressPair(_nativeToken=native_token, _bridgedToken=bridged_token)

    @classmethod
    def set_daily_limit(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, daily_limit: int
    ) -> JSONLike:
        """Handler method for the 'set_daily_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setDailyLimit(_token=token, _dailyLimit=daily_limit)

    @classmethod
    def set_execution_daily_limit(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, daily_limit: int
    ) -> JSONLike:
        """Handler method for the 'set_execution_daily_limit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setExecutionDailyLimit(_token=token, _dailyLimit=daily_limit)

    @classmethod
    def set_execution_max_per_tx(
        cls, ledger_api: LedgerApi, contract_address: str, token: Address, max_per_tx: int
    ) -> JSONLike:
        """Handler method for the 'set_execution_max_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setExecutionMaxPerTx(_token=token, _maxPerTx=max_per_tx)

    @classmethod
    def set_fee_manager(cls, ledger_api: LedgerApi, contract_address: str, fee_manager: Address) -> JSONLike:
        """Handler method for the 'set_fee_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setFeeManager(_feeManager=fee_manager)

    @classmethod
    def set_forwarding_rules_manager(cls, ledger_api: LedgerApi, contract_address: str, manager: Address) -> JSONLike:
        """Handler method for the 'set_forwarding_rules_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setForwardingRulesManager(_manager=manager)

    @classmethod
    def set_gas_limit_manager(cls, ledger_api: LedgerApi, contract_address: str, manager: Address) -> JSONLike:
        """Handler method for the 'set_gas_limit_manager' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setGasLimitManager(_manager=manager)

    @classmethod
    def set_max_per_tx(cls, ledger_api: LedgerApi, contract_address: str, token: Address, max_per_tx: int) -> JSONLike:
        """Handler method for the 'set_max_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setMaxPerTx(_token=token, _maxPerTx=max_per_tx)

    @classmethod
    def set_mediator_contract_on_other_side(
        cls, ledger_api: LedgerApi, contract_address: str, mediator_contract: Address
    ) -> JSONLike:
        """Handler method for the 'set_mediator_contract_on_other_side' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setMediatorContractOnOtherSide(_mediatorContract=mediator_contract)

    @classmethod
    def set_min_per_tx(cls, ledger_api: LedgerApi, contract_address: str, token: Address, min_per_tx: int) -> JSONLike:
        """Handler method for the 'set_min_per_tx' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setMinPerTx(_token=token, _minPerTx=min_per_tx)

    @classmethod
    def set_token_factory(cls, ledger_api: LedgerApi, contract_address: str, token_factory: Address) -> JSONLike:
        """Handler method for the 'set_token_factory' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setTokenFactory(_tokenFactory=token_factory)

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

    @classmethod
    def get_daily_limit_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token: Address = None,
        new_limit: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'DailyLimitChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("token", token), ("newLimit", new_limit)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.DailyLimitChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_execution_daily_limit_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token: Address = None,
        new_limit: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'ExecutionDailyLimitChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("token", token), ("newLimit", new_limit)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.ExecutionDailyLimitChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_failed_message_fixed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        message_id: str | None = None,
        token: Address = None,
        recipient: Address = None,
        value: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'FailedMessageFixed' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("messageId", message_id), ("token", token), ("recipient", recipient), ("value", value))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.FailedMessageFixed().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_fee_distributed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        fee: int | None = None,
        token: Address = None,
        message_id: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'FeeDistributed' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("fee", fee), ("token", token), ("messageId", message_id))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.FeeDistributed().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_fee_distribution_failed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token: Address = None,
        fee: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'FeeDistributionFailed' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("token", token), ("fee", fee)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.FeeDistributionFailed().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_new_token_registered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        native_token: Address = None,
        bridged_token: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'NewTokenRegistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("nativeToken", native_token), ("bridgedToken", bridged_token))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.NewTokenRegistered().get_logs(
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

    @classmethod
    def get_tokens_bridged_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token: Address = None,
        recipient: Address = None,
        value: int | None = None,
        message_id: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'TokensBridged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("token", token), ("recipient", recipient), ("value", value), ("messageId", message_id))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.TokensBridged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_tokens_bridging_initiated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token: Address = None,
        sender: Address = None,
        value: int | None = None,
        message_id: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'TokensBridgingInitiated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("token", token), ("sender", sender), ("value", value), ("messageId", message_id))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.TokensBridgingInitiated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }
