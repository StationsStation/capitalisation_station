# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
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

"""This package contains a scaffold of a handler."""

import json
from typing import Optional, cast

from aea.skills.base import Handler
from aea.protocols.base import Message
from aea.configurations.base import PublicId

from packages.valory.protocols.http.message import HttpMessage
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.skills.reporting.strategy import ReportingStrategy
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.skills.reporting.behaviours import from_id_to_instrument_name
from packages.eightballer.protocols.orders.custom_types import Order
from packages.eightballer.protocols.positions.custom_types import Position


class BaseHandler(Handler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = Optional[PublicId]  # noqa

    def setup(self) -> None:
        """Implement the setup."""

    def handle(self, message: Message) -> None:
        """Implement the reaction to an event."""
        self.context.logger.info(f"Handling message: {message}")

    def _handle_error(self, message: Message):
        self.context.logger.error(f"Error in {self.__class__.__name__} handler: {message}")

    def teardown(self) -> None:
        """Implement the handler teardown."""

    @property
    def strategy(self):
        """Get the strategy."""
        return cast(ReportingStrategy, self.context.reporting_strategy)


class MarketsReportingHandler(BaseHandler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = MarketsMessage.protocol_id

    def handle(self, message: Message) -> None:
        """Implement the reaction to an event."""
        self.context.logger.debug(f"Reporting on markets: {message}")
        new_instances = []
        existing_instances = []
        if message.performative == MarketsMessage.Performative.ALL_MARKETS:
            for market in message.markets.markets:
                market.info = json.dumps(market.info)
                if isinstance(market.precision, dict):
                    market.precision = market.precision["amount"]
                if isinstance(market.limits, dict):
                    market.limits = market.limits["amount"]["min"]
                market.id = f"{message.exchange_id}_{market.symbol}_{self.context.agent_address}"
                market.exchange_id = message.exchange_id
                instance = self.strategy.get_instance(market, "id")
                if not instance:
                    new_instances.append(market)
                else:
                    existing_instances.append(market)
            if new_instances:
                self.strategy.bulk_add_instances(new_instances)
            if existing_instances:
                self.strategy.bulk_update_instances(existing_instances)
        elif message.performative == MarketsMessage.Performative.ERROR:
            self._handle_error(message)
        else:
            msg = f"Cannot handle message of performative {message.performative}"
            raise ValueError(msg)


class BalancesReportingHandler(BaseHandler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = BalancesMessage.protocol_id

    def handle(self, message: Message) -> None:
        """Handle reports on balances."""
        self.context.logger.debug(f"Reporting on balances: {message}")
        new_instances = []
        existing_instances = []
        if message.performative == BalancesMessage.Performative.ALL_BALANCES:
            for balance in message.balances.balances:
                balance.id = f"{message.exchange_id}_{balance.asset_id}_{self.context.agent_address}"
                balance.exchange_id = message.exchange_id
                instance = self.strategy.get_instance(balance, "id")
                if not instance:
                    new_instances.append(balance)
                else:
                    existing_instances.append(balance)
            if new_instances:
                self.strategy.bulk_add_instances(new_instances)
            if existing_instances:
                self.strategy.bulk_update_instances(existing_instances)
        elif message.performative == BalancesMessage.Performative.ERROR:
            self._handle_error(message)
        else:
            msg = f"Cannot handle message of performative {message.performative}"
            raise ValueError(msg)


class OrdersReportingHandler(BaseHandler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = OrdersMessage.protocol_id

    def handle(self, message: Message) -> None:
        """Handle reports on orders."""
        self.context.logger.debug(f"Reporting on orders: {message}")
        new_instances = []
        existing_instances = []
        if message.performative == OrdersMessage.Performative.ORDERS:
            for order in message.orders.orders:
                _order = self._parse_order(order)
                instance = self.strategy.get_instance(_order, "id")
                if not instance:
                    new_instances.append(_order)
                else:
                    existing_instances.append(_order)
            if new_instances:
                self.strategy.bulk_add_instances(new_instances)
            if existing_instances:
                self.strategy.bulk_update_instances(existing_instances)

        elif message.performative in {
            OrdersMessage.Performative.ORDER,
            OrdersMessage.Performative.CREATE_ORDER,
        }:
            order = message.order
            _order = self._parse_order(order)
            instance = self.strategy.get_instance(_order, "id")
            if not instance:
                self.strategy.add_instance(_order)
            else:
                self.strategy.bulk_update_instances([_order])
        elif message.performative == OrdersMessage.Performative.ERROR:
            self._handle_error(message)
        else:
            msg = f"Cannot handle message of performative {message.performative}"
            raise ValueError(msg)

    def _parse_order(self, order: Order):
        """Parse the order."""
        data = order.dict()
        order = Order(**data)
        order.fee = None
        order.fees = None
        order.trades = None
        return order


class TickersReportingHandler(BaseHandler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = TickersMessage.protocol_id

    def handle(self, message: Message) -> None:
        """Handle reports on tickers."""
        self.context.logger.debug(f"Reporting on tickers: {message}")
        new_instances = []
        existing_instances = []
        if message.performative == TickersMessage.Performative.ALL_TICKERS:
            for ticker in message.tickers.tickers:
                ticker.info = json.dumps(ticker.info)
                ticker.id = f"{message.exchange_id}_{ticker.symbol}_{self.context.agent_address}"
                instance = self.strategy.get_instance(ticker, "id")
                if not instance:
                    new_instances.append(ticker)
                else:
                    existing_instances.append(ticker)
            if new_instances:
                self.strategy.bulk_add_instances(new_instances)
            if existing_instances:
                self.strategy.bulk_update_instances(existing_instances)
        elif message.performative == TickersMessage.Performative.ERROR:
            self._handle_error(message)
        else:
            msg = f"Cannot handle message of performative {message.performative}"
            raise ValueError(msg)


class PositionsReportingHandler(BaseHandler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = PositionsMessage.protocol_id

    def handle(self, message: Message) -> None:
        """Handle reports on positions."""
        self.context.logger.debug(f"Reporting on positions: {message}")
        new_instances = []
        existing_instances = []
        if message.performative == PositionsMessage.Performative.ALL_POSITIONS:
            for position in message.positions.positions:
                instance = self._handle_position(position, message)
                if not instance:
                    new_instances.append(position)
                else:
                    existing_instances.append(position)
        elif message.performative == PositionsMessage.Performative.POSITION:
            position = message.position
            instance = self._handle_position(position, message)
            if not instance:
                new_instances.append(position)
            else:
                existing_instances.append(position)
        elif message.performative == PositionsMessage.Performative.ERROR:
            self._handle_error(message)
        else:
            msg = f"Cannot handle message of performative {message.performative}"
            raise ValueError(msg)
        if new_instances:
            self.strategy.bulk_add_instances(new_instances)
        if existing_instances:
            self.strategy.bulk_update_instances(existing_instances)
        if any([new_instances, existing_instances]):
            self.strategy.pivot_all_exchanges()
            self.strategy.pivot_all_positions()

    def _handle_position(self, position: Position, message) -> None:
        """We refactor the position to be a dict."""
        position.info = json.dumps(position.info)
        position.id = f"{message.exchange_id}_{position.symbol}_{self.context.agent_address}"
        return self.strategy.get_instance(position, "id")

    def _handle_error(self, message: Message):
        self.context.logger.error(f"Error in {self.__class__.__name__} handler: {message}")
        if message.error_code == PositionsMessage.ErrorCode.UNKNOWN_POSITION:
            # we need to set the position to closed by nulling the size.
            # we get the last out going message.
            dialogue = self.context.positions_dialogues.update(message=message)
            if dialogue:
                last_outgoing_message = dialogue.last_outgoing_message
                position_id = f"{last_outgoing_message.exchange_id}_{from_id_to_instrument_name(last_outgoing_message.position_id)}_{self.context.agent_address}"  # noqa: E501
                position = Position(
                    id=position_id,
                    symbol=from_id_to_instrument_name(last_outgoing_message.position_id),
                )
                position_model = self.strategy.get_instance(position, "id")
                if position_model:
                    position.size = 0
                    self.strategy.bulk_update_instances([position])
                else:
                    self.context.logger.error(f"Could not find position for {position.id}")
            else:
                self.context.logger.error(f"Could not find dialogue for {message.performative}")
        else:
            msg = f"Cannot handle message of performative {message.performative}"
            raise ValueError(msg)


class HttpHandler(BaseHandler):
    """The HTTP response handler."""

    SUPPORTED_PROTOCOL: PublicId | None = HttpMessage.protocol_id
    allowed_response_performatives = frozenset({HttpMessage.Performative.RESPONSE})

    def handle(self, message: Message) -> None:
        """Handle the http response message."""
        msg = cast(HttpMessage, message)
        self.context.http_dialogues.update(msg)
        if msg.performative == HttpMessage.Performative.RESPONSE:
            if msg.status_code == 200:
                if json.loads(msg.body)["ok"]:
                    self.context.logger.debug("success")
                else:
                    msg = f"FAILED http error: status_code={msg.status_code}"
                    raise ValueError(msg)
            else:
                msg = f"FAILED http error: status_code={msg.status_code}"
                raise ValueError(msg)
        else:
            msg = f"Cannot handle message of performative {msg.performative}"
            raise ValueError(msg)
