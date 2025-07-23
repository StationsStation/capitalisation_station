# ------------------------------------------------------------------------------
#
#   Copyright 2025 zarathustra
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a behaviours of the Derolas Automator."""

import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, cast
from dataclasses import dataclass

from aea_ledger_ethereum import (
    HexBytes,
    JSONLike,
    EthereumApi,
    SignedTransaction,
    try_decorator,
)
from aea.skills.behaviours import State, FSMBehaviour, TickerBehaviour

from packages.zarathustra.contracts.derolas_staking.contract import DerolasStaking


@dataclass
class GameState:
    """Game state dataclass."""

    current_epoch: int
    epoch_length: int
    epoch_end_block: int
    minimum_donation: int
    blocks_remaining: int
    epoch_rewards: int
    total_donated: int
    total_claimed: int
    incentive_balance: int
    user_current_donation: int
    user_current_share: int
    user_claimable: int
    has_claimed: bool
    can_play_game: bool


SLEEP = 3
GAS = 5_000_000
GAS_PREMIUM = 1.1
TX_MINING_TIMEOUT = 120  # seconds
BLOCK_MARGIN = 10

# ruff: noqa: BLE001
# - BLE001: Do not catch blind exception: `Exception`


def signed_tx_to_dict(signed_transaction: Any) -> dict[str, str | int]:
    """Write SignedTransaction to dict."""
    signed_transaction_dict: dict[str, str | int] = {
        "raw_transaction": cast(str, signed_transaction.raw_transaction.hex()),
        "hash": cast(str, signed_transaction.hash.hex()),
        "r": cast(int, signed_transaction.r),
        "s": cast(int, signed_transaction.s),
        "v": cast(int, signed_transaction.v),
    }
    return signed_transaction_dict


@try_decorator("Unable to send transaction: {}", logger_method="warning")
def try_send_signed_transaction(ethereum_api: EthereumApi, tx_signed: JSONLike, **_kwargs: Any) -> str | None:
    """Try send a raw signed transaction."""
    signed_transaction = SignedTransactionTranslator.from_dict(tx_signed)
    hex_value = ethereum_api.api.eth.send_raw_transaction(  # pylint: disable=no-member
        signed_transaction.raw_transaction
    )
    tx_digest = hex_value.hex()
    if not tx_digest.startswith("0x"):
        tx_digest = "0x" + tx_digest
    return tx_digest


class SignedTransactionTranslator:
    """Translator for SignedTransaction."""

    @staticmethod
    def to_dict(signed_transaction: SignedTransaction) -> dict[str, str | int]:
        """Write SignedTransaction to dict."""
        signed_transaction_dict: dict[str, str | int] = {
            "raw_transaction": cast(str, signed_transaction.raw_transaction.hex()),
            "hash": cast(str, signed_transaction.hash.hex()),
            "r": cast(int, signed_transaction.r),
            "s": cast(int, signed_transaction.s),
            "v": cast(int, signed_transaction.v),
        }
        return signed_transaction_dict

    @staticmethod
    def from_dict(signed_transaction_dict: JSONLike) -> SignedTransaction:
        """Get SignedTransaction from dict."""
        if not isinstance(signed_transaction_dict, dict) and len(signed_transaction_dict) == 5:
            msg = f"Invalid for conversion. Found object: {signed_transaction_dict}."
            raise ValueError(  # pragma: nocover
                msg
            )
        return SignedTransaction(
            raw_transaction=HexBytes(cast(str, signed_transaction_dict["raw_transaction"])),
            hash=HexBytes(cast(str, signed_transaction_dict["hash"])),
            r=cast(int, signed_transaction_dict["r"]),
            s=cast(int, signed_transaction_dict["s"]),
            v=cast(int, signed_transaction_dict["v"]),
        )


class DerolasautomatorabciappEvents(Enum):
    """Events for the fsm."""

    EPOCH_ENDED = "EPOCH_ENDED"
    GAME_ON = "GAME_ON"
    MAX_DONATORS_REACHED = "MAX_DONATORS_REACHED"
    NO_TRIGGER = "NO_TRIGGER"
    ELIGIBLE_TO_DONATE = "ELIGIBLE_TO_DONATE"
    EPOCH_ONGOING = "EPOCH_ONGOING"
    CLAIMED = "CLAIMED"
    DONATED = "DONATED"
    EPOCH_FINISHED = "EPOCH_FINISHED"
    EPOCH_END_NEAR = "EPOCH_END_NEAR"
    TX_TIMEOUT = "TX_TIMEOUT"
    CANNOT_PLAY_GAME = "CANNOT_PLAY_GAME"
    TX_FAILED = "TX_FAILED"
    CLAIMABLE = "CLAIMABLE"
    ALREADY_DONATED = "ALREADY_DONATED"
    ERROR = "ERROR"


class DerolasautomatorabciappStates(Enum):
    """States for the fsm."""

    AWAITTRIGGERROUND = "awaittriggerround"
    CHECKREADYTODONATEROUND = "checkreadytodonateround"
    MAKECLAIMROUND = "makeclaimround"
    ENDEPOCHROUND = "endepochround"
    CHECKEPOCHROUND = "checkepochround"
    DONATEROUND = "donateround"


class BaseState(State, ABC):  # noqa: PLR0904
    """Base class for states."""

    _state: DerolasautomatorabciappStates = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._event = None
        self._is_done = False

    @abstractmethod
    def act(self) -> None:
        """Perfom the act."""
        raise NotImplementedError

    def is_done(self) -> bool:
        """Is done."""
        return self._is_done

    @property
    def event(self) -> str | None:
        """Current event."""
        return self._event

    @property
    def name(self) -> str:
        """Name of the class."""
        return self.__class__.__name__

    @property
    def ledger_api_dialogues(self):
        """Ledger API Dialogues."""
        return self.context.ledger_api_dialogues

    @property
    def contract_api_dialogues(self):
        """Contract API Dialogues."""
        return self.context.contract_api_dialogues

    @property
    def derolas_staking_contract(self) -> DerolasStaking:
        """Derolas Staking contract."""
        return self.context.derolas_state.derolas_staking_contract

    @property
    def derolas_contract_address(self):
        """Derolas Staking contract."""
        return self.context.derolas_state.derolas_contract_address

    @property
    def base_ledger_api(self):
        """Base Ledger API."""
        return self.context.derolas_state.base_ledger_api

    @property
    def crypto(self):
        """Ethereum crypto."""
        return self.context.derolas_state.crypto

    def build_transaction(self, func, value: int = 0):
        """Build the transaction."""

        nonce = self.base_ledger_api.api.eth.get_transaction_count(self.crypto.address)

        txn = func.build_transaction(
            {
                "from": self.crypto.address,
                "nonce": nonce,
                "gas": GAS,
                "gasPrice": int(self.base_ledger_api.api.eth.gas_price * GAS_PREMIUM),
                "value": value,
            }
        )
        try:
            self.base_ledger_api.api.eth.call(txn)  # pylint: disable=no-member
        except Exception as e:
            self.context.logger.warning(f"Transaction call failed: {e}")
            raise
        self.context.logger.debug(f"Transaction built: {txn}")
        return txn

    def simulate_tx(self, raw_tx) -> None:
        """Simulate the transaction."""
        self.base_ledger_api.api.eth.call(raw_tx)  # pylint: disable=no-member

    @property
    def can_play_game(self) -> bool:
        """Call "can_play_game" on Derolas contract."""

        return self.derolas_staking_contract.can_play_game(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )["bool"]

    @property
    def current_epoch(self) -> int:
        """Call "current_epoch" on Derolas contract."""

        return self.derolas_staking_contract.current_epoch(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )["int"]

    def get_blocks_remaining(self) -> int:
        """Call "get_blocks_remaining" on Derolas contract."""

        return self.derolas_staking_contract.get_blocks_remaining(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )["int"]

    def epoch_to_donations(self, epoch: int, sender: str) -> int:
        """Call "epoch_to_donations" on Derolas contract."""

        return self.derolas_staking_contract.epoch_to_donations(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
            var_0=epoch,
            var_1=sender,
        )["int"]

    @property
    def epoch_length(self) -> int:
        """Call "get_epoch_length" on Derolas contract."""

        return self.derolas_staking_contract.get_epoch_length(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )["int"]

    @property
    def current_block(self) -> int:
        """Get current block number."""
        return self.base_ledger_api.get_state("get_block_number")["get_block_number_result"]

    @property
    def minimum_donation(self):
        """Call "minimum_donation" on Derolas contract."""

        return self.derolas_staking_contract.minimum_donation(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )["int"]

    @property
    def pending_donations(self):
        """Pending donations from eightballer/skills/simple_fsm PostTradeRound."""
        return self.context.shared_state.get("state").pending_donations

    @property
    def game_state(self) -> GameState:
        """Get the game state."""
        state = self.derolas_staking_contract.get_game_state(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
            user=self.crypto.address,
        )
        return GameState(*state.values())


class AwaitTriggerRound(BaseState):
    """This class implements the behaviour of the state AwaitTriggerRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.AWAITTRIGGERROUND

    def act(self) -> None:
        """Perfom the act."""

        try:
            game_state = self.game_state
            self.context.logger.debug(f"{self.name}: game state: {game_state}")
            if not game_state.blocks_remaining:
                self._event = DerolasautomatorabciappEvents.EPOCH_FINISHED
            elif game_state.user_claimable > 0:
                self._event = DerolasautomatorabciappEvents.CLAIMABLE
            elif not self.pending_donations:
                self._event = DerolasautomatorabciappEvents.NO_TRIGGER
            elif game_state.can_play_game:
                self._event = DerolasautomatorabciappEvents.GAME_ON
            else:
                self._event = DerolasautomatorabciappEvents.CANNOT_PLAY_GAME
            self.context.logger.info(f"{self.name}: event {self._event}")
        except Exception as e:
            self.context.logger.info(f"Exception in {self.name}: {e}")
            self._event = DerolasautomatorabciappEvents.ERROR

        self._is_done = True

    @property
    def claimable(self) -> int:
        """Call "claimable" on Derolas contract."""

        return self.derolas_staking_contract.claimable(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
            address=self.crypto.address,
        )["int"]


