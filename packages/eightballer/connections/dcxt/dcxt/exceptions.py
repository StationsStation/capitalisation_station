"""Custom exceptions for the DCXT package."""


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


class RequestTimeout(Exception):
    """Raised when there is a request timeout."""


class ExchangeError(Exception):
    """Raised when there is an error with the exchange."""


class AuthenticationError(Exception):
    """Raised when there is an authentication error."""


class InsufficientFunds(Exception):
    """Raised when there are insufficient funds to perform the operation."""


class BadSymbol(Exception):
    """Raised when the symbol is not recognised by the exchange."""


class ExchangeNotAvailable(Exception):
    """Raised when the exchange is not available."""


class InvalidOrder(Exception):
    """Raised when the order is invalid."""


class OrderNotFound(Exception):
    """Raised when the order is not found."""


class ApprovalError(Exception):
    """Raised when there is an error with the approvals."""


class RpcError(Exception):
    """Exception raised when an RPC error occurs."""


class UnsupportedAsset(Exception):
    """Raised when the asset is not supported by the exchange."""
