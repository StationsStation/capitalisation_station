"""
Musi
"""
from packages.eightballer.skills.dex_data_retrieval.rounds import (
    DexDataRetrievalAbciApp,
    FailedDexRound,
    FetchDexMarketsRound,
    RetrievedDexDataRound,
)
from packages.valory.skills.abstract_round_abci.abci_app_chain import AbciAppTransitionMapping, chain
from packages.valory.skills.registration_abci.rounds import (
    AgentRegistrationAbciApp,
    FinishedRegistrationRound,
    RegistrationStartupRound,
)
from packages.valory.skills.reset_pause_abci.rounds import (
    FinishedResetAndPauseErrorRound,
    FinishedResetAndPauseRound,
    ResetAndPauseRound,
    ResetPauseAbciApp,
)

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
