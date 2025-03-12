"""Simple tests for the arbitrage strategy."""

import json
import unittest
from pathlib import Path

from packages.eightballer.protocols.orders.custom_types import Order
from packages.eightballer.customs.arbitrage_strategy.strategy import (
    ArbitrageStrategy,
    ArbitrageStrategy as EnhancedArbitrageStrategy,
)


def read_test_json(file_path):
    """Read a JSON file and return its contents."""
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def test_strategy_init():
    """Test the strategy init."""
    strategy = ArbitrageStrategy()
    assert strategy is not None


class TestEnhancedArbitrageStrategy(unittest.TestCase):
    """Test suite for the EnhancedArbitrageStrategy class."""

    def setup_method(self, method):
        """Set up test fixtures."""
        # Sample portfolio data
        self.method = method
        portfolio_path = Path(__file__).parent / "data" / "case_0" / "portfolio.json"
        self.portfolio = read_test_json(portfolio_path)
        self.prices = read_test_json(Path(__file__).parent / "data" / "case_0" / "prices.json")

        self.strategy = EnhancedArbitrageStrategy()

    def test_strategy_init(self):
        """Test the strategy init."""
        assert self.strategy is not None

    def test_get_orders(self):
        """Test the get_orders method."""
        orders = self.strategy.get_orders(self.portfolio, self.prices)
        assert orders is not None
        assert len(orders) > 0
        assert all(isinstance(order, Order) for order in orders)