class CheckEpochRound(BaseState):
    """This class implements the behaviour of the state CheckEpochRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.CHECKEPOCHROUND

    def act(self) -> None:
        """Perfom the act."""

        try:
            game_state: GameState = self.game_state
            if game_state.blocks_remaining == 0:
                self._event = DerolasautomatorabciappEvents.EPOCH_FINISHED
            elif not game_state.can_play_game:
                self._event = DerolasautomatorabciappEvents.CANNOT_PLAY_GAME
            elif game_state.blocks_remaining < BLOCK_MARGIN:
                self._event = DerolasautomatorabciappEvents.EPOCH_END_NEAR
            else:
                self._event = DerolasautomatorabciappEvents.EPOCH_ONGOING
            self.context.logger.debug(f"{self.name}: event {self._event}")
        except Exception as e:
            self.context.logger.exception(f"Exception in {self.name}: {e}")
            self._event = DerolasautomatorabciappEvents.ERROR

        self._is_done = True


class EndEpochRound(BaseState):
    """This class implements the behaviour of the state EndEpochRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.ENDEPOCHROUND

    def act(self) -> None:
        """Perfom the act."""

        try:
            w3_function = self.end_epoch()
            raw_tx = self.build_transaction(w3_function)
            self.simulate_tx(raw_tx)
            signed_tx = signed_tx_to_dict(self.crypto.entity.sign_transaction(raw_tx))
            tx_hash = try_send_signed_transaction(self.base_ledger_api, signed_tx)
            self.context.logger.debug(f"Transaction hash: {tx_hash}")
            tx_receipt = self.base_ledger_api.api.eth.wait_for_transaction_receipt(tx_hash, timeout=TX_MINING_TIMEOUT)
            if tx_receipt is None:
                self._event = DerolasautomatorabciappEvents.TX_TIMEOUT
            elif tx_receipt.status == 0:
                self._event = DerolasautomatorabciappEvents.TX_FAILED
            else:  # tx_receipt.status == 1
                self._event = DerolasautomatorabciappEvents.EPOCH_ENDED
            self.context.logger.debug(f"{self.name}: event {self._event}")
        except Exception as e:
            self.context.logger.info(f"Exception in {self.name}: {e}")
            self._event = DerolasautomatorabciappEvents.ERROR

        self._is_done = True

    def end_epoch(self):
        """Call "end_epoch" on Derolas contract."""

        return self.derolas_staking_contract.end_round(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )


