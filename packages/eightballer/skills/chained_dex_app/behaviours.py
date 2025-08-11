# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
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

"""This module contains the behaviours for the 'abci' skill."""

from packages.eightballer.skills.chained_dex_app.composition import ChaineddexAbciApp
from packages.eightballer.skills.reset_pause_abci.behaviours import ResetPauseABCIConsensusBehaviour
from packages.eightballer.skills.registration_abci.behaviours import (
    RegistrationStartupBehaviour,
    AgentRegistrationRoundBehaviour,
)
from packages.eightballer.skills.dex_data_retrieval.behaviours import DexDataRetrievalRoundBehaviour
from packages.eightballer.skills.abstract_round_abci.behaviours import BaseBehaviour, AbstractRoundBehaviour


class DexDataAbciAppConsensusBehaviour(AbstractRoundBehaviour):
    """This behaviour manages the consensus stages for the price estimation."""

    initial_behaviour_cls = RegistrationStartupBehaviour
    abci_app_cls = ChaineddexAbciApp  # type: ignore
    behaviours: set[type[BaseBehaviour]] = {
        *AgentRegistrationRoundBehaviour.behaviours,
        *DexDataRetrievalRoundBehaviour.behaviours,
        *ResetPauseABCIConsensusBehaviour.behaviours,
    }
