"""This module contains the Derolas contract interface."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId

from packages.zarathustra.contracts.derolas_staking import (
    PUBLIC_ID as DEROLAS_STAKING_PUBLIC_ID,
)


ADDRESS_BASE = "0x35CAf83118d58504C179b50D538a095ac08Ebc8f"


class DerolasStaking(Contract):
    """The DerolasStaking contract."""

    contract_id: PublicId = DEROLAS_STAKING_PUBLIC_ID

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
    def epoch_donated(cls, ledger_api: LedgerApi, contract_address: str, var_0: int) -> JSONLike:
        """Handler method for the 'epoch_donated' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochDonated(var_0).call()
        return {"bool": result}

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
    def epoch_to_end_block(cls, ledger_api: LedgerApi, contract_address: str, var_0: int) -> JSONLike:
        """Handler method for the 'epoch_to_end_block' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToEndBlock(var_0).call()
        return {"int": result}

    @classmethod
    def epoch_to_total_donated(cls, ledger_api: LedgerApi, contract_address: str, var_0: int) -> JSONLike:
        """Handler method for the 'epoch_to_total_donated' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.epochToTotalDonated(var_0).call()
        return {"int": result}

    @classmethod
    def estimate_ticket_percentage(cls, ledger_api: LedgerApi, contract_address: str, donation: int) -> JSONLike:
        """Handler method for the 'estimate_ticket_percentage' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.estimateTicketPercentage(donation=donation).call()
        return {"int": result}

    @classmethod
    def get_blocks_remaining(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_blocks_remaining' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getBlocksRemaining().call()
        return {"int": result}

    @classmethod
    def get_current_epoch(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_current_epoch' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentEpoch().call()
        return {"int": result}

    @classmethod
    def get_current_share(cls, ledger_api: LedgerApi, contract_address: str, address: Address) -> JSONLike:
        """Handler method for the 'get_current_share' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getCurrentShare(_address=address).call()
        return {"int": result}

    @classmethod
    def get_epoch_length(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_epoch_length' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getEpochLength().call()
        return {"int": result}

    @classmethod
    def get_epoch_rewards(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_epoch_rewards' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getEpochRewards().call()
        return {"int": result}

    @classmethod
    def get_game_state(cls, ledger_api: LedgerApi, contract_address: str, user: Address) -> JSONLike:
        """Handler method for the 'get_game_state' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getGameState(user=user).call()
        return {
            "_epochLength": result[0],
            "_currentEpoch": result[1],
            "_epochEndBlock": result[2],
            "_minimumDonation": result[3],
            "_blocksRemaining": result[4],
            "_epochRewards": result[5],
            "_totalDonated": result[6],
            "_totalClaimed": result[7],
            "_incentiveBalance": result[8],
            "_userCurrentDonation": result[9],
            "_userCurrentShare": result[10],
            "_userClaimable": result[11],
            "_hasClaimed": result[12],
            "_canPlayGame": result[13],
        }

    @classmethod
    def get_total_claimed(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_total_claimed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getTotalClaimed().call()
        return {"int": result}

    @classmethod
    def get_total_donated(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_total_donated' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getTotalDonated().call()
        return {"int": result}

    @classmethod
    def get_total_unclaimed(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'get_total_unclaimed' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getTotalUnclaimed().call()
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
    def permit2(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'permit2' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.permit2().call()
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
    def end_round(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'end_round' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.endRound()

    @classmethod
    def force_advance_epoch(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'force_advance_epoch' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.forceAdvanceEpoch()

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
    def top_up_incentive_balance(cls, ledger_api: LedgerApi, contract_address: str, amount: int) -> JSONLike:
        """Handler method for the 'top_up_incentive_balance' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.topUpIncentiveBalance(amount=amount)

    @classmethod
    def transfer_ownership(cls, ledger_api: LedgerApi, contract_address: str, new_owner: Address) -> JSONLike:
        """Handler method for the 'transfer_ownership' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.transferOwnership(newOwner=new_owner)

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
    def get_eth_donated_to_balancer_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'EthDonatedToBalancer' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {key: value for key, value in (("amount", amount)) if value is not None}
        to_block = to_block or "latest"
        if to_block == "latest":
            to_block = ledger_api.api.eth.block_number
        from_block = from_block or (to_block - look_back)
        result = instance.events.EthDonatedToBalancer().get_logs(
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
    def get_rewards_claimed_events(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        donator_address: Address = None,
        amount: int | None = None,
        look_back: int = 1000,
        to_block: str = "latest",
        from_block: int | None = None,
    ) -> JSONLike:
        """Handler method for the 'RewardsClaimed' events ."""

        instance = cls.get_instance(ledger_api, contract_address)
        arg_filters = {
            key: value for key, value in (("donatorAddress", donator_address), ("amount", amount)) if value is not None
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
