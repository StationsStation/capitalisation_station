"""Simple tests for the arbitrage strategy."""

import json
import unittest
from pathlib import Path

import pytest

from packages.eightballer.protocols.orders.custom_types import Order
from packages.eightballer.customs.lbtc_arbitrage.strategy import (
    ArbitrageStrategy,
)


TEST_INIT_KWARGS = {
    "base_asset": "LBTC",
    "quote_asset": "USDC",
    "min_profit": 0.00,
    "order_size": 0.01,
}


def read_test_json(file_path):
    """Read a JSON file and return its contents."""
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)

def get_cases()->list:
    """
    check how many folders are in the data directory.
    """
    res = [x.stem for x in (Path(__file__).parent / "data").iterdir() if x.is_dir()]
    return res

def test_strategy_init():
    """Test the strategy init."""
    strategy = ArbitrageStrategy(**TEST_INIT_KWARGS)
    assert strategy is not None


class TestEnhancedArbitrageStrategy():
    """Test suite for the EnhancedArbitrageStrategy class."""

    def _setup_method(self, method, case):
        """Set up test fixtures."""
        # Sample portfolio data
        self.method = method
        portfolio_path = Path(__file__).parent / "data" / case / "portfolio.json"
        self.portfolio = read_test_json(portfolio_path)
        self.prices = read_test_json(Path(__file__).parent / "data" / case / "prices.json")
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
        orders = self.strategy.get_orders(self.portfolio, self.prices)
        assert orders is not None
        assert len(orders) > 0
        assert all(isinstance(order, Order) for order in orders)
