"""Collect data round behaviour class."""

import json
from datetime import datetime, timedelta
from collections.abc import Generator

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.skills.simple_fsm.strategy import TZ, CEX_LEDGER_ID, ArbitrageStrategy
from packages.eightballer.protocols.tickers.custom_types import Tickers
from packages.eightballer.connections.ccxt_wrapper.connection import PUBLIC_ID as CCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseConnectionRound


DATA_COLLECTION_TIMEOUT_SECONDS = 10
DEFAULT_ENCODING = "utf-8"


class CollectDataRound(BaseConnectionRound):
    """This class implements the CollectDataRound state."""

    matching_round = "collectdataround"
    attempts = 0
    started = False

    supported_protocols = {
        OrdersMessage.protocol_id: [],
        TickersMessage.protocol_id: [],
        BalancesMessage.protocol_id: [],
    }

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

    def handle_cexs(self):
        """Handle the CEXs."""
        for exchange_id in self.context.arbitrage_strategy.cexs:
            self.context.logger.debug(f"Getting balances for {exchange_id} on {CEX_LEDGER_ID}")
            futures = yield from self.get_futures(exchange_id, CEX_LEDGER_ID)
            balances, tickers, orders = yield from self.parse_futures(futures)
            if any(f is None for f in (balances, tickers, orders)):
                self.context.logger.error(f"Error getting data for {exchange_id} on {CEX_LEDGER_ID}")
                yield from self._handle_error()
                return

            if any(
                [
                    balances.performative == BalancesMessage.Performative.ERROR,
                    tickers.performative == TickersMessage.Performative.ERROR,
                    orders.performative == OrdersMessage.Performative.ERROR,
                ]
            ):
                self.context.logger.error(f"Error getting data for {exchange_id} on {CEX_LEDGER_ID}")
                yield from self._handle_error()
                return
            self.strategy.agent_state.portfolio[CEX_LEDGER_ID][exchange_id] = [
                b.dict() for b in balances.balances.balances
            ]
            self.strategy.agent_state.prices[CEX_LEDGER_ID][exchange_id] = [t.dict() for t in tickers.tickers.tickers]
            self.strategy.agent_state.existing_orders[CEX_LEDGER_ID][exchange_id] = [
                o.dict() for o in orders.orders.orders
            ]

    def act(self) -> Generator:
        """Perform the action of the state."""

        if not self.started:
            self.started = True
            self.started_at = datetime.now(tz=TZ)
            self.context.logger.debug(f"Starting data collection. at {self.started_at!s}")
            self.pending_bals = []
            self.pending_tickers = []
            self.pending_orders = []
            for k in self.supported_protocols:
                self.supported_protocols[k] = []
            for exchange_id, ledger_ids in self.strategy.dexs.items():
                for ledger_id in ledger_ids:
                    self.context.logger.debug(f"Getting balances for {exchange_id} on {ledger_id}")
                    balances = self.submit_msg(
                        BalancesMessage.Performative.GET_ALL_BALANCES,
                        connection_id=str(DCXT_PUBLIC_ID),
                        exchange_id=exchange_id,
                        ledger_id=ledger_id,
                        timeout=DATA_COLLECTION_TIMEOUT_SECONDS,
                    )
                    balances.validation_func = self._validate_balance_msg
                    balances.exchange_id = exchange_id
                    balances.ledger_id = ledger_id
                    self.pending_bals.append(balances)

                    orders = self.submit_msg(
                        OrdersMessage.Performative.GET_ORDERS,
                        connection_id=str(DCXT_PUBLIC_ID),
                        exchange_id=exchange_id,
                        ledger_id=ledger_id,
                    )
                    orders.validation_func = self._validate_orders_msg
                    orders.exchange_id = exchange_id
                    orders.ledger_id = ledger_id
                    self.pending_orders.append(orders)
            return
        if any(
            [
                len(self.pending_bals) != len(self.supported_protocols.get(BalancesMessage.protocol_id)),
                len(self.pending_orders) != len(self.supported_protocols.get(OrdersMessage.protocol_id)),
            ]
        ):
            self.context.logger.debug(
                f"Waiting for all messages to be received. {self.pending_bals} {self.pending_orders}"
            )
            if not datetime.now(tz=TZ) - timedelta(seconds=DATA_COLLECTION_TIMEOUT_SECONDS) < self.started_at:
                self.context.logger.error("Timeout waiting for messages.")
                self._event = ArbitrageabciappEvents.TIMEOUT
                self._is_done = True
                self.context.logger.error("Error getting data for all exchanges")
                self.started = False
                return
            return

        # we validate all the responses
        are_all_valid = all(f.validation_func(f.last_message) for f in self.pending_bals + self.pending_orders)

        if not are_all_valid:
            self.context.logger.error("Error getting data for all exchanges")
            self._handle_error()
            return

        for order in self.pending_orders:
            self.strategy.state.existing_orders[order.ledger_id][order.exchange_id] = list(
                order.last_message.orders.orders
            )

        for bal in self.pending_bals:
            self.strategy.state.portfolio[bal.ledger_id][bal.exchange_id] = [
                b.dict() for b in bal.last_message.balances.balances
            ]

        self.context.logger.debug("Data collection complete.")
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.attempts = 0

    def _validate_orders_msg(self, orders: OrdersMessage) -> bool:
        """Validate the orders message."""
        if orders is None:
            self.context.logger.error("Orders message is None")
            return False
        if orders.performative is OrdersMessage.Performative.ERROR:
            self.context.logger.error(f"Error getting orders: {orders}")
            return False
        if orders.performative is not OrdersMessage.Performative.ORDERS:
            self.context.logger.error(f"Invalid performative: {orders.performative}")
            return False
        try:
            return all(
                [
                    orders is not None,
                    isinstance(orders, OrdersMessage),
                    orders.orders is not None,
                ]
            )
        except Exception as err:
            self.context.logger.exception("Orders message is None")
            msg = f"Error validating orders message: {err}"
            raise ValueError(msg) from err

    def _validate_balance_msg(self, balances: BalancesMessage) -> bool:
        """Validate the balance message."""
        return all(
            [
                balances is not None,
                isinstance(balances, BalancesMessage),
                balances.performative != BalancesMessage.Performative.ERROR,
            ]
        )

    def _handle_error(self, attempts=1) -> Generator[None, None, bool]:
        self.attempts += 1
        if self.attempts >= attempts:
            self.context.logger.error("Max attempts reached. Giving up.")
            self._event = ArbitrageabciappEvents.TIMEOUT
            self._is_done = True
            return False
        return True

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
            asset_a = self.strategy.trading_strategy.base_asset
            asset_b = self.strategy.trading_strategy.quote_asset
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
                    yield from self._handle_error()
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
                yield from self._handle_error()
                return
        return tickers  # noqa:B901

    def setup(self) -> None:
        """Setup the state."""
        self.started = False
        self._is_done = False
        self._event = ArbitrageabciappEvents.TIMEOUT
        self.attempts = 0
        super().setup()
