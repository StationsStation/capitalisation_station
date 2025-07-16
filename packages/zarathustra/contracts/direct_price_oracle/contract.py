"""This module contains the DirectPriceOracle contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId

from packages.zarathustra.contracts.direct_price_oracle import (
    PUBLIC_ID as DIRECT_PRICE_ORACLE_PUOBLIC_ID,
)


class DirectPriceOracle(Contract):
    """The DirectPriceOracle contract."""

    contract_id: PublicId = DIRECT_PRICE_ORACLE_PUOBLIC_ID

    @classmethod
    def pyth_adapter(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'pyth_adapter' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.PYTH_ADAPTER().call()
        return {"address": result}

    @classmethod
    def address_to_asset(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'address_to_asset' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.addressToAsset(var_0).call()
        return {"str": result}

    @classmethod
    def asset_to_price_feed_id(cls, ledger_api: LedgerApi, contract_address: str, var_0: str) -> JSONLike:
        """Handler method for the 'asset_to_price_feed_id' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.assetToPriceFeedId(var_0).call()
        return {"str": result}

    @classmethod
    def extract_message_and_signature(cls, ledger_api: LedgerApi, contract_address: str, full_data: str) -> JSONLike:
        """Handler method for the 'extract_message_and_signature' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.extractMessageAndSignature(fullData=full_data).call()
        return {"message": result, "signature": result}

    @classmethod
    def get_asset_price(cls, ledger_api: LedgerApi, contract_address: str, asset: str) -> JSONLike:
        """Handler method for the 'get_asset_price' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getAssetPrice(_asset=asset).call()
        return {"assetPrice_": result}

    @classmethod
    def get_asset_price_1(cls, ledger_api: LedgerApi, contract_address: str, asset: Address) -> JSONLike:
        """Handler method for the 'get_asset_price_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getAssetPrice_1(_asset=asset).call()
        return {"assetPrice_": result}

    @classmethod
    def get_asset_price_2(cls, ledger_api: LedgerApi, contract_address: str, asset: str) -> JSONLike:
        """Handler method for the 'get_asset_price_2' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getAssetPrice_2(_asset=asset).call()
        return {"assetPrice_": result}

    @classmethod
    def get_price_max_age(cls, ledger_api: LedgerApi, contract_address: str, nabla_contract: Address) -> JSONLike:
        """Handler method for the 'get_price_max_age' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getPriceMaxAge(_nablaContract=nabla_contract).call()
        return {"int": result}

    @classmethod
    def get_update_fee(cls, ledger_api: LedgerApi, contract_address: str, price_update_data: list[str]) -> JSONLike:
        """Handler method for the 'get_update_fee' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getUpdateFee(_priceUpdateData=price_update_data).call()
        return {"updateFee_": result}

    @classmethod
    def is_backstop_pool(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'is_backstop_pool' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isBackstopPool(var_0).call()
        return {"bool": result}

    @classmethod
    def is_price_feed_registered(cls, ledger_api: LedgerApi, contract_address: str, asset: str) -> JSONLike:
        """Handler method for the 'is_price_feed_registered' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isPriceFeedRegistered(_asset=asset).call()
        return {"bool": result}

    @classmethod
    def is_price_feed_registered_1(cls, ledger_api: LedgerApi, contract_address: str, id: str) -> JSONLike:
        """Handler method for the 'is_price_feed_registered_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isPriceFeedRegistered_1(_id=id).call()
        return {"isRegistered_": result}

    @classmethod
    def is_price_feed_registered_2(cls, ledger_api: LedgerApi, contract_address: str, token: Address) -> JSONLike:
        """Handler method for the 'is_price_feed_registered_2' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isPriceFeedRegistered_2(_token=token).call()
        return {"isRegistered_": result}

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
    def price_feed_id_to_asset(cls, ledger_api: LedgerApi, contract_address: str, var_0: str) -> JSONLike:
        """Handler method for the 'price_feed_id_to_asset' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.priceFeedIdToAsset(var_0).call()
        return {"str": result}

    @classmethod
    def validate_message(cls, ledger_api: LedgerApi, contract_address: str, full_message: str) -> JSONLike:
        """Handler method for the 'validate_message' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.validateMessage(_fullMessage=full_message).call()
        return {"bool": result}

    @classmethod
    def verify_signature(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        signer: Address,
        message: str,
        signature: str,
    ) -> JSONLike:
        """Handler method for the 'verify_signature' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.verifySignature(_signer=signer, _message=message, _signature=signature).call()
        return {"success_": result}

    @classmethod
    def register_price_feed(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address, var_1: str) -> JSONLike:
        """Handler method for the 'register_price_feed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.registerPriceFeed(var_0, var_1)

    @classmethod
    def register_price_feed_1(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        asset_name: str,
        price_feed_id: str,
    ) -> JSONLike:
        """Handler method for the 'register_price_feed_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.registerPriceFeed_1(_assetName=asset_name, _priceFeedId=price_feed_id)

    @classmethod
    def register_token(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        token_address: Address,
        asset_name: str,
    ) -> JSONLike:
        """Handler method for the 'register_token' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.registerToken(_tokenAddress=token_address, _assetName=asset_name)

    @classmethod
    def remove_backstop_pool(cls, ledger_api: LedgerApi, contract_address: str, backstop_pool: Address) -> JSONLike:
        """Handler method for the 'remove_backstop_pool' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.removeBackstopPool(_backstopPool=backstop_pool)

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
    def set_backstop_pool(cls, ledger_api: LedgerApi, contract_address: str, backstop_pool: Address) -> JSONLike:
        """Handler method for the 'set_backstop_pool' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setBackstopPool(_backstopPool=backstop_pool)

    @classmethod
    def set_price_max_age(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        nabla_contract: Address,
        new_price_max_age: int,
    ) -> JSONLike:
        """Handler method for the 'set_price_max_age' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setPriceMaxAge(_nablaContract=nabla_contract, _newPriceMaxAge=new_price_max_age)

    @classmethod
    def set_signer(cls, ledger_api: LedgerApi, contract_address: str, new_signer: Address) -> JSONLike:
        """Handler method for the 'set_signer' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setSigner(_newSigner=new_signer)

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

    @classmethod
    def unregister_price_feed(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'unregister_price_feed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.unregisterPriceFeed(var_0)

    @classmethod
    def unregister_token(cls, ledger_api: LedgerApi, contract_address: str, token_address: Address) -> JSONLike:
        """Handler method for the 'unregister_token' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.unregisterToken(_tokenAddress=token_address)

    @classmethod
    def update_price_feeds(cls, ledger_api: LedgerApi, contract_address: str, price_update_data: list[str]) -> JSONLike:
        """Handler method for the 'update_price_feeds' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.updatePriceFeeds(_priceUpdateData=price_update_data)

    @classmethod
    def get_asset_registered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        asset_name: str | None = None,
        price_feed_id: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'AssetRegistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("assetName", asset_name),
                ("priceFeedId", price_feed_id),
            )
            if value is not None
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
    def get_backstop_pool_removed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        backstop_pool: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'BackstopPoolRemoved' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("sender", sender), ("backstopPool", backstop_pool)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.BackstopPoolRemoved().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_backstop_pool_set_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        backstop_pool: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'BackstopPoolSet' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("sender", sender), ("backstopPool", backstop_pool)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.BackstopPoolSet().get_logs(
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
    def get_price_feed_update_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        id: str | None = None,
        publish_time: int | None = None,
        price: int | None = None,
        conf: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'PriceFeedUpdate' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("id", id),
                ("publishTime", publish_time),
                ("price", price),
                ("conf", conf),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.PriceFeedUpdate().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_price_feeds_updated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        update_fee: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'PriceFeedsUpdated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("sender", sender), ("updateFee", update_fee)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.PriceFeedsUpdated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_price_max_age_set_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        nabla_contract: Address = None,
        new_price_max_age: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'PriceMaxAgeSet' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("nablaContract", nabla_contract),
                ("newPriceMaxAge", new_price_max_age),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.PriceMaxAgeSet().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_signer_set_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        new_signer: Address = None,
        old_signer: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'SignerSet' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("newSigner", new_signer),
                ("oldSigner", old_signer),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.SignerSet().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_token_registered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        sender: Address = None,
        token: Address = None,
        price_feed_id: str | None = None,
        asset_name: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'TokenRegistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (
                ("sender", sender),
                ("token", token),
                ("priceFeedId", price_feed_id),
                ("assetName", asset_name),
            )
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.TokenRegistered().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }
