# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains round behaviours of AbciApp."""

import json
import time
from abc import ABC
from typing import Any, cast
from collections.abc import Generator

from aea.mail.base import Message

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.eightballer.connections.dcxt.connection import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.skills.dex_data_retrieval.models import Params
from packages.eightballer.skills.dex_data_retrieval.rounds import (
    Event as Events,
    SynchronizedData,
    FetchDexOrdersRound,
    FetchDexMarketsRound,
    FetchDexTickersRound,
    FetchDexBalancesRound,
    FetchDexOrdersPayload,
    FetchDexMarketsPayload,
    FetchDexPositionsRound,
    DexDataRetrievalAbciApp,
    FetchDexBalancesPayload,
    FetchDexPositionsPayload,
)
from packages.valory.skills.abstract_round_abci.behaviours import BaseBehaviour, AbstractRoundBehaviour
from packages.eightballer.skills.dex_data_retrieval.payloads import FetchDexTickersPayload


DEFAULT_RETRIES = 10
DEFAULT_RETRY_DELAY = 5.0


class DexDataRetrievalBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the dex_data_retrieval skill."""

    done_event = Events.DONE

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)

    def get_ccxt_response(
        self,
        protocol_performative: Message.Performative,
        **kwargs,
    ) -> Generator[None, None, Any]:
        """Get a ccxt response."""
        if protocol_performative not in self._performative_to_dialogue_class:
            msg = f"Unsupported protocol performative '{protocol_performative}'"
            raise ValueError(msg)
        dialogue_class = self._performative_to_dialogue_class[protocol_performative]

        msg, dialogue = dialogue_class.create(
            counterparty=str(DCXT_PUBLIC_ID),
            performative=protocol_performative,
            **kwargs,
        )
        msg._sender = str(self.context.skill_id)  # noqa
        response = yield from self._do_request(msg, dialogue)
        return response

    def __init__(self, **kwargs: Any):
        """Initialize the behaviour."""
        super().__init__(**kwargs)
        self._performative_to_dialogue_class = {
            MarketsMessage.Performative.GET_ALL_MARKETS: self.context.markets_dialogues,
            OrdersMessage.Performative.GET_ORDERS: self.context.orders_dialogues,
            BalancesMessage.Performative.GET_ALL_BALANCES: self.context.balances_dialogues,
            PositionsMessage.Performative.GET_ALL_POSITIONS: self.context.positions_dialogues,
            TickersMessage.Performative.GET_ALL_TICKERS: self.context.tickers_dialogues,
        }


class FetchDexMarketsBehaviour(DexDataRetrievalBaseBehaviour):
    """FetchDexMarketsBehaviour."""

    matching_round: type[AbstractRound] = FetchDexMarketsRound
    behaviour_id = "fetch_dex_markets_behaviour"

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        exchange_ids = self.params.dex_data_retrieval_config.exchange_ids
        extra_kwargs = self.params.dex_data_retrieval_config.extra_kwargs

        if self.params.dex_data_retrieval_config.enabled:
            self.context.logger.info(f"Fetching markets from {exchange_ids}")

        exchange_to_markets = {}
        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            for exchange_id in exchange_ids:
                extra_kwargs = extra_kwargs.get(exchange_id, {}) if extra_kwargs else {}
                successful = False
                retries = 0
                while not successful and retries < DEFAULT_RETRIES:
                    msg: MarketsMessage = yield from self.get_ccxt_response(
                        protocol_performative=MarketsMessage.Performative.GET_ALL_MARKETS,
                        exchange_id=exchange_id,
                        **extra_kwargs,
                    )
                    if not self._is_result_ok(msg, exchange_id):
                        retries += 1
                        time.sleep(DEFAULT_RETRY_DELAY)
                    else:
                        successful = True

                if not successful:
                    self.context.logger.error(
                        f"Error fetching markets from {exchange_id} after {DEFAULT_RETRIES} retries. Aborting..."
                    )
                    exchange_to_markets = None
                    break
                exchange_to_markets[exchange_id] = self._from_markets_to_dict(msg, exchange_id)
                self.context.logger.info(f"Received {len(exchange_to_markets[exchange_id])} markets from {exchange_id}")

            self.context.logger.info(f"Fetched Exchanges: {exchange_ids}")
            sender = self.context.agent_address
            payload = FetchDexMarketsPayload(
                sender=sender,
                markets=json.dumps(exchange_to_markets),
            )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _is_result_ok(self, msg: MarketsMessage, exchange_id) -> bool:
        if msg.Performative == MarketsMessage.Performative.ERROR:
            self.context.logger.error(f"Error fetching markets from {exchange_id}: {msg.error_msg} Retrying...")
            return False
        return True

    def _from_markets_to_dict(self, markets_msg: MarketsMessage, exchange_id: str) -> dict:
        """Convert markets message to dict."""
        return {
            exchange_id: {m.id: m.symbol for m in markets_msg.markets.markets},
        }


class FetchDexBalancesBehaviour(DexDataRetrievalBaseBehaviour):
    """FetchDexBalancesBehaviour."""

    matching_round: type[AbstractRound] = FetchDexBalancesRound
    behaviour_id = "fetch_dex_balances_behaviour"

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        exchange_ids = self.params.dex_data_retrieval_config.exchange_ids
        extra_kwargs = self.params.dex_data_retrieval_config.extra_kwargs

        exchange_to_balances = {}
        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            for exchange_id in exchange_ids:
                params = {}
                if extra_kwargs is not None:
                    params = extra_kwargs.get(exchange_id, {}).copy()
                # extra kwargs must in the form str to bytes
                for key, value in params.items():
                    params[key] = value.encode("utf-8")

                msg: BalancesMessage = yield from self.get_ccxt_response(
                    protocol_performative=BalancesMessage.Performative.GET_ALL_BALANCES,
                    exchange_id=exchange_id,
                    params=params,
                )

                balances = self._from_balances_to_dict(msg, exchange_id)
                self.context.logger.info(f"Received {len(balances[exchange_id])} balances from {exchange_id}")
                exchange_to_balances.update(balances)
            sender = self.context.agent_address
            payload = FetchDexBalancesPayload(
                sender=sender,
                balances=json.dumps(exchange_to_balances),
            )
        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _from_balances_to_dict(self, balances_msg: BalancesMessage, exchange_id: str) -> dict:
        """Convert balances message to dict."""
        return {
            exchange_id: [b.as_json() for b in balances_msg.balances.balances],
        }


class FetchDexOrdersBehaviour(DexDataRetrievalBaseBehaviour):
    """FetchDexOrdersBehaviour."""

    matching_round: type[AbstractRound] = FetchDexOrdersRound
    behaviour_id = "fetch_dex_orders_behaviour"
    done_event = Events.DONE

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        extra_kwargs = self.params.dex_data_retrieval_config.extra_kwargs
        exchange_to_orders = {}
        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            for exchange_id in self.params.dex_data_retrieval_config.exchange_ids:
                extra_kwargs = extra_kwargs.get(exchange_id, {})
                msg: OrdersMessage = yield from self.get_ccxt_response(
                    protocol_performative=OrdersMessage.Performative.GET_ORDERS,
                    exchange_id=exchange_id,
                    **extra_kwargs,
                )
                self.context.logger.info(f"Received {len(msg.orders.orders)} orders from {exchange_id}")
                exchange_to_orders.update(self._from_orders_to_dict(msg, exchange_id))

            sender = self.context.agent_address
            payload = FetchDexOrdersPayload(
                sender=sender,
                orders=json.dumps(exchange_to_orders),
            )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _from_orders_to_dict(self, orders_msg: OrdersMessage, exchange_id) -> dict:
        """Convert orders message to dict."""
        return {
            exchange_id: [o.as_json() for o in orders_msg.orders.orders],
        }


class FetchDexPositionsBehaviour(DexDataRetrievalBaseBehaviour):
    """FetchDexPositionsBehaviour."""

    matching_round: type[AbstractRound] = FetchDexPositionsRound
    behaviour_id = "fetch_dex_positions_behaviour"
    done_event = Events.DONE

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        extra_kwargs = self.params.dex_data_retrieval_config.extra_kwargs
        exchange_to_positions = {}

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            for exchange_id in self.params.dex_data_retrieval_config.exchange_ids:
                extra_kwargs = extra_kwargs.get(exchange_id, {})
                params = {}
                for key, value in extra_kwargs.items():
                    params[key] = value.encode("utf-8")

                msg: PositionsMessage = yield from self.get_ccxt_response(
                    protocol_performative=PositionsMessage.Performative.GET_ALL_POSITIONS,
                    exchange_id=exchange_id,
                    params=params,
                )
                exchange_to_positions.update(self._from_positions_to_dict(msg, exchange_id))
                self.context.logger.info(
                    f"Received {len(exchange_to_positions[exchange_id])} positions from {exchange_id}"
                )

            sender = self.context.agent_address
            payload = FetchDexPositionsPayload(
                sender=sender,
                positions=json.dumps(exchange_to_positions),
            )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _from_positions_to_dict(self, positions_msg: PositionsMessage, exchange_id: str) -> dict:
        """Convert positions message to dict."""
        for pos in positions_msg.positions.positions:
            pos.exchange_id = exchange_id
        return {
            exchange_id: [pos.as_json() for pos in positions_msg.positions.positions],
        }


class FetchDexTickersBehaviour(DexDataRetrievalBaseBehaviour):
    """FetchDexTickersBehaviour."""

    matching_round: type[AbstractRound] = FetchDexTickersRound
    behaviour_id = "fetch_dex_tickers_behaviour"
    done_event = Events.DONE

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        extra_kwargs = self.params.dex_data_retrieval_config.extra_kwargs
        exchange_to_tickers = {}

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            for exchange_id in self.params.dex_data_retrieval_config.exchange_ids:
                params = extra_kwargs.get(exchange_id, {}).copy()
                for key, value in params.items():
                    params[key] = value.encode("utf-8")
                msg: TickersMessage = yield from self.get_ccxt_response(
                    protocol_performative=TickersMessage.Performative.GET_ALL_TICKERS,
                    exchange_id=exchange_id,
                    params=params,
                )
                exchange_to_tickers.update(self._from_tickers_to_dict(msg, exchange_id))
                self.context.logger.info(f"Received {len(exchange_to_tickers[exchange_id])} tickers from {exchange_id}")

            sender = self.context.agent_address
            self.context.logger.info(f"Received Exchanges: {exchange_to_tickers}")
            payload = FetchDexTickersPayload(
                sender=sender,
                tickers=json.dumps(exchange_to_tickers),
            )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _from_tickers_to_dict(self, tickers_msg: TickersMessage, exchange_id: str) -> dict:
        """Convert tickers message to dict."""

        def select_fields(ticker):
            fields = [
                "symbol",
                "bid",
                "bidVolume",
                "ask",
                "askVolume",
                "last",
                "lastVolume",
                "high",
                "low",
                "last",
                "datetime",
                "close",
            ]
            return {k: v for k, v in ticker.items() if k in fields}

        return {
            exchange_id: [select_fields(t.as_json()) for t in tickers_msg.tickers.tickers],
        }


class DexDataRetrievalRoundBehaviour(AbstractRoundBehaviour):
    """RoundBehaviour."""

    initial_behaviour_cls = FetchDexMarketsBehaviour
    abci_app_cls = DexDataRetrievalAbciApp  # type: ignore
    behaviours: set[type[BaseBehaviour]] = {
        FetchDexBalancesBehaviour,
        FetchDexMarketsBehaviour,
        FetchDexTickersBehaviour,
        FetchDexOrdersBehaviour,
        FetchDexPositionsBehaviour,
    }
