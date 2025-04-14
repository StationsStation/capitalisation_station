"""Base exchange class."""

from enum import Enum


class SupportedExchanges(Enum):
    """Supported exchanges."""

    BALANCER = "balancer"
    DERIVE = "derive"
    COWSWAP = "cowswap"
