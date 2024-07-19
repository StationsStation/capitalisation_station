# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""This module contains the shared state for the abci skill of AbciApp."""

from dataclasses import dataclass
from typing import Any, Dict, List, Union

from packages.eightballer.skills.dex_data_retrieval.rounds import (
    DexDataRetrievalAbciApp,
)
from packages.valory.skills.abstract_round_abci.models import BaseParams
from packages.valory.skills.abstract_round_abci.models import (
    BenchmarkTool as BaseBenchmarkTool,
)
from packages.valory.skills.abstract_round_abci.models import Requests as BaseRequests
from packages.valory.skills.abstract_round_abci.models import (
    SharedState as BaseSharedState,
)


@dataclass
class DexDataRetrievalConfig:
    """Config for the DexDataRetrieval skill."""

    enabled: bool
    exchange_ids: List[str]
    extra_kwargs: Dict[str, Dict[str, Union[str, int, float, bool]]]
    retries: int
    backoff: float
    reporting_enabled: bool


class SharedState(BaseSharedState):
    """Keep the current shared state of the skill."""

    abci_app_cls = DexDataRetrievalAbciApp


class Params(BaseParams):
    """Parameters."""

    dex_data_retrieval_config: Dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the parameters object."""
        config = self._ensure("dex_data_retrieval_config", kwargs, dict)
        self.dex_data_retrieval_config = DexDataRetrievalConfig(**config)
        super().__init__(*args, **kwargs)


Requests = BaseRequests
BenchmarkTool = BaseBenchmarkTool
