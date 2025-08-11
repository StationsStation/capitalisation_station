"""Contains cases for the reporting tests."""

from packages.eightballer.protocols.markets.custom_types import Market
from packages.eightballer.protocols.positions.custom_types import Position, PositionSide


EXCHANGE_1 = "deribit"
EXCHANGE_2 = "binance"

TEST_MARKET_NAME_1 = "ETH/USD:ETH-29AUG23-1800-C"
TEST_MARKET_NAME_2 = "ETH/USD:ETH-29AUG23-1900-P"

POSITION_CASE_1 = Position(
    id="test_id",
    exchange_id=EXCHANGE_1,
    symbol=TEST_MARKET_NAME_1,
    side=PositionSide.LONG,
    entry_price=100,
    size=1,
    timestamp=1629780000,
    datetime="2021-08-24T00:00:00+00:00",
    last_update_timestamp=1629780000,
    initial_margin=0.1,
    initial_margin_percentage=0.1,
)

POSITION_CASE_2 = Position(
    id="test_id",
    exchange_id=EXCHANGE_1,
    symbol=TEST_MARKET_NAME_2,
    side=PositionSide.LONG,
    entry_price=100,
    size=1,
)

TEST_MARKET_DATA = Market(
    id="test_id",
    exchange_id=EXCHANGE_1,
    symbol=TEST_MARKET_NAME_1,
    strike=2000,
    expiry_datetime="2021-08-23T18:00:00+00:00",
    option_type="call",
)
