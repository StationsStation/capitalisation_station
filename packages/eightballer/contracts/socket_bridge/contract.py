"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class SocketBridge(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def bridge_type(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'bridge_type' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.bridgeType().call()
        return {"str": result}

    @classmethod
    def connector_cache(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'connector_cache' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.connectorCache(var_0).call()
        return {"str": result}

    @classmethod
    def get_min_fees(
        cls, ledger_api: LedgerApi, contract_address: str, connector_: Address, msg_gas_limit_: int, payload_size_: int
    ) -> JSONLike:
        """Handler method for the 'get_min_fees' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getMinFees(
            connector_=connector_, msgGasLimit_=msg_gas_limit_, payloadSize_=payload_size_
        ).call()
        return {"totalFees": result}

    @classmethod
    def has_role(cls, ledger_api: LedgerApi, contract_address: str, role_: str, address_: Address) -> JSONLike:
        """Handler method for the 'has_role' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.hasRole(role_=role_, address_=address_).call()
        return {"bool": result}

    @classmethod
    def hook__(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'hook__' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.hook__().call()
        return {"address": result}

    @classmethod
    def identifier_cache(cls, ledger_api: LedgerApi, contract_address: str, var_0: str) -> JSONLike:
        """Handler method for the 'identifier_cache' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.identifierCache(var_0).call()
        return {"str": result}

    @classmethod
    def nominee(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'nominee' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.nominee().call()
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
    def token(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'token' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.token().call()
        return {"address": result}

    @classmethod
    def valid_connectors(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'valid_connectors' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.validConnectors(var_0).call()
        return {"bool": result}

    @classmethod
    def bridge(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        receiver_: Address,
        amount_: int,
        msg_gas_limit_: int,
        connector_: Address,
        extra_data_: str,
        options_: str,
    ) -> JSONLike:
        """Handler method for the 'bridge' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.bridge(
            receiver_=receiver_,
            amount_=amount_,
            msgGasLimit_=msg_gas_limit_,
            connector_=connector_,
            extraData_=extra_data_,
            options_=options_,
        )

    @classmethod
    def claim_owner(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'claim_owner' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.claimOwner()

    @classmethod
    def grant_role(cls, ledger_api: LedgerApi, contract_address: str, role_: str, grantee_: Address) -> JSONLike:
        """Handler method for the 'grant_role' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.grantRole(role_=role_, grantee_=grantee_)

    @classmethod
    def nominate_owner(cls, ledger_api: LedgerApi, contract_address: str, nominee_: Address) -> JSONLike:
        """Handler method for the 'nominate_owner' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.nominateOwner(nominee_=nominee_)

    @classmethod
    def receive_inbound(
        cls, ledger_api: LedgerApi, contract_address: str, sibling_chain_slug_: int, payload_: str
    ) -> JSONLike:
        """Handler method for the 'receive_inbound' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.receiveInbound(siblingChainSlug_=sibling_chain_slug_, payload_=payload_)

    @classmethod
    def rescue_funds(
        cls, ledger_api: LedgerApi, contract_address: str, token_: Address, rescue_to_: Address, amount_: int
    ) -> JSONLike:
        """Handler method for the 'rescue_funds' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.rescueFunds(token_=token_, rescueTo_=rescue_to_, amount_=amount_)

    @classmethod
    def retry(cls, ledger_api: LedgerApi, contract_address: str, connector_: Address, message_id_: str) -> JSONLike:
        """Handler method for the 'retry' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.retry(connector_=connector_, messageId_=message_id_)

    @classmethod
    def revoke_role(cls, ledger_api: LedgerApi, contract_address: str, role_: str, revokee_: Address) -> JSONLike:
        """Handler method for the 'revoke_role' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.revokeRole(role_=role_, revokee_=revokee_)

    @classmethod
    def update_connector_status(
        cls, ledger_api: LedgerApi, contract_address: str, connectors: list[Address], statuses: list[bool]
    ) -> JSONLike:
        """Handler method for the 'update_connector_status' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.updateConnectorStatus(connectors=connectors, statuses=statuses)

    @classmethod
    def update_hook(cls, ledger_api: LedgerApi, contract_address: str, hook_: Address, approve_: bool) -> JSONLike:
        """Handler method for the 'update_hook' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.updateHook(hook_=hook_, approve_=approve_)

    @classmethod
    def get_bridging_tokens_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        connector: Address = None,
        sender: Address = None,
        receiver: Address = None,
        amount: int | None = None,
        message_id: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'BridgingTokens' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("connector", connector),
                ("sender", sender),
                ("receiver", receiver),
                ("amount", amount),
                ("messageId", message_id),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.BridgingTokens().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_connector_status_updated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        connector: Address = None,
        status: bool | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'ConnectorStatusUpdated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("connector", connector), ("status", status)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.ConnectorStatusUpdated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_hook_updated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        new_hook: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'HookUpdated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("newHook", new_hook)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.HookUpdated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_owner_claimed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        claimer: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OwnerClaimed' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("claimer", claimer)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.OwnerClaimed().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_owner_nominated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        nominee: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OwnerNominated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("nominee", nominee)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.OwnerNominated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_role_granted_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        role: str | None = None,
        grantee: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'RoleGranted' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("role", role), ("grantee", grantee)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.RoleGranted().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_role_revoked_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        role: str | None = None,
        revokee: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'RoleRevoked' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("role", role), ("revokee", revokee)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.RoleRevoked().get_logs(
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
        connecter: Address = None,
        receiver: Address = None,
        amount: int | None = None,
        message_id: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'TokensBridged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("connecter", connecter),
                ("receiver", receiver),
                ("amount", amount),
                ("messageId", message_id),
            )
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
