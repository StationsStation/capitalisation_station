"""Musi."""

from packages.eightballer.skills.reset_pause_abci.rounds import (
    ResetPauseAbciApp,
    ResetAndPauseRound,
    FinishedResetAndPauseRound,
    FinishedResetAndPauseErrorRound,
)
from packages.eightballer.skills.registration_abci.rounds import (
    AgentRegistrationAbciApp,
    RegistrationStartupRound,
    FinishedRegistrationRound,
)
from packages.eightballer.skills.dex_data_retrieval.rounds import (
    FailedDexRound,
    FetchDexMarketsRound,
    RetrievedDexDataRound,
    DexDataRetrievalAbciApp,
)
from packages.eightballer.skills.abstract_round_abci.abci_app_chain import AbciAppTransitionMapping, chain


abci_app_transition_mapping: AbciAppTransitionMapping = {
    FinishedRegistrationRound: FetchDexMarketsRound,
    RetrievedDexDataRound: ResetAndPauseRound,
    FailedDexRound: ResetAndPauseRound,
    FinishedResetAndPauseRound: FetchDexMarketsRound,
    FinishedResetAndPauseErrorRound: RegistrationStartupRound,
}


ChaineddexAbciApp = chain(
    (
        AgentRegistrationAbciApp,
        DexDataRetrievalAbciApp,
        ResetPauseAbciApp,
    ),
    abci_app_transition_mapping,
)
