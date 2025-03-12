"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904

from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class Olas(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def minting_finished(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'minting_finished' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.mintingFinished().call()
        return {"bool": result}

    @classmethod
    def name(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'name' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.name().call()
        return {"str": result}

    @classmethod
    def total_supply(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'total_supply' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.totalSupply().call()
        return {"int": result}

    @classmethod
    def permit_typehash(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'permit_typehash' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.PERMIT_TYPEHASH().call()
        return {"str": result}

    @classmethod
    def decimals(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'decimals' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.decimals().call()
        return {"int": result}

    @classmethod
    def domain_separator(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'domain_separator' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.DOMAIN_SEPARATOR().call()
        return {"str": result}

    @classmethod
    def version(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'version' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.version().call()
        return {"str": result}

    @classmethod
    def balance_of(cls, ledger_api: LedgerApi, contract_address: str, owner: Address) -> JSONLike:
        """Handler method for the 'balance_of' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.balanceOf(_owner=owner).call()
        return {"int": result}

    @classmethod
    def is_bridge(cls, ledger_api: LedgerApi, contract_address: str, address: Address) -> JSONLike:
        """Handler method for the 'is_bridge' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isBridge(_address=address).call()
        return {"bool": result}

    @classmethod
    def nonces(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address) -> JSONLike:
        """Handler method for the 'nonces' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.nonces(var_0).call()
        return {"int": result}

    @classmethod
    def get_token_interfaces_version(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_token_interfaces_version' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getTokenInterfacesVersion().call()
        return {"major": result, "minor": result, "patch": result}

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
    def symbol(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'symbol' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.symbol().call()
        return {"str": result}

    @classmethod
    def permit_typehash_legacy(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'permit_typehash_legacy' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.PERMIT_TYPEHASH_LEGACY().call()
        return {"str": result}

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
    def allowance(cls, ledger_api: LedgerApi, contract_address: str, owner: Address, spender: Address) -> JSONLike:
        """Handler method for the 'allowance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.allowance(_owner=owner, _spender=spender).call()
        return {"int": result}

    @classmethod
    def expirations(cls, ledger_api: LedgerApi, contract_address: str, var_0: Address, var_1: Address) -> JSONLike:
        """Handler method for the 'expirations' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.expirations(var_0, var_1).call()
        return {"int": result}

    @classmethod
    def approve(cls, ledger_api: LedgerApi, contract_address: str, to: Address, value: int) -> JSONLike:
        """Handler method for the 'approve' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.approve(_to=to, _value=value)

    @classmethod
    def set_bridge_contract(cls, ledger_api: LedgerApi, contract_address: str, bridge_contract: Address) -> JSONLike:
        """Handler method for the 'set_bridge_contract' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setBridgeContract(_bridgeContract=bridge_contract)

    @classmethod
    def transfer_from(
        cls, ledger_api: LedgerApi, contract_address: str, sender: Address, recipient: Address, amount: int
    ) -> JSONLike:
        """Handler method for the 'transfer_from' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferFrom(_sender=sender, _recipient=recipient, _amount=amount)

    @classmethod
    def increase_allowance(
        cls, ledger_api: LedgerApi, contract_address: str, to: Address, added_value: int
    ) -> JSONLike:
        """Handler method for the 'increase_allowance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.increaseAllowance(_to=to, _addedValue=added_value)

    @classmethod
    def transfer_and_call(
        cls, ledger_api: LedgerApi, contract_address: str, to: Address, value: int, data: str
    ) -> JSONLike:
        """Handler method for the 'transfer_and_call' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferAndCall(_to=to, _value=value, _data=data)

    @classmethod
    def mint(cls, ledger_api: LedgerApi, contract_address: str, to: Address, amount: int) -> JSONLike:
        """Handler method for the 'mint' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.mint(_to=to, _amount=amount)

    @classmethod
    def burn(cls, ledger_api: LedgerApi, contract_address: str, value: int) -> JSONLike:
        """Handler method for the 'burn' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.burn(_value=value)

    @classmethod
    def decrease_approval(
        cls, ledger_api: LedgerApi, contract_address: str, spender: Address, subtracted_value: int
    ) -> JSONLike:
        """Handler method for the 'decrease_approval' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.decreaseApproval(_spender=spender, _subtractedValue=subtracted_value)

    @classmethod
    def claim_tokens(cls, ledger_api: LedgerApi, contract_address: str, token: Address, to: Address) -> JSONLike:
        """Handler method for the 'claim_tokens' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.claimTokens(_token=token, _to=to)

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
    def finish_minting(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'finish_minting' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.finishMinting()

    @classmethod
    def permit(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        holder: Address,
        spender: Address,
        nonce: int,
        expiry: int,
        allowed: bool,
        v: int,
        r: str,
        s: str,
    ) -> JSONLike:
        """Handler method for the 'permit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.permit(
            _holder=holder, _spender=spender, _nonce=nonce, _expiry=expiry, _allowed=allowed, _v=v, _r=r, _s=s
        )

    @classmethod
    def decrease_allowance(
        cls, ledger_api: LedgerApi, contract_address: str, spender: Address, subtracted_value: int
    ) -> JSONLike:
        """Handler method for the 'decrease_allowance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.decreaseAllowance(spender=spender, subtractedValue=subtracted_value)

    @classmethod
    def transfer(cls, ledger_api: LedgerApi, contract_address: str, to: Address, value: int) -> JSONLike:
        """Handler method for the 'transfer' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transfer(_to=to, _value=value)

    @classmethod
    def push(cls, ledger_api: LedgerApi, contract_address: str, to: Address, amount: int) -> JSONLike:
        """Handler method for the 'push' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.push(_to=to, _amount=amount)

    @classmethod
    def move(cls, ledger_api: LedgerApi, contract_address: str, from_: Address, to: Address, amount: int) -> JSONLike:
        """Handler method for the 'move' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.move(_from=from_, _to=to, _amount=amount)

    @classmethod
    def permit_1(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        holder: Address,
        spender: Address,
        value: int,
        deadline: int,
        v: int,
        r: str,
        s: str,
    ) -> JSONLike:
        """Handler method for the 'permit_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.permit_1(
            _holder=holder, _spender=spender, _value=value, _deadline=deadline, _v=v, _r=r, _s=s
        )

    @classmethod
    def increase_approval(
        cls, ledger_api: LedgerApi, contract_address: str, spender: Address, added_value: int
    ) -> JSONLike:
        """Handler method for the 'increase_approval' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.increaseApproval(_spender=spender, _addedValue=added_value)

    @classmethod
    def pull(cls, ledger_api: LedgerApi, contract_address: str, from_: Address, amount: int) -> JSONLike:
        """Handler method for the 'pull' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.pull(_from=from_, _amount=amount)

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(_newOwner=new_owner)

    @classmethod
    def get_mint_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        to: Address = None,
        amount: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Mint' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("to", to), ("amount", amount)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Mint().get_logs(fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters)
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_mint_finished_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'MintFinished' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in () if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.MintFinished().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_ownership_renounced_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        previous_owner: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OwnershipRenounced' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("previousOwner", previous_owner)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.OwnershipRenounced().get_logs(
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
    def get_burn_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        burner: Address = None,
        value: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Burn' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("burner", burner), ("value", value)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Burn().get_logs(fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters)
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_transfer_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        from_: Address = None,
        to: Address = None,
        value: int | None = None,
        data: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Transfer' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("from_", from_), ("to", to), ("value", value), ("data", data))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Transfer().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_approval_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        owner: Address = None,
        spender: Address = None,
        value: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Approval' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("owner", owner), ("spender", spender), ("value", value)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Approval().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_transfer_events_2(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        from_: Address = None,
        to: Address = None,
        value: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Transfer' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("from_", from_), ("to", to), ("value", value)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Transfer().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }
