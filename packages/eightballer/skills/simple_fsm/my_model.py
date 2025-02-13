# -*- coding: utf-8 -*-
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

from typing import Any, Dict, Callable

from aea.skills.base import Model

from packages.valory.skills.abstract_round_abci.models import FrozenMixin

class Requests(Model, FrozenMixin):
    """Keep the current pending requests."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the state."""
        # mapping from dialogue reference nonce to a callback
        self.request_id_to_callback: Dict[str, Callable] = {}
        super().__init__(*args, **kwargs)
        self._frozen = True


class ArbitrageStrategy(Model):
    """This class scaffolds a model."""

    dexs: list = []
    cexs: list = []
    ledgers: list = []
    order_size: float = 0.0

    def __init__(self, **kwargs):
        """Initialize the model."""
        self.cexs = kwargs.pop("cexs", [])
        self.dexs = kwargs.pop("dexs", [])
        self.ledgers = kwargs.pop("ledgers", [])
        self.order_size = kwargs.pop("order_size", 0)
        super().__init__(**kwargs)

