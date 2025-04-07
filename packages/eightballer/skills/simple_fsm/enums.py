"""Enums for the FSMs."""

from enum import Enum


class ArbitrageabciappEvents(Enum):
    """This class defines the events for the Arbitrageabciapp FSM."""

    DONE = "DONE"
    TIMEOUT = "TIMEOUT"
    OPPORTUNITY_FOUND = "OPPORTUNITY_FOUND"
    ENTRY_EXIT_ERROR = "ENTRY_EXIT_ERROR"
