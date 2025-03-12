"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904

from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class Lbtc(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def bascule(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'bascule' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.Bascule().call()
        return {"address": result}

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
    def allowance(cls, ledger_api: LedgerApi, contract_address: str, owner: Address, spender: Address) -> JSONLike:
        """Handler method for the 'allowance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.allowance(owner=owner, spender=spender).call()
        return {"int": result}

    @classmethod
    def balance_of(cls, ledger_api: LedgerApi, contract_address: str, account: Address) -> JSONLike:
        """Handler method for the 'balance_of' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.balanceOf(account=account).call()
        return {"int": result}

    @classmethod
    def calc_unstake_request_amount(
        cls, ledger_api: LedgerApi, contract_address: str, script_pubkey: str, amount: int
    ) -> JSONLike:
        """Handler method for the 'calc_unstake_request_amount' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.calcUnstakeRequestAmount(scriptPubkey=script_pubkey, amount=amount).call()
        return {"amountAfterFee": result, "isAboveDust": result}

    @classmethod
    def consortium(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'consortium' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.consortium().call()
        return {"address": result}

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
    def eip712_domain(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'eip712_domain' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.eip712Domain().call()
        return {
            "fields": result,
            "name": result,
            "version": result,
            "chainId": result,
            "verifyingContract": result,
            "salt": result,
            "extensions": result,
        }

    @classmethod
    def get_burn_commission(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_burn_commission' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getBurnCommission().call()
        return {"int": result}

    @classmethod
    def get_dust_fee_rate(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_dust_fee_rate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getDustFeeRate().call()
        return {"int": result}

    @classmethod
    def get_mint_fee(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_mint_fee' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getMintFee().call()
        return {"int": result}

    @classmethod
    def get_treasury(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_treasury' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getTreasury().call()
        return {"address": result}

    @classmethod
    def is_claimer(cls, ledger_api: LedgerApi, contract_address: str, claimer: Address) -> JSONLike:
        """Handler method for the 'is_claimer' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isClaimer(claimer=claimer).call()
        return {"bool": result}

    @classmethod
    def is_minter(cls, ledger_api: LedgerApi, contract_address: str, minter: Address) -> JSONLike:
        """Handler method for the 'is_minter' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.isMinter(minter=minter).call()
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
    def nonces(cls, ledger_api: LedgerApi, contract_address: str, owner: Address) -> JSONLike:
        """Handler method for the 'nonces' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.nonces(owner=owner).call()
        return {"int": result}

    @classmethod
    def operator(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'operator' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.operator().call()
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
    def pauser(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'pauser' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.pauser().call()
        return {"address": result}

    @classmethod
    def pending_owner(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'pending_owner' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.pendingOwner().call()
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
    def accept_ownership(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'accept_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.acceptOwnership()

    @classmethod
    def add_claimer(cls, ledger_api: LedgerApi, contract_address: str, new_claimer: Address) -> JSONLike:
        """Handler method for the 'add_claimer' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.addClaimer(newClaimer=new_claimer)

    @classmethod
    def add_minter(cls, ledger_api: LedgerApi, contract_address: str, new_minter: Address) -> JSONLike:
        """Handler method for the 'add_minter' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.addMinter(newMinter=new_minter)

    @classmethod
    def approve(cls, ledger_api: LedgerApi, contract_address: str, spender: Address, value: int) -> JSONLike:
        """Handler method for the 'approve' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.approve(spender=spender, value=value)

    @classmethod
    def batch_mint(cls, ledger_api: LedgerApi, contract_address: str, to: list[Address], amount: list[int]) -> JSONLike:
        """Handler method for the 'batch_mint' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.batchMint(to=to, amount=amount)

    @classmethod
    def batch_mint_1(
        cls, ledger_api: LedgerApi, contract_address: str, payload: list[str], proof: list[str]
    ) -> JSONLike:
        """Handler method for the 'batch_mint_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.batchMint_1(payload=payload, proof=proof)

    @classmethod
    def batch_mint_with_fee(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        mint_payload: list[str],
        proof: list[str],
        fee_payload: list[str],
        user_signature: list[str],
    ) -> JSONLike:
        """Handler method for the 'batch_mint_with_fee' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.batchMintWithFee(
            mintPayload=mint_payload, proof=proof, feePayload=fee_payload, userSignature=user_signature
        )

    @classmethod
    def burn(cls, ledger_api: LedgerApi, contract_address: str, amount: int) -> JSONLike:
        """Handler method for the 'burn' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.burn(amount=amount)

    @classmethod
    def burn_1(cls, ledger_api: LedgerApi, contract_address: str, from_: Address, amount: int) -> JSONLike:
        """Handler method for the 'burn_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.burn_1(from_=from_, amount=amount)

    @classmethod
    def change_bascule(cls, ledger_api: LedgerApi, contract_address: str, new_val: Address) -> JSONLike:
        """Handler method for the 'change_bascule' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.changeBascule(newVal=new_val)

    @classmethod
    def change_burn_commission(cls, ledger_api: LedgerApi, contract_address: str, new_value: int) -> JSONLike:
        """Handler method for the 'change_burn_commission' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.changeBurnCommission(newValue=new_value)

    @classmethod
    def change_consortium(cls, ledger_api: LedgerApi, contract_address: str, new_val: Address) -> JSONLike:
        """Handler method for the 'change_consortium' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.changeConsortium(newVal=new_val)

    @classmethod
    def change_dust_fee_rate(cls, ledger_api: LedgerApi, contract_address: str, new_rate: int) -> JSONLike:
        """Handler method for the 'change_dust_fee_rate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.changeDustFeeRate(newRate=new_rate)

    @classmethod
    def change_name_and_symbol(cls, ledger_api: LedgerApi, contract_address: str, name_: str, symbol_: str) -> JSONLike:
        """Handler method for the 'change_name_and_symbol' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.changeNameAndSymbol(name_=name_, symbol_=symbol_)

    @classmethod
    def change_treasury_address(cls, ledger_api: LedgerApi, contract_address: str, new_value: Address) -> JSONLike:
        """Handler method for the 'change_treasury_address' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.changeTreasuryAddress(newValue=new_value)

    @classmethod
    def initialize(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        consortium_: Address,
        burn_commission_: int,
        treasury: Address,
        owner_: Address,
    ) -> JSONLike:
        """Handler method for the 'initialize' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.initialize(
            consortium_=consortium_, burnCommission_=burn_commission_, treasury=treasury, owner_=owner_
        )

    @classmethod
    def mint(cls, ledger_api: LedgerApi, contract_address: str, to: Address, amount: int) -> JSONLike:
        """Handler method for the 'mint' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.mint(to=to, amount=amount)

    @classmethod
    def mint_1(cls, ledger_api: LedgerApi, contract_address: str, payload: str, proof: str) -> JSONLike:
        """Handler method for the 'mint_1' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.mint_1(payload=payload, proof=proof)

    @classmethod
    def mint_with_fee(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        mint_payload: str,
        proof: str,
        fee_payload: str,
        user_signature: str,
    ) -> JSONLike:
        """Handler method for the 'mint_with_fee' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.mintWithFee(
            mintPayload=mint_payload, proof=proof, feePayload=fee_payload, userSignature=user_signature
        )

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
    def permit(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        owner: Address,
        spender: Address,
        value: int,
        deadline: int,
        v: int,
        r: str,
        s: str,
    ) -> JSONLike:
        """Handler method for the 'permit' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.permit(owner=owner, spender=spender, value=value, deadline=deadline, v=v, r=r, s=s)

    @classmethod
    def redeem(cls, ledger_api: LedgerApi, contract_address: str, script_pubkey: str, amount: int) -> JSONLike:
        """Handler method for the 'redeem' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.redeem(scriptPubkey=script_pubkey, amount=amount)

    @classmethod
    def reinitialize(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'reinitialize' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.reinitialize()

    @classmethod
    def remove_claimer(cls, ledger_api: LedgerApi, contract_address: str, old_claimer: Address) -> JSONLike:
        """Handler method for the 'remove_claimer' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.removeClaimer(oldClaimer=old_claimer)

    @classmethod
    def remove_minter(cls, ledger_api: LedgerApi, contract_address: str, old_minter: Address) -> JSONLike:
        """Handler method for the 'remove_minter' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.removeMinter(oldMinter=old_minter)

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
    def set_mint_fee(cls, ledger_api: LedgerApi, contract_address: str, fee: int) -> JSONLike:
        """Handler method for the 'set_mint_fee' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.setMintFee(fee=fee)

    @classmethod
    def toggle_withdrawals(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'toggle_withdrawals' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.toggleWithdrawals()

    @classmethod
    def transfer(cls, ledger_api: LedgerApi, contract_address: str, to: Address, value: int) -> JSONLike:
        """Handler method for the 'transfer' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transfer(to=to, value=value)

    @classmethod
    def transfer_from(
        cls, ledger_api: LedgerApi, contract_address: str, from_: Address, to: Address, value: int
    ) -> JSONLike:
        """Handler method for the 'transfer_from' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferFrom(from_=from_, to=to, value=value)

    @classmethod
    def transfer_operator_role(cls, ledger_api: LedgerApi, contract_address: str, new_operator: Address) -> JSONLike:
        """Handler method for the 'transfer_operator_role' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOperatorRole(newOperator=new_operator)

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

    @classmethod
    def transfer_pauser_role(cls, ledger_api: LedgerApi, contract_address: str, new_pauser: Address) -> JSONLike:
        """Handler method for the 'transfer_pauser_role' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferPauserRole(newPauser=new_pauser)

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
    def get_bascule_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        prev_val: Address = None,
        new_val: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'BasculeChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("prevVal", prev_val), ("newVal", new_val)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.BasculeChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_batch_mint_skipped_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        payload_hash: str | None = None,
        payload: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'BatchMintSkipped' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("payloadHash", payload_hash), ("payload", payload)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.BatchMintSkipped().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_bridge_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        prev_val: Address = None,
        new_val: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'BridgeChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("prevVal", prev_val), ("newVal", new_val)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.BridgeChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_burn_commission_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        prev_value: int | None = None,
        new_value: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'BurnCommissionChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("prevValue", prev_value), ("newValue", new_value)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.BurnCommissionChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_claimer_updated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        claimer: Address = None,
        is_claimer: bool | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'ClaimerUpdated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("claimer", claimer), ("isClaimer", is_claimer)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.ClaimerUpdated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_consortium_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        prev_val: Address = None,
        new_val: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'ConsortiumChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("prevVal", prev_val), ("newVal", new_val)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.ConsortiumChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_dust_fee_rate_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        old_rate: int | None = None,
        new_rate: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'DustFeeRateChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("oldRate", old_rate), ("newRate", new_rate)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.DustFeeRateChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_fee_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        old_fee: int | None = None,
        new_fee: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'FeeChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("oldFee", old_fee), ("newFee", new_fee)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.FeeChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_fee_charged_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        fee: int | None = None,
        user_signature: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'FeeCharged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("fee", fee), ("userSignature", user_signature)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.FeeCharged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_initialized_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        version: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'Initialized' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("version", version)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.Initialized().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_mint_proof_consumed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        recipient: Address = None,
        payload_hash: str | None = None,
        payload: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'MintProofConsumed' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("recipient", recipient), ("payloadHash", payload_hash), ("payload", payload))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.MintProofConsumed().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_minter_updated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        minter: Address = None,
        is_minter: bool | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'MinterUpdated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("minter", minter), ("isMinter", is_minter)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.MinterUpdated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_name_and_symbol_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        name: str | None = None,
        symbol: str | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'NameAndSymbolChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("name", name), ("symbol", symbol)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.NameAndSymbolChanged().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_operator_role_transferred_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        previous_operator: Address = None,
        new_operator: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OperatorRoleTransferred' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("previousOperator", previous_operator), ("newOperator", new_operator))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.OperatorRoleTransferred().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_ownership_transfer_started_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        previous_owner: Address = None,
        new_owner: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'OwnershipTransferStarted' events ."""

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
        result = instance.events.OwnershipTransferStarted().get_logs(
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
    def get_pauser_role_transferred_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        previous_pauser: Address = None,
        new_pauser: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'PauserRoleTransferred' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("previousPauser", previous_pauser), ("newPauser", new_pauser))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.PauserRoleTransferred().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
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

    @classmethod
    def get_treasury_address_changed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        prev_value: Address = None,
        new_value: Address = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'TreasuryAddressChanged' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("prevValue", prev_value), ("newValue", new_value)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.TreasuryAddressChanged().get_logs(
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

    @classmethod
    def get_unstake_request_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        from_address: Address = None,
        script_pub_key: str | None = None,
        amount: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'UnstakeRequest' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value
            for key, value in (("fromAddress", from_address), ("scriptPubKey", script_pub_key), ("amount", amount))
            if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.UnstakeRequest().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_withdrawals_enabled_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        var__none: bool | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'WithdrawalsEnabled' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("", var__none)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.WithdrawalsEnabled().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }
