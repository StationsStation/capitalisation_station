"""Simple tests for the arbitrage strategy."""

import json
from pathlib import Path

import pytest

from packages.eightballer.protocols.orders.custom_types import Order
from packages.eightballer.customs.lbtc_arbitrage.strategy import (
    ArbitrageStrategy,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeRequest


TEST_INIT_KWARGS = {
    "base_asset": "LBTC",
    "quote_asset": "USDC",
    "min_profit": 0.00,
    "order_size": 0.01,
    "max_open_orders": 1,
}


def read_test_json(file_path):
    """Read a JSON file and return its contents."""
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def get_cases() -> list:
    """Check how many folders are in the data directory."""
    return [x.stem for x in (Path(__file__).parent / "data").iterdir() if x.is_dir()]


def test_strategy_init():
    """Test the strategy init."""
    strategy = ArbitrageStrategy(**TEST_INIT_KWARGS)
    assert strategy is not None


class TestEnhancedArbitrageStrategy:
    """Test suite for the EnhancedArbitrageStrategy class."""

    def _setup_method(self, method, case):
        """Set up test fixtures."""
        # Sample portfolio data
        self.method = method
        portfolio_path = Path(__file__).parent / "data" / case / "portfolio.json"
        self.portfolio = read_test_json(portfolio_path)
        self.prices = read_test_json(Path(__file__).parent / "data" / case / "prices.json")
        self.orders = {}
        self.strategy = ArbitrageStrategy(**TEST_INIT_KWARGS)

    @pytest.mark.parametrize("case", get_cases())
    def test_strategy_init(self, case):
        """Test the strategy init."""
        self._setup_method("test_strategy_init", case)
        assert self.strategy is not None

    @pytest.mark.parametrize("case", get_cases())
    def test_get_orders(self, case):
        """Test the get_orders method."""
        self._setup_method("test_get_orders", case)
        orders = self.strategy.get_orders(self.portfolio, self.prices, self.orders)
        assert orders is not None
        assert len(orders) > 0
        assert all(isinstance(order, Order) for order in orders)

    @pytest.mark.parametrize("case", get_cases())
    def test_get_bridge_requests(self, case):
        """Test the get_bridge_requests method."""
        self._setup_method("test_get_bridge_requests", case)
        requests = self.strategy.get_bridge_requests(
            self.portfolio,
        )
        assert requests is not None
        assert all(isinstance(request, BridgeRequest) for request in requests)
