# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
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

"""This package contains a scaffold of a model."""

import json
import pathlib
import datetime
from copy import deepcopy
from typing import TYPE_CHECKING, Any, cast
from collections import deque
from dataclasses import field, asdict, dataclass

from aea.skills.base import Model
from aea.configurations.base import PublicId

from packages.eightballer.protocols.orders.custom_types import Order
from packages.eightballer.skills.abstract_round_abci.models import FrozenMixin
from packages.eightballer.protocols.user_interaction.message import (
    UserInteractionMessage,
)
from packages.eightballer.protocols.user_interaction.dialogues import (
    UserInteractionDialogues,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeRequest
from packages.eightballer.connections.apprise_wrapper.connection import (
    CONNECTION_ID as APPRISE_PUBLIC_ID,
)


TZ = datetime.datetime.now().astimezone().tzinfo


CEX_LEDGER_ID = "cex"

if TYPE_CHECKING:
    from collections.abc import Callable


DEFAULT_COOL_DOWN_PERIOD = 10
DEFAULT_MAX_OPEN_ORDERS = 1


PORTFOLIO_FILE = "portfolio.json"
EXISTING_ORDERS_FILE = "existing_orders.json"
FAILED_ORDERS_FILE = "failed_orders.json"
ORDERS_FILE = "orders.json"
PRICES_FILE = "prices.json"

UNHEALTHY_TRANSITION_THRESHOLD = 600  # 10 minutes


@dataclass
class ArbitrageOpportunity:
    """An arbitrage opportunity."""

    market: str
    delta: float
    percent: float
    best_bid: float
    best_ask: float
    best_bid_exchange: str
    best_ask_exchange: str
    best_bid_ledger: str
    best_ask_ledger: str
    required_asset_a: float = None
    required_asset_b: float = None
    balance_a: float = None
    balance_b: float = None


@dataclass
class AgentState:
    """The agent state."""

    portfolio: dict[str : dict[str, list[dict]]]
    prices: dict[str : dict[str, float]]
    existing_orders: dict[str : dict[str, list[dict]]]
    new_orders: list[Order]
    failed_orders: list[Order]
    submitted_orders: list[Order]
    unaffordable_opportunity: list[ArbitrageOpportunity]
    current_round: str = None
    current_period: int = 0
    last_transition_time: datetime.datetime = None
    bridge_requests: list[BridgeRequest] = field(default_factory=list)
    pending_donations: deque[float] = field(default_factory=deque)

    def write_to_file(self):
        """Write the state to files."""
        pathlib.Path(PORTFOLIO_FILE).write_text(json.dumps(self.portfolio, indent=4), encoding="utf-8")
        pathlib.Path(PRICES_FILE).write_text(json.dumps(self.prices, indent=4), encoding="utf-8")
        pathlib.Path(EXISTING_ORDERS_FILE).write_text(json.dumps(self.existing_orders, indent=4), encoding="utf-8")

    def to_json(self) -> dict:
        """Convert the state to JSON."""

        return json.dumps(
            {
                "portfolio": self.portfolio,
                "prices": self.prices,
                "new_orders": [json.loads(order.model_dump_json()) for order in self.new_orders],
                "open_orders": [json.loads(order.model_dump_json()) for order in self.all_order_list],
                "failed_orders": [json.loads(order.model_dump_json()) for order in self.failed_orders],
                "submitted_orders": [json.loads(order.model_dump_json()) for order in self.submitted_orders],
                "unaffordable_opportunity": [asdict(op) for op in self.unaffordable_opportunity],
                "total_open_orders": len(self.all_order_list),
                "time_since_last_update": datetime.datetime.now(tz=TZ).isoformat(),
                "current_state": self.current_round,
                "current_period": self.current_period,
                "is_healthy": self.is_healthy,
            }
        )

    @property
    def is_healthy(self) -> bool:
        """Check if the agent is healthy."""

        if self.last_transition_time is None:
            return False

        current_time = datetime.datetime.now(tz=TZ)
        time_since_last_transition = (current_time - self.last_transition_time).total_seconds()

        return all(
            [
                self.current_round is not None,
                self.current_period > 0,
                self.portfolio,
                self.prices,
                time_since_last_transition < UNHEALTHY_TRANSITION_THRESHOLD,
            ]
        )

    @property
    def all_order_list(self) -> list[Order]:
        """Get all orders."""
        all_order_list: list[Order] = []
        for exchanges in self.existing_orders.values():
            for orders in exchanges.values():
                all_order_list += orders
        return all_order_list


class ArbitrageStrategy(Model):
    """This class scaffolds a model."""

    dexs: list = []
    cexs: list = []
    ledgers: list = []
    order_size: float = 0.0
    fetch_all_tickers = False
    cool_down_period = 0
    state: AgentState = None
    error_count = 0

    entry_order: Order = None
    exit_order: Order = None
    donate: bool = True

    def __init__(self, **kwargs):
        """Initialize the model."""
        self.cexs = kwargs.pop("cexs", [])
        self.dexs = kwargs.pop("dexs", [])
        self.ledgers = kwargs.pop("ledgers", [])
        self.strategy_init_kwargs = kwargs.pop("strategy_init_kwargs", {})
        self.strategy_public_id = PublicId.from_str(kwargs.pop("strategy_public_id"))
        self.fetch_all_tickers = kwargs.pop("fetch_all_tickers", False)
        self.cooldown_period = kwargs.pop("cooldown_period", DEFAULT_COOL_DOWN_PERIOD)
        self.state = self.build_initial_state()
        super().__init__(**kwargs)
        self.context.shared_state["state"] = self.state
        self.context.logger.info(
            "ArbitrageStrategy initialized. with cooldown period: %s",
            self.cooldown_period,
        )
        self.context.logger.info(
            "ArbitrageStrategy initialized. with strategy public id: %s",
            self.strategy_public_id,
        )
        self.context.logger.info(
            "ArbitrageStrategy initialized. with strategy init kwargs: %s",
            self.strategy_init_kwargs,
        )

    def build_initial_state(self) -> dict:
        """Build the portfolio."""
        data = {CEX_LEDGER_ID: {cex: {} for cex in self.cexs}}
        for exchange_id, ledgers in self.dexs.items():
            for ledger_id in ledgers:
                if ledger_id not in data:
                    data[ledger_id] = {}
                if exchange_id not in data[ledger_id]:
                    data[ledger_id][exchange_id] = []

        return AgentState(
            portfolio=deepcopy(data),
            prices=deepcopy(data),
            existing_orders=deepcopy(data),
            new_orders=[],
            failed_orders=[],
            submitted_orders=[],
            unaffordable_opportunity=[],
        )

    def send_notification_to_user(self, title: str, msg: str, attach: str | None = None) -> None:
        """Send notification to user."""
        dialogues = cast(UserInteractionDialogues, self.context.user_interaction_dialogues)
        msg, _ = dialogues.create(
            counterparty=str(APPRISE_PUBLIC_ID),
            performative=UserInteractionMessage.Performative.NOTIFICATION,
            title=title,
            body=msg,
            attach=attach,
        )
        self.context.outbox.put_message(message=msg)


class Requests(Model, FrozenMixin):
    """Keep the current pending requests."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the state."""
        # mapping from dialogue reference nonce to a callback
        self.request_id_to_callback: dict[str, Callable] = {}
        super().__init__(*args, **kwargs)
        self._frozen = True
