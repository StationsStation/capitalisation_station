"""Custom exchange modules."""

import ccxt.async_support as ccxt  # pylint: disable=E0401,E0611


class CustomBroker(ccxt.binance):
    """Custom override allowing overrides."""