class CheckReadyToDonateRound(BaseState):
    """This class implements the behaviour of the state CheckReadyToDonateRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.CHECKREADYTODONATEROUND

    def act(self) -> None:
        """Perfom the act."""

        try:
            gamestate: GameState = self.game_state
            if not gamestate.can_play_game or not self.pending_donations:
                self._event = DerolasautomatorabciappEvents.CANNOT_PLAY_GAME
            else:
                value_captured = self.pending_donations.popleft()
                msg = f"Value captured: {value_captured} USD, donating: {gamestate.minimum_donation / 1e18} ETH"
                self.context.logger.info(msg)
                self._event = DerolasautomatorabciappEvents.ELIGIBLE_TO_DONATE
        except Exception as e:
            self.context.logger.info(f"Exception in {self.name}: {e}")
            self._event = DerolasautomatorabciappEvents.ERROR

        self.context.logger.info(f"{self.name}: event {self._event}")
        self._is_done = True

    @property
    def max_donators_per_epoch(self) -> int:
        """Call "max_donators_per_epoch" on Derolas contract."""

        return self.derolas_staking_contract.max_donators_per_epoch(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )["int"]

    def epoch_to_total_donated(self, epoch: int) -> int:
        """Call "epoch_to_total_donated" on Derolas contract."""

        return self.derolas_staking_contract.epoch_to_total_donated(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
            var_0=epoch,
        )["int"]


class DonateRound(BaseState):
    """This class implements the behaviour of the state DonateRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.DONATEROUND

    def act(self) -> None:
        """Perfom the act."""

        try:
            state: GameState = self.game_state
            w3_function = self.donate()
            raw_tx = self.build_transaction(w3_function, value=state.minimum_donation)
            self.simulate_tx(raw_tx)
            signed_tx = signed_tx_to_dict(self.crypto.entity.sign_transaction(raw_tx))
            tx_hash = try_send_signed_transaction(self.base_ledger_api, signed_tx)
            self.context.logger.debug(f"Transaction hash: {tx_hash}")
            tx_receipt = self.base_ledger_api.api.eth.wait_for_transaction_receipt(tx_hash, timeout=TX_MINING_TIMEOUT)
            if tx_receipt is None:
                self._event = DerolasautomatorabciappEvents.TX_TIMEOUT
            elif tx_receipt.status == 0:
                self._event = DerolasautomatorabciappEvents.TX_FAILED
            else:
                self._event = DerolasautomatorabciappEvents.DONATED
        except Exception as e:
            self.context.logger.info(f"Exception in {self.name}: {e}")
            self._event = DerolasautomatorabciappEvents.ERROR

        self._is_done = True

    def donate(self):
        """Call "donate" on Derolas contract."""

        return self.derolas_staking_contract.donate(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )


