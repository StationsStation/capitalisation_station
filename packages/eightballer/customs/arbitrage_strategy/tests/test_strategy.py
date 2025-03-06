"""Simple tests for the arbitrage strategy."""

from packages.eightballer.customs.arbitrage_strategy.strategy import ArbitrageStrategy


def test_strategy_init():
    """Test the strategy init."""
    strategy = ArbitrageStrategy()
    assert strategy is not None
