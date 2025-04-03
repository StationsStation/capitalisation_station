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

from typing import TYPE_CHECKING, Any

from aea.skills.base import Model
from aea.configurations.base import PublicId

from packages.eightballer.protocols.orders.custom_types import Orders
from packages.eightballer.skills.abstract_round_abci.models import FrozenMixin


if TYPE_CHECKING:
    from collections.abc import Callable


DEFAULT_COOL_DOWN_PERIOD = 15
DEFAULT_MAX_OPEN_ORDERS = 1


class ArbitrageStrategy(Model):
    """This class scaffolds a model."""

    dexs: list = []
    cexs: list = []
    ledgers: list = []
    order_size: float = 0.0
    fetch_all_tickers = False
    cool_down_period = 0
    outstanding_orders: Orders = Orders(orders=[])

    def __init__(self, **kwargs):
        """Initialize the model."""
        self.cexs = kwargs.pop("cexs", [])
        self.dexs = kwargs.pop("dexs", [])
        self.ledgers = kwargs.pop("ledgers", [])
        self.strategy_init_kwargs = kwargs.pop("strategy_init_kwargs", {})
        self.strategy_public_id = PublicId.from_str(kwargs.pop("strategy_public_id"))
        self.fetch_all_tickers = kwargs.pop("fetch_all_tickers", False)
        self.cool_down_period = kwargs.pop("cool_down_period", DEFAULT_COOL_DOWN_PERIOD)
        super().__init__(**kwargs)


class Requests(Model, FrozenMixin):
    """Keep the current pending requests."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the state."""
        # mapping from dialogue reference nonce to a callback
        self.request_id_to_callback: dict[str, Callable] = {}
        super().__init__(*args, **kwargs)
        self._frozen = True