class MakeClaimRound(BaseState):
    """This class implements the behaviour of the state MakeClaimRound."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = DerolasautomatorabciappStates.MAKECLAIMROUND

    def act(self) -> None:
        """Perfom the act."""

        try:
            w3_function = self.claim()
            raw_tx = self.build_transaction(w3_function)
            self.simulate_tx(raw_tx)
            signed_tx = signed_tx_to_dict(self.crypto.entity.sign_transaction(raw_tx))
            tx_hash = try_send_signed_transaction(self.base_ledger_api, signed_tx)
            self.context.logger.debug(f"Transaction hash: {tx_hash}")
            tx_receipt = self.base_ledger_api.api.eth.wait_for_transaction_receipt(tx_hash, timeout=TX_MINING_TIMEOUT)
            if tx_receipt is None:
                self._event = DerolasautomatorabciappEvents.TX_TIMEOUT
            elif tx_receipt.status == 0:
                self._event = DerolasautomatorabciappEvents.TX_FAILED
            else:
                self._event = DerolasautomatorabciappEvents.CLAIMED
        except Exception as e:
            self.context.logger.info(f"Exception in {self.name}: {e}")
            self._event = DerolasautomatorabciappEvents.ERROR

        self._is_done = True

    def claim(self):
        """Call "claim" on Derolas contract."""

        return self.derolas_staking_contract.claim(
            ledger_api=self.base_ledger_api,
            contract_address=self.derolas_contract_address,
        )


class DerolasautomatorabciappFsmBehaviour(FSMBehaviour, TickerBehaviour):
    """This class implements a simple Finite State Machine behaviour."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(tick_interval=30, **kwargs)
        self.register_state(
            DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            AwaitTriggerRound(**kwargs),
            True,
        )
        self.register_state(
            DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            CheckReadyToDonateRound(**kwargs),
        )
        self.register_state(DerolasautomatorabciappStates.MAKECLAIMROUND.value, MakeClaimRound(**kwargs))
        self.register_state(DerolasautomatorabciappStates.ENDEPOCHROUND.value, EndEpochRound(**kwargs))
        self.register_state(
            DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            CheckEpochRound(**kwargs),
        )
        self.register_state(DerolasautomatorabciappStates.DONATEROUND.value, DonateRound(**kwargs))

        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.CLAIMABLE,
            destination=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.CANNOT_PLAY_GAME,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.GAME_ON,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.NO_TRIGGER,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.CANNOT_PLAY_GAME,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_END_NEAR,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_FINISHED,
            destination=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_ONGOING,
            destination=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.ALREADY_DONATED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.CANNOT_PLAY_GAME,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.ELIGIBLE_TO_DONATE,
            destination=DerolasautomatorabciappStates.DONATEROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.CHECKREADYTODONATEROUND.value,
            event=DerolasautomatorabciappEvents.MAX_DONATORS_REACHED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.DONATED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.TX_FAILED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.DONATEROUND.value,
            event=DerolasautomatorabciappEvents.TX_TIMEOUT,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_ENDED,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.TX_FAILED,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.ENDEPOCHROUND.value,
            event=DerolasautomatorabciappEvents.TX_TIMEOUT,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.CLAIMED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.ERROR,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.TX_FAILED,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.MAKECLAIMROUND.value,
            event=DerolasautomatorabciappEvents.TX_TIMEOUT,
            destination=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
        )
        self.register_transition(
            source=DerolasautomatorabciappStates.AWAITTRIGGERROUND.value,
            event=DerolasautomatorabciappEvents.EPOCH_FINISHED,
            destination=DerolasautomatorabciappStates.CHECKEPOCHROUND.value,
        )

    def setup(self) -> None:
        """Implement the setup."""
        self.context.logger.info("Setting up Derolasautomatorabciapp FSM behaviour.")

    def teardown(self) -> None:
        """Implement the teardown."""
        self.context.logger.info("Tearing down Derolasautomatorabciapp FSM behaviour.")

    def act(self) -> None:
        """Implement the act."""
        if self.current is None:
            self.context.logger.info("No state to act on.")
            self.terminate()
        self.context.logger.debug(f"Entering {self.current}")
        super().act()

    def terminate(self) -> None:
        """Implement the termination."""
        self.teardown()
        os._exit(0)
