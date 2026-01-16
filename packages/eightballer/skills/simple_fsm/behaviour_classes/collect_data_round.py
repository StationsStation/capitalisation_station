"""Collect data round behaviour class."""

from datetime import datetime, timedelta
from collections.abc import Generator

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.skills.simple_fsm.strategy import TZ, CEX_LEDGER_ID, ArbitrageStrategy
from packages.eightballer.connections.ccxt_wrapper.connection import PUBLIC_ID as CCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseConnectionRound


DATA_COLLECTION_TIMEOUT_SECONDS = 10
DEFAULT_ENCODING = "utf-8"


def get_base_and_quote(symbol: str) -> tuple[str, str] | None:
    if len(assets := symbol.split("/")) == 2:
        base_asset, quote_asset = assets
        return base_asset, quote_asset
    return None


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
            if not all((balances, tickers, orders)):
                self.context.logger.error(
                    f"Error getting data for {exchange_id} on {CEX_LEDGER_ID}",
                    extra={"balances": balances, "tickers": tickers, "orders": orders},
                )
                yield from self._handle_error()
                return

            if any(
                [
                    balances.performative == BalancesMessage.Performative.ERROR,
                    tickers.performative == TickersMessage.Performative.ERROR,
                    orders.performative == OrdersMessage.Performative.ERROR,
                ]
            ):
                self.context.logger.error(
                    f"Error performative for {exchange_id} on {CEX_LEDGER_ID}",
                    extra={"balances": balances, "tickers": tickers, "orders": orders},
                )
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
            self.context.logger.debug("Starting data collection.")
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

        sent_bals = len(self.pending_bals)
        recv_bals = len(self.supported_protocols.get(BalancesMessage.protocol_id))
        sent_orders = len(self.pending_orders)
        recv_orders = len(self.supported_protocols.get(OrdersMessage.protocol_id))
        if sent_bals != recv_bals or sent_orders != recv_orders:
            self.context.logger.debug(
                "Waiting for pending messages.",
                extra={
                    "sent_bals": sent_bals,
                    "recv_bals": recv_bals,
                    "sent_orders": sent_orders,
                    "recv_orders": recv_orders,
                },
            )
            if not datetime.now(tz=TZ) - timedelta(seconds=DATA_COLLECTION_TIMEOUT_SECONDS) < self.started_at:
                self.context.logger.error("Timeout waiting for messages getting data from all exchanges.")
                self._event = ArbitrageabciappEvents.TIMEOUT
                self._is_done = True
                self.started = False
                return
            return

        # we validate all the responses
        invalid_messages = []
        for dialogue in self.pending_bals + self.pending_orders:
            if not dialogue.validation_func(dialogue.last_message):
                invalid_messages.append(dialogue.last_message)

        if invalid_messages:
            self.context.logger.error(
                "Not all received balance and order messages are valid.",
                extra={"invalid_messages": invalid_messages},
            )
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

        # Retrieve the strategy parameters as provided per the aea-config.yaml
        strategy_base_asset = self.strategy.strategy_init_kwargs["base_asset"]
        strategy_quote_asset = self.strategy.strategy_init_kwargs["quote_asset"]  # always USDC

        # NOTE: ideally, we would use the ledger_id and exchange from a config
        # instead of assuming we have only two such pairs (i.e. ("derive", "derive") and ("base", "cowswap"))
        asset_holdings = {}

        # 1. get the all token holdings
        for ledger_id, exchanges in self.strategy.state.portfolio.items():
            for exchange_id, balances in exchanges.items():
                venue = (ledger_id, exchange_id)
                for balance_kwargs in balances:
                    balance = BalancesMessage.Balance(**balance_kwargs)
                    asset_id = balance.asset_id  # field always exists
                    amount = balance.total  # field always exists
                    asset_holdings[(venue, asset_id)] = amount
        self.context.logger.debug(f"Asset holdings: {asset_holdings}")

        # 2. get base and quote asset holdings
        base_asset_holdings = {}
        quote_asset_holdings = {}
        for (venue, asset_id), amount in asset_holdings.items():
            if asset_id == strategy_base_asset:
                base_asset_holdings[venue] = amount
            if asset_id == strategy_quote_asset:
                quote_asset_holdings[venue] = amount
        self.context.logger.debug(f"Base asset holdings: {base_asset_holdings}")
        self.context.logger.debug(f"Quote asset holdings: {quote_asset_holdings}")
        # We assume we only operate and track portfolio balance accross two venues
        base_asset_balances_available = len(base_asset_holdings) == 2
        quote_asset_balances_available = len(quote_asset_holdings) == 2

        # if not base_asset_balances_available:
        #     self.context.logger.warning(f"Expected {base_asset} balances on 2 venues, found: {base_asset_holdings}")
        # if not quote_asset_balances_available:
        #     self.context.logger.warning(f"Expected {quote_asset} balances on 2 venues, found: {quote_asset_holdings}")

        # 3. Get the base_asset ticker at both venues
        base_asset_tickers: dict[tuple[str, str], TickersMessage.Ticker] = {}
        for ledger_id, exchanges in self.strategy.state.prices.items():
            for exchange_id, tickers in exchanges.items():
                venue = (ledger_id, exchange_id)
                for ticker_kwargs in tickers:
                    ticker = TickersMessage.Ticker(**ticker_kwargs)
                    base_asset, quote_asset = get_base_and_quote(symbol=ticker.symbol)
                    if base_asset == strategy_base_asset and quote_asset == strategy_quote_asset:  # TODO: case incensitive matching
                        base_asset_tickers[venue] = ticker
                        break
                else:
                    self.context.logger.warning(f"No ticker for {strategy_base_asset}/{strategy_quote_asset} on {venue}")
        self.context.logger.info(f"Base asset tickers: {base_asset_tickers}")

        base_asset_tickers_available = len(base_asset_tickers) == 2

        # 4. get the value of base_asset token holdings in quote_asset denomination
        # If there is no bid, the value is zero and we end up with a downward spike in our signal
        quote_asset_denominated_value = {}
        for venue, base_asset_ticker in base_asset_tickers.items():
            base_asset_quote_denominated_price = base_asset_ticker.bid or 0.0
            if base_asset_quote_denominated_price == 0.0:
                self.context.logger.warning(f"Cannot determine value of token (no bid price): {base_asset_ticker}")

            base_asset_amount = base_asset_holdings.get(venue) # should exist, but we may not (yet) have received the message
            if base_asset_amount is None:
                self.context.logger.warning(f"Did not find holdings of {base_asset} on {venue} for ticker {base_asset_ticker}")
                continue

            base_asset_value = base_asset_amount * base_asset_quote_denominated_price
            quote_asset_denominated_value[venue] = base_asset_value
            # if venue not in quote_asset_holdings:  # should exist, but we may not (yet) have received the message
                # self.context.logger.warning(f"Did not find {strategy_quote_asset} holdings on {venue}")

        # 4. compute the sum total accross all (both) venues and store
        # we only store if we have:
        #   - token tickers (even if bid is zero)
        #   - USDC balances on both venues (even if amount is zero)
        #   - token balances on both venues (even if amount is zero)

        # In case there is no ticker bid, no base asset holding, or no quote asset holding on one of the two venues
        # i.e. due to missed message or any other reason, we will get a downward spike in our signal

        # This can be simplified. We could exit early, however, we do need to set the flags at the end of this method body!
        quote_asset_denominated_value_available = len(quote_asset_denominated_value) == 2
        if base_asset_balances_available and quote_asset_balances_available and base_asset_tickers_available and quote_asset_denominated_value_available:
            total_usd = sum(quote_asset_holdings.values()) + sum(quote_asset_denominated_value.values())
            try:
                self.strategy.portfolio_db.save_snapshot(total_usd=total_usd)
            except Exception:
                self.context.logger.exception("Error saving portfolio snapshot", exc_info=True)
        else:
            self.context.logger.info(
                f"Not all asset data available (yet):\n"
                f"Base asset ({strategy_base_asset}) balances: {base_asset_holdings}\n"
                f"Quote asset ({strategy_quote_asset}) balances: {quote_asset_holdings}\n"
                f"Base asset tickers: {base_asset_tickers}\n"
                f"Total {strategy_quote_asset} denominated value: {quote_asset_denominated_value}"
            )

        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.attempts = 0
        self.context.logger.debug("Data collection complete.")

    def _validate_orders_msg(self, orders: OrdersMessage) -> bool:
        """Validate the orders message."""
        if orders is None:
            self.context.logger.error("Orders message is None")
            return False
        if orders.performative is OrdersMessage.Performative.ERROR:
            self.context.logger.error("Error performative.", extra={"orders": orders})
            return False
        if orders.performative is not OrdersMessage.Performative.ORDERS:
            self.context.logger.error("Invalid performative.", extra={"orders": orders})
            return False
        try:
            return all(
                [
                    orders is not None,
                    isinstance(orders, OrdersMessage),
                    orders.orders is not None,
                ]
            )
        except Exception:
            self.context.logger.exception("Error validating orders message.")
            return False

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
            self.context.logger.error(f"Max retry attempts ({self.attempts}) reached.")
            self._event = ArbitrageabciappEvents.TIMEOUT
            self._is_done = True
            return False
        return True

    def setup(self) -> None:
        """Setup the state."""
        self.started = False
        self._is_done = False
        self._event = ArbitrageabciappEvents.TIMEOUT
        self.attempts = 0
        super().setup()
        for k in self.supported_protocols:
            self.supported_protocols[k] = []
