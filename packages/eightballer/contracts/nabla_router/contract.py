"""This module contains the NableRouter contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId

from packages.eightballer.contracts.nabla_router import (
    PUBLIC_ID as NABLA_ROUTER_PUBLIC_ID,
)


class NablaRouter(Contract):
    """The NablaRouter contract."""

    contract_id: PublicId = NABLA_ROUTER_PUBLIC_ID

    @classmethod
    def get_amount_out(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        token_in_out: list[Address],
        token_prices: list[int],
    ) -> JSONLike:
        """Handler method for the 'get_amount_out' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getAmountOut(
            _amountIn=amount_in, _tokenInOut=token_in_out, _tokenPrices=token_prices
        ).call()
        return {"amountOut_": result, "swapFee_": result}

    @classmethod
    def get_gate(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_gate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getGate().call()
        return {"address": result}

    @classmethod
    def is_allowed(cls, ledger_api: LedgerApi, contract_address: str, user: Address, amount: int) -> JSONLike:
        """Handler method for the 'is_allowed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isAllowed(_user=user, _amount=amount).call()
        return {"bool": result}

    @classmethod
    def is_gated(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'is_gated' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isGated().call()
        return {"bool": result}

    @classmethod
    def oracle_adapter(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'oracle_adapter' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.oracleAdapter().call()
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
    def paused(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'paused' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.paused().call()
        return {"bool": result}

    @classmethod
    def pool_by_asset(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'pool_by_asset' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.poolByAsset(var_0).call()
        return {"address": result}

    @classmethod
    def disable_gated_access(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'disable_gated_access' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.disableGatedAccess()

    @classmethod
    def enable_gated_access(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'enable_gated_access' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.enableGatedAccess()

    @classmethod
    def pause(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'pause' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.pause()

    @classmethod
    def register_pool(cls, ledger_api: LedgerApi, contract_address: str, swap_pool: Address) -> JSONLike:
        """Handler method for the 'register_pool' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.registerPool(_swapPool=swap_pool)

    @classmethod
    def renounce_ownership(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'renounce_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.renounceOwnership()

    @classmethod
    def set_gate(cls, ledger_api: LedgerApi, contract_address: str, new_gate: Address) -> JSONLike:
        """Handler method for the 'set_gate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setGate(_newGate=new_gate)

    @classmethod
    def set_oracle_adapter(cls, ledger_api: LedgerApi, contract_address: str, new_oracle_adapter: Address) -> JSONLike:
        """Handler method for the 'set_oracle_adapter' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setOracleAdapter(_newOracleAdapter=new_oracle_adapter)

    @classmethod
    def swap_exact_tokens_for_tokens(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        amount_out_min: int,
        token_in_out: list[Address],
        to: Address,
        deadline: int,
        price_update_data: list[str],
    ) -> JSONLike:
        """Handler method for the 'swap_exact_tokens_for_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.swapExactTokensForTokens(
            _amountIn=amount_in,
            _amountOutMin=amount_out_min,
            _tokenInOut=token_in_out,
            _to=to,
            _deadline=deadline,
            _priceUpdateData=price_update_data,
        )

    @classmethod
    def swap_exact_tokens_for_tokens_without_price_feed_update(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        amount_out_min: int,
        token_in_out: list[Address],
        to: Address,
        deadline: int,
    ) -> JSONLike:
        """Handler method for the 'swap_exact_tokens_for_tokens_without_price_feed_update' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.swapExactTokensForTokensWithoutPriceFeedUpdate(
            _amountIn=amount_in,
            _amountOutMin=amount_out_min,
            _tokenInOut=token_in_out,
            _to=to,
            _deadline=deadline,
        )

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

    @classmethod
    def unpause(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'unpause' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.unpause()

    @classmethod
    def unregister_pool(cls, ledger_api: LedgerApi, contract_address: str, asset: Address) -> JSONLike:
        """Handler method for the 'unregister_pool' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.unregisterPool(_asset=asset)

    @classmethod
    def get_gate_updated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        owner: Address = None,
        old_gate: Address = None,
        new_gate: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'GateUpdated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("owner", owner),
                ("oldGate", old_gate),
                ("newGate", new_gate),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.GateUpdated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_gated_access_disabled_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        owner: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'GatedAccessDisabled' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("owner", owner)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.GatedAccessDisabled().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_gated_access_enabled_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        owner: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'GatedAccessEnabled' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("owner", owner)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.GatedAccessEnabled().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_oracle_adapter_set_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        old_oracle_adapter: Address = None,
        new_oracle_adapter: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OracleAdapterSet' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("oldOracleAdapter", old_oracle_adapter),
                ("newOracleAdapter", new_oracle_adapter),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.OracleAdapterSet().get_logs(
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
            for key, value in (
                ("previousOwner", previous_owner),
                ("newOwner", new_owner),
            )
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
    def get_paused_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        account: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Paused' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("account", account)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Paused().get_logs(fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters)
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_swap_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        amount_in: int | None = None,
        amount_out: int | None = None,
        token_in: Address = None,
        token_out: Address = None,
        to: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Swap' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("amountIn", amount_in),
                ("amountOut", amount_out),
                ("tokenIn", token_in),
                ("tokenOut", token_out),
                ("to", to),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Swap().get_logs(fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters)
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_swap_pool_registered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        pool: Address = None,
        asset: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'SwapPoolRegistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("sender", sender), ("pool", pool), ("asset", asset)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.SwapPoolRegistered().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_swap_pool_unregistered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        asset: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'SwapPoolUnregistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("sender", sender), ("asset", asset)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.SwapPoolUnregistered().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_unpaused_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        account: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Unpaused' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("account", account)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Unpaused().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }
