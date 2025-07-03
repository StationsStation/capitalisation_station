"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class NablaPortal(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def weth(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'weth' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.WETH().call()
        return {"address": result}

    @classmethod
    def assets_by_router(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address, var_1: Address) -> JSONLike:
        """Handler method for the 'assets_by_router' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.assetsByRouter(var_0, var_1).call()
        return {"bool": result}

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
    def get_router_assets(cls, ledger_api: LedgerApi, contract_address: str, router: Address) -> JSONLike:
        """Handler method for the 'get_router_assets' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getRouterAssets(_router=router).call()
        return {"routerAssets_": result}

    @classmethod
    def get_routers(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_routers' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getRouters().call()
        return {"routers_": result}

    @classmethod
    def guard_on(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'guard_on' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.guardOn(var_0).call()
        return {"bool": result}

    @classmethod
    def guard_oracle(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'guard_oracle' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.guardOracle().call()
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
    def quote_swap_exact_tokens_for_tokens(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        token_path: list[Address],
        router_path: list[Address],
        token_prices: list[int],
    ) -> JSONLike:
        """Handler method for the 'quote_swap_exact_tokens_for_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.quoteSwapExactTokensForTokens(
            _amountIn=amount_in, _tokenPath=token_path, _routerPath=router_path, _tokenPrices=token_prices
        ).call()
        return {"amountOut_": result}

    @classmethod
    def router_assets(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address, var_1: int) -> JSONLike:
        """Handler method for the 'router_assets' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.routerAssets(var_0, var_1).call()
        return {"address": result}

    @classmethod
    def routers(cls, ledger_api: LedgerApi, contract_address: str, var_0: int) -> JSONLike:
        """Handler method for the 'routers' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.routers(var_0).call()
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
    def en_garde(cls, ledger_api: LedgerApi, contract_address: str, router: Address) -> JSONLike:
        """Handler method for the 'en_garde' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.enGarde(_router=router)

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
    def register_asset(cls, ledger_api: LedgerApi, contract_address: str, router: Address, asset: Address) -> JSONLike:
        """Handler method for the 'register_asset' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.registerAsset(_router=router, _asset=asset)

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
    def set_guard_oracle(cls, ledger_api: LedgerApi, contract_address: str, guard_oracle_address: Address) -> JSONLike:
        """Handler method for the 'set_guard_oracle' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setGuardOracle(_guardOracleAddress=guard_oracle_address)

    @classmethod
    def set_oracle_adapter(cls, ledger_api: LedgerApi, contract_address: str, new_oracle_adapter: Address) -> JSONLike:
        """Handler method for the 'set_oracle_adapter' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setOracleAdapter(_newOracleAdapter=new_oracle_adapter)

    @classmethod
    def stand_down(cls, ledger_api: LedgerApi, contract_address: str, router: Address) -> JSONLike:
        """Handler method for the 'stand_down' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.standDown(_router=router)

    @classmethod
    def swap_eth_for_exact_tokens(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        amount_out_min: int,
        token_path: list[Address],
        router_path: list[Address],
        to: Address,
        deadline: int,
        price_update_data: list[str],
    ) -> JSONLike:
        """Handler method for the 'swap_eth_for_exact_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.swapEthForExactTokens(
            _amountIn=amount_in,
            _amountOutMin=amount_out_min,
            _tokenPath=token_path,
            _routerPath=router_path,
            _to=to,
            _deadline=deadline,
            _priceUpdateData=price_update_data,
        )

    @classmethod
    def swap_exact_tokens_for_eth(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        amount_out_min: int,
        token_path: list[Address],
        router_path: list[Address],
        to: Address,
        deadline: int,
        price_update_data: list[str],
    ) -> JSONLike:
        """Handler method for the 'swap_exact_tokens_for_eth' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.swapExactTokensForEth(
            _amountIn=amount_in,
            _amountOutMin=amount_out_min,
            _tokenPath=token_path,
            _routerPath=router_path,
            _to=to,
            _deadline=deadline,
            _priceUpdateData=price_update_data,
        )

    @classmethod
    def swap_exact_tokens_for_tokens(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        amount_out_min: int,
        token_path: list[Address],
        router_path: list[Address],
        to: Address,
        deadline: int,
        price_update_data: list[str],
    ) -> JSONLike:
        """Handler method for the 'swap_exact_tokens_for_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.swapExactTokensForTokens(
            _amountIn=amount_in,
            _amountOutMin=amount_out_min,
            _tokenPath=token_path,
            _routerPath=router_path,
            _to=to,
            _deadline=deadline,
            _priceUpdateData=price_update_data,
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
    def unregister_asset(
        cls, ledger_api: LedgerApi, contract_address: str, router: Address, asset: Address
    ) -> JSONLike:
        """Handler method for the 'unregister_asset' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.unregisterAsset(_router=router, _asset=asset)

    @classmethod
    def get_asset_registered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        router: Address = None,
        asset: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'AssetRegistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("sender", sender), ("router", router), ("asset", asset)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.AssetRegistered().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_asset_unregistered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        router: Address = None,
        asset: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'AssetUnregistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("sender", sender), ("router", router), ("asset", asset)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.AssetUnregistered().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_eth_for_exact_tokens_swapped_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        to: Address = None,
        router_path: list[Address] | None = None,
        token_path: list[Address] | None = None,
        swap_amounts: list[int] | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'EthForExactTokensSwapped' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("to", to),
                ("routerPath", router_path),
                ("tokenPath", token_path),
                ("swapAmounts", swap_amounts),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.EthForExactTokensSwapped().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_exact_tokens_for_eth_swapped_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        to: Address = None,
        router_path: list[Address] | None = None,
        token_path: list[Address] | None = None,
        swap_amounts: list[int] | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'ExactTokensForEthSwapped' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("to", to),
                ("routerPath", router_path),
                ("tokenPath", token_path),
                ("swapAmounts", swap_amounts),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.ExactTokensForEthSwapped().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_exact_tokens_for_tokens_swapped_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        to: Address = None,
        router_path: list[Address] | None = None,
        token_path: list[Address] | None = None,
        swap_amounts: list[int] | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'ExactTokensForTokensSwapped' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("to", to),
                ("routerPath", router_path),
                ("tokenPath", token_path),
                ("swapAmounts", swap_amounts),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.ExactTokensForTokensSwapped().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

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
            for key, value in (("owner", owner), ("oldGate", old_gate), ("newGate", new_gate))
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
    def get_guard_activated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        router: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'GuardActivated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("sender", sender), ("router", router)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.GuardActivated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_guard_deactivated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        router: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'GuardDeactivated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("sender", sender), ("router", router)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.GuardDeactivated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_guard_oracle_set_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        new_guard_oracle: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'GuardOracleSet' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("sender", sender), ("newGuardOracle", new_guard_oracle)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.GuardOracleSet().get_logs(
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
        new_oracle_adapter: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OracleAdapterSet' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("sender", sender), ("newOracleAdapter", new_oracle_adapter))
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
