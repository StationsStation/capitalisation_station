"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


ADDRESS_BASE = "0x27B863F382791e0E4950497B4bbda5b69CbB10b9"


class DerolasStaking(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def assets_in_pool(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'assets_in_pool' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.assetsInPool().call()
        return {"int": result}

    @classmethod
    def balancer_router(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'balancer_router' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.balancerRouter().call()
        return {"address": result}

    @classmethod
    def can_pay_ticket(cls, ledger_api: LedgerApi, contract_address: str, claim_amount: int) -> JSONLike:
        """Handler method for the 'can_pay_ticket' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.canPayTicket(claimAmount=claim_amount).call()
        return {"bool": result}

    @classmethod
    def can_play_game(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'can_play_game' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.canPlayGame().call()
        return {"bool": result}

    @classmethod
    def claimable(cls, ledger_api: LedgerApi, contract_address: str, address: Address) -> JSONLike:
        """Handler method for the 'claimable' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.claimable(_address=address).call()
        return {"int": result}

    @classmethod
    def current_epoch(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'current_epoch' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.currentEpoch().call()
        return {"int": result}

    @classmethod
    def epoch_length(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'epoch_length' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochLength().call()
        return {"int": result}

    @classmethod
    def epoch_rewards(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'epoch_rewards' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochRewards().call()
        return {"int": result}

    @classmethod
    def epoch_to_claimable(cls, ledger_api: LedgerApi, contract_address: str, var_0: int, var_1: Address) -> JSONLike:
        """Handler method for the 'epoch_to_claimable' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToClaimable(var_0, var_1).call()
        return {"int": result}

    @classmethod
    def epoch_to_claimed(cls, ledger_api: LedgerApi, contract_address: str, var_0: int, var_1: Address) -> JSONLike:
        """Handler method for the 'epoch_to_claimed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToClaimed(var_0, var_1).call()
        return {"int": result}

    @classmethod
    def epoch_to_donations(cls, ledger_api: LedgerApi, contract_address: str, var_0: int, var_1: Address) -> JSONLike:
        """Handler method for the 'epoch_to_donations' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToDonations(var_0, var_1).call()
        return {"int": result}

    @classmethod
    def epoch_to_total_claimed(cls, ledger_api: LedgerApi, contract_address: str, var_0: int) -> JSONLike:
        """Handler method for the 'epoch_to_total_claimed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToTotalClaimed(var_0).call()
        return {"int": result}

    @classmethod
    def epoch_to_total_donated(cls, ledger_api: LedgerApi, contract_address: str, var_0: int) -> JSONLike:
        """Handler method for the 'epoch_to_total_donated' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToTotalDonated(var_0).call()
        return {"int": result}

    @classmethod
    def epoch_to_total_unclaimed(cls, ledger_api: LedgerApi, contract_address: str, var_0: int) -> JSONLike:
        """Handler method for the 'epoch_to_total_unclaimed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToTotalUnclaimed(var_0).call()
        return {"int": result}

    @classmethod
    def estimate_ticket_percentage(cls, ledger_api: LedgerApi, contract_address: str, donation: int) -> JSONLike:
        """Handler method for the 'estimate_ticket_percentage' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.estimateTicketPercentage(donation=donation).call()
        return {"int": result}

    @classmethod
    def get_current_share(cls, ledger_api: LedgerApi, contract_address: str, address: Address) -> JSONLike:
        """Handler method for the 'get_current_share' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentShare(_address=address).call()
        return {"int": result}

    @classmethod
    def get_epoch_progress(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_epoch_progress' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getEpochProgress().call()
        return {"int": result}

    @classmethod
    def incentive_balance(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'incentive_balance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.incentiveBalance().call()
        return {"int": result}

    @classmethod
    def incentive_token_address(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'incentive_token_address' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.incentiveTokenAddress().call()
        return {"address": result}

    @classmethod
    def last_auction_block(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'last_auction_block' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.lastAuctionBlock().call()
        return {"int": result}

    @classmethod
    def max_donators_per_epoch(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'max_donators_per_epoch' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.maxDonatorsPerEpoch().call()
        return {"int": result}

    @classmethod
    def minimum_donation(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'minimum_donation' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.minimumDonation().call()
        return {"int": result}

    @classmethod
    def olas_index(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'olas_index' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.olasIndex().call()
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
    def pool_id(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'pool_id' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.poolId().call()
        return {"address": result}

    @classmethod
    def total_claimed(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'total_claimed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.totalClaimed().call()
        return {"int": result}

    @classmethod
    def total_donated(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'total_donated' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.totalDonated().call()
        return {"int": result}

    @classmethod
    def total_unclaimed(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'total_unclaimed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.totalUnclaimed().call()
        return {"int": result}

    @classmethod
    def weth_index(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'weth_index' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.wethIndex().call()
        return {"int": result}

    @classmethod
    def claim(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'claim' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.claim()

    @classmethod
    def donate(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'donate' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.donate()

    @classmethod
    def end_epoch(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'end_epoch' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.endEpoch()

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
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

    @classmethod
    def get_agent_registered_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        agent_address: Address = None,
        agent_id: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'AgentRegistered' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("agentAddress", agent_address), ("agentId", agent_id)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.AgentRegistered().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_auction_ended_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        epoch_rewards: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'AuctionEnded' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("epochRewards", epoch_rewards)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.AuctionEnded().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_donation_received_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        donator_address: Address = None,
        amount: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'DonationReceived' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("donatorAddress", donator_address), ("amount", amount)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.DonationReceived().get_logs(
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
    def get_rewards_claimed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        agent_address: Address = None,
        amount: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'RewardsClaimed' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("agentAddress", agent_address), ("amount", amount)) if value is not None
        }
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.RewardsClaimed().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }

    @classmethod
    def get_unclaimed_rewards_donated_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'UnclaimedRewardsDonated' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("amount", amount)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.UnclaimedRewardsDonated().get_logs(
            fromBlock=from_block, toBlock=to_block, argument_filters=arg_filters
        )
        return {
            "events": result,
            "from_block": from_block,
            "to_block": to_block,
        }
