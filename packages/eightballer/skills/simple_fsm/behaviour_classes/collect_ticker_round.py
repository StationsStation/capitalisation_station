"""Collect data round behaviour class."""

import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections.abc import Callable, Generator

from aea.protocols.dialogue.base import Dialogue as BaseDialogue

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.skills.simple_fsm.strategy import TZ, ArbitrageStrategy
from packages.eightballer.protocols.tickers.custom_types import Tickers
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseConnectionRound


DATA_COLLECTION_TIMEOUT_SECONDS = 10
DEFAULT_ENCODING = "utf-8"


@dataclass
class AggregateRequest:
    """Aggregate request class."""

    validation_func: Callable
    exchange_id: str
    ledger_id: str
    ticker_request_dialogues: list[BaseDialogue]


class CollectTickerRound(BaseConnectionRound):
    """This class implements the CollectDataRound state."""

    matching_round = "collecttickerround"
    attempts = 0
    started = False

    supported_protocols = {
        TickersMessage.protocol_id: [],
    }

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy

    def _handle_startup(self) -> None:
        """Handle the startup of the state."""
        self.started = True
        self.started_at = datetime.now(tz=TZ)
        self.context.logger.info("Starting ticker collection.")
        self.pending_tickers: list[AggregateRequest] = []
        for k in self.supported_protocols:
            self.supported_protocols[k] = []

        for exchange_id, ledger_ids in self.strategy.dexs.items():
            for ledger_id in ledger_ids:
                self.context.logger.debug(f"Getting tickers for {exchange_id} on {ledger_id}")
                tickers_request = self.get_tickers(
                    exchange_id=exchange_id,
                    ledger_id=ledger_id,
                )
                self.pending_tickers.append(tickers_request)

    def act(self) -> Generator:
        """Perform the action of the state."""

        if not self.started:
            self._handle_startup()
            return None

        sent_tickers = sum(len(i.ticker_request_dialogues) for i in self.pending_tickers)
        recv_tickers = len(self.supported_protocols.get(TickersMessage.protocol_id))
        if sent_tickers != recv_tickers:
            self.context.logger.debug(
                self.context.logger.debug(
                    "Waiting for pending messages.",
                    extra={
                        "sent_tickers": sent_tickers,
                        "recv_tickers": recv_tickers,
                    },
                )
            )
            if not datetime.now(tz=TZ) - timedelta(seconds=DATA_COLLECTION_TIMEOUT_SECONDS) < self.started_at:
                self.context.logger.error("Timeout waiting for messages getting tickers from all exchanges.")
                self.started = False
                return self._handle_error()
            return None

        invalid_messages = []
        for aggregate_request in self.pending_tickers:
            for dialogue in aggregate_request.ticker_request_dialogues:
                if not dialogue.validation_func(dialogue.last_message):
                    invalid_messages.append(dialogue.last_message)

        if invalid_messages:
            self.context.logger.error(
                "Not all received ticker messages are valid.",
                extra={"invalid_messages": invalid_messages},
            )
            self._handle_error()
            return None

        for aggregate_ticker in self.pending_tickers:
            tickers = Tickers(tickers=[])
            for ticker in aggregate_ticker.ticker_request_dialogues:
                tickers.tickers.append(ticker.last_incoming_message.ticker)

            self.strategy.state.prices[ticker.ledger_id][ticker.exchange_id] = [t.dict() for t in tickers.tickers]

        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.attempts = 0
        self.context.logger.debug("Ticker collection complete.")
        return None

    def _handle_error(self, attempts=1) -> Generator[None, None, bool]:
        self.attempts += 1
        if self.attempts >= attempts:
            self.context.logger.error(f"Max retry attempts ({self.attempts}) reached.")
            self._event = ArbitrageabciappEvents.TIMEOUT
            self._is_done = True
            return False
        return True

    def get_tickers(
        self,
        exchange_id: str,
        ledger_id: str,
    ) -> AggregateRequest:
        """Get the tickers from a specific exchange."""
        performative = (
            TickersMessage.Performative.GET_ALL_TICKERS
            if self.context.arbitrage_strategy.fetch_all_tickers
            else TickersMessage.Performative.GET_TICKER
        )

        aggregated_request = AggregateRequest(
            validation_func=self._validate_ticker_msg,
            exchange_id=exchange_id,
            ledger_id=ledger_id,
            ticker_request_dialogues=[],
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
            for param in params:
                ticker_dialogue = self.submit_msg(
                    performative,
                    connection_id=str(DCXT_PUBLIC_ID),
                    exchange_id=exchange_id,
                    ledger_id=ledger_id,
                    **param,
                )
                ticker_dialogue.validation_func = self._validate_ticker_msg
                ticker_dialogue.exchange_id = exchange_id
                ticker_dialogue.ledger_id = ledger_id
                aggregated_request.ticker_request_dialogues.append(ticker_dialogue)
        else:
            msg = "Please contact the developer to implement this feature."
            raise NotImplementedError(msg)
        return aggregated_request

    def _validate_ticker_msg(self, ticker: TickersMessage) -> bool:
        """Validate the ticker message."""
        if ticker is None:
            return False
        if not isinstance(ticker, TickersMessage):
            return False
        if ticker.performative == TickersMessage.Performative.ERROR:
            return False
        return (
            ticker.performative in {TickersMessage.Performative.TICKER, TickersMessage.Performative.ALL_TICKERS}
            and ticker.ticker is not None
        )

    def setup(self) -> None:
        """Setup the state."""
        self.started = False
        self._is_done = False
        self._event = ArbitrageabciappEvents.TIMEOUT
        self.attempts = 0
        super().setup()
