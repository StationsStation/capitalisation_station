"""Class for interacting with the 1inch API."""

from typing import Any

from packages.eightballer.connections.dcxt.dcxt.defi_exchange import BaseErc20Exchange


class OneInchApiClient(BaseErc20Exchange):
    """Class for interacting with the 1inch API."""

    async def fetch_open_orders(self, address: str) -> dict[str, Any]:
        """Fetch the open orders for the given address."""

    async def create_order(self, order: dict[str, Any]) -> dict[str, Any]:
        """Create an order."""

    async def fetch_tickers(self, *args, **kwargs) -> dict[str, Any]:
        """Fetch the tickers."""

    async def fetch_positions(self, *arg, **kwargs) -> dict[str, Any]:
        """Fetch the positions for the given address."""
