"""Collect data round behaviour class."""

import json
from time import sleep
from collections.abc import Generator

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.skills.simple_fsm.strategy import CEX_LEDGER_ID, ArbitrageStrategy
from packages.eightballer.protocols.tickers.custom_types import Tickers
from packages.eightballer.connections.ccxt_wrapper.connection import PUBLIC_ID as CCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseConnectionRound


DATA_COLLECTION_TIMEOUT_SECONDS = 1
DEFAULT_ENCODING = "utf-8"


class CollectDataRound(BaseConnectionRound):
    """This class implements the CollectDataRound state."""

    matching_round = "collectdataround"
    attempts = 0
    started = False

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy

    async def get_futures(self, exchange_id: str, ledger_id: str, is_cex=True) -> Generator:
        """Get the futures for the given exchange and ledger id."""
        connection_id = str(CCXT_PUBLIC_ID) if is_cex else str(DCXT_PUBLIC_ID)
        balances_future = self.get_response(
            BalancesMessage.Performative.GET_ALL_BALANCES,
            connection_id=connection_id,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
            timeout=DATA_COLLECTION_TIMEOUT_SECONDS,
        )

        tickers_future = self.get_response(
            TickersMessage.Performative.GET_ALL_TICKERS,
            connection_id=connection_id,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
            timeout=DATA_COLLECTION_TIMEOUT_SECONDS,
        )
        order_future = self.get_response(
            OrdersMessage.Performative.GET_ORDERS,
            connection_id=connection_id,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
            symbol="OLAS/USDT",
            timeout=DATA_COLLECTION_TIMEOUT_SECONDS,
        )
        return balances_future, tickers_future, order_future

    def parse_futures(self, futures: list) -> Generator:
        """We efficiently parse the futures."""
        while not all(f.done() for f in futures):
            yield
        yield [f.result() for f in futures]

    def act(self) -> Generator:
        """Perform the action of the state."""
        if self.started:
            return

        self.started = True
        for exchange_id in self.context.arbitrage_strategy.cexs:
            self.context.logger.debug(f"Getting balances for {exchange_id} on {CEX_LEDGER_ID}")
            futures = yield from self.get_futures(exchange_id, CEX_LEDGER_ID)
            balances, tickers, orders = yield from self.parse_futures(futures)
            if any(f is None for f in (balances, tickers, orders)):
                self.context.logger.error(f"Error getting data for {exchange_id} on {CEX_LEDGER_ID}")
                return self._handle_error()

            if any(
                [
                    balances.performative == BalancesMessage.Performative.ERROR,
                    tickers.performative == TickersMessage.Performative.ERROR,
                    orders.performative == OrdersMessage.Performative.ERROR,
                ]
            ):
                self.context.logger.error(f"Error getting data for {exchange_id} on {CEX_LEDGER_ID}")
                return self._handle_error()
            self.strategy.agent_state.portfolio[CEX_LEDGER_ID][exchange_id] = [
                b.dict() for b in balances.balances.balances
            ]
            self.strategy.agent_state.prices[CEX_LEDGER_ID][exchange_id] = [t.dict() for t in tickers.tickers.tickers]
            self.strategy.agent_state.existing_orders[CEX_LEDGER_ID][exchange_id] = [
                o.dict() for o in orders.orders.orders
            ]

        for exchange_id, ledger_ids in self.strategy.dexs.items():
            for ledger_id in ledger_ids:
                self.context.logger.debug(f"Getting balances for {exchange_id} on {ledger_id}")

                balances = yield from self.get_response(
                    BalancesMessage.Performative.GET_ALL_BALANCES,
                    connection_id=str(DCXT_PUBLIC_ID),
                    exchange_id=exchange_id,
                    ledger_id=ledger_id,
                )
                if balances is None or balances.performative == BalancesMessage.Performative.ERROR:
                    self.context.logger.error(f"Error getting balances for {exchange_id} on {ledger_id}")
                    return self._handle_error()

                tickers = yield from self.get_tickers(
                    exchange_id=exchange_id,
                    ledger_id=ledger_id,
                )
                if not tickers:
                    self.context.logger.error(f"Error getting tickers for {exchange_id} on {ledger_id}")
                    return self._handle_error()

                self.strategy.state.portfolio[ledger_id][exchange_id] = [b.dict() for b in balances.balances.balances]
                self.strategy.state.prices[ledger_id][exchange_id] = [t.dict() for t in tickers.tickers]
                self.context.logger.debug(f"Got balances + tickers for {exchange_id} on {ledger_id}")

        self.context.logger.debug("Data collection complete.")
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.attempts = 0

    def _handle_error(
        self,
    ) -> None:
        """In the case that data is not retrieved, handled the necessary error."""
        self.started = False
        self.attempts += 1
        sleep(DATA_COLLECTION_TIMEOUT_SECONDS * self.attempts)

    def get_tickers(
        self,
        exchange_id: str,
        ledger_id: str,
    ) -> Generator:
        """Get the tickers from a specific exchange."""
        performative = (
            TickersMessage.Performative.GET_ALL_TICKERS
            if self.context.arbitrage_strategy.fetch_all_tickers
            else TickersMessage.Performative.GET_TICKER
        )

        if performative == TickersMessage.Performative.GET_TICKER:
            # we want to get the wrapped base token
            asset_a = self.strategy.trading_strategy.quote_asset
            asset_b = self.strategy.trading_strategy.base_asset
            params = []

            def encode_dict(d: dict) -> bytes:
                """Encode a dictionary."""
                return json.dumps(d).encode(DEFAULT_ENCODING)

            params.append(
                {
                    "asset_a": asset_a,
                    "asset_b": asset_b,
                    "params": encode_dict({"amount": self.context.arbitrage_strategy.trading_strategy.order_size}),
                }
            )
            tickers = Tickers(tickers=[])
            for param in params:
                ticker = yield from self.get_response(
                    performative,
                    connection_id=str(DCXT_PUBLIC_ID),
                    exchange_id=exchange_id,
                    ledger_id=ledger_id,
                    **param,
                )

                if (
                    ticker is None
                    or not isinstance(ticker, TickersMessage)
                    or ticker.performative == TickersMessage.Performative.ERROR
                ):
                    self.context.logger.error(f"Error getting ticker for {exchange_id} on {ledger_id}")
                    self.started = False
                    sleep(DATA_COLLECTION_TIMEOUT_SECONDS)
                    return
                tickers.tickers.append(ticker.ticker)

        else:
            tickers = yield from self.get_response(
                performative,
                connection_id=str(DCXT_PUBLIC_ID),
                exchange_id=exchange_id,
                ledger_id=ledger_id,
            )
            if (
                ticker is None
                or not isinstance(ticker, TickersMessage)
                or tickers.performative == TickersMessage.Performative.ERROR
            ):
                self.context.logger.error(f"Error getting tickers for {exchange_id} on {ledger_id}")
                self.started = False
                sleep(DATA_COLLECTION_TIMEOUT_SECONDS)
                return
        return tickers

    def setup(self) -> None:
        """Setup the state."""
        self.started = False
        self._is_done = False
        self._event = ArbitrageabciappEvents.TIMEOUT
        self.attempts = 0
        super().setup()
