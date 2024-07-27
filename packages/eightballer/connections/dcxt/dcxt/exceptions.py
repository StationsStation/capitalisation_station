"""
Custom exceptions for the DCXT package.
"""


class Reversion(Exception):
    """Reversion exception."""


class BalanceException(Exception):
    """Raised when the balance is too low to perform the swap."""


class SwapConfigurationError(Exception):
    """Raised when there is an error with the swap configuration."""


class SwapException(Exception):
    """Raised when there is an error with the swap."""


class SorRetrievalException(Exception):
    """Raised when there is an error retrieving the SOR."""


class ConfigurationError(Exception):
    """Raised when there is an error with the configuration."""
