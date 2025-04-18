# ------------------------------------------------------------------------------
#
#   Copyright 2023
#   Copyright 2023 valory-xyz
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

"""This package contains a behaviour that autogenerated from the protocol ``."""

import os
import sys
import asyncio
import pathlib
import importlib
from typing import Any
from datetime import datetime
from textwrap import dedent
from collections.abc import Generator

from aea.skills.behaviours import FSMBehaviour
from aea.configurations.base import ComponentType
from aea.configurations.loader import load_component_configuration

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.skills.simple_fsm.strategy import TZ, ArbitrageStrategy
from packages.eightballer.protocols.orders.custom_types import Order, OrderStatus
from packages.eightballer.connections.ccxt_wrapper.connection import PUBLIC_ID as CCXT_PUBLIC_ID
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseBehaviour, BaseConnectionRound
from packages.eightballer.skills.simple_fsm.behaviour_classes.post_trade_round import PostTradeRound
from packages.eightballer.skills.simple_fsm.behaviour_classes.collect_data_round import CollectDataRound
from packages.eightballer.skills.simple_fsm.behaviour_classes.no_opportunity_round import NoOpportunityRound


DEFAULT_ENCODING = "utf-8"


# Define states

PORTFOLIO_FILE = "portfolio.json"
EXISTING_ORDERS_FILE = "existing_orders.json"
FAILED_ORDERS_FILE = "failed_orders.json"
ORDERS_FILE = "orders.json"
PRICES_FILE = "prices.json"

ORDER_PLACEMENT_TIMEOUT_SECONDS = 10


class UnexpectedStateException(Exception):
    """Exception raised when an unexpected state is reached."""


class SetupRound(BaseBehaviour):
    """This class implements the SetupRound state."""

    clear_data = False
    is_first_run = True

    async def act(self) -> None:
        """Perform the action of the state."""
        self.context.logger.debug("SetupRound: Performing action")
        self._event = ArbitrageabciappEvents.DONE
        await asyncio.sleep(0)
        if self.clear_data:
            for f in ["orders.json", "portfolio.json", "prices.json"]:
                if pathlib.Path(f).exists():
                    pathlib.Path(f).unlink()
            self.context.shared_state = {}
        # We also ensure all behaviours are setup

        self.context.behaviours.main.setup()
        self._is_done = True


class IdentifyOpportunityRound(BaseBehaviour):
    """This class implements the IdentifyOpportunityRound state."""

    # we have to import the strategy due to the loading sequence of the agent dependencies.

    async def act(self) -> None:
        """Perform the action of the state."""
        if self.started:
            return
        self.started = True
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE

        orders = self.strategy.trading_strategy.get_orders(
            portfolio=self.strategy.state.portfolio,
            prices=self.strategy.state.prices,
            orders=self.strategy.state.existing_orders,
            **self.custom_config.kwargs["strategy_run_kwargs"],
        )
        self.strategy.state.unaffordable_opportunity = self.strategy.trading_strategy.unaffordable
        if self.strategy.state.unaffordable_opportunity:
            self.context.logger.info(f"Opportunity unaffordable: {self.strategy.state.unaffordable_opportunity}")
        if orders:
            self.context.logger.info(f"Opportunity found: {orders}")
            self.strategy.state.new_orders = orders
            self._event = ArbitrageabciappEvents.OPPORTUNITY_FOUND
        await asyncio.sleep(0)

    def setup(self) -> None:
        """Setup the state."""
        self.started = False
        sys.path.append(".")
        strat_pub_id = self.context.arbitrage_strategy.strategy_public_id

        _dir = "vendor" if pathlib.Path("vendor").exists() else "packages"
        component_dir = pathlib.Path(_dir, strat_pub_id.author, "customs", strat_pub_id.name)
        self.custom_config = load_component_configuration(component_type=ComponentType.CUSTOM, directory=component_dir)

        def validate():
            """Validate the custom configuration."""
            expected_keys = {"strategy_class", "strategy_init_kwargs", "strategy_run_kwargs"}
            missing_keys = expected_keys - set(self.custom_config.kwargs.keys())
            if missing_keys:
                msg = (
                    f"Missing keys in custom configuration: {missing_keys} "
                    + f"Please check the configuration. in {self.custom_config.directory}"
                )
                raise ValueError(msg)
            expected_files = {"strategy.py"}
            missing_files = expected_files - set(self.custom_config.fingerprint.keys())
            if missing_files:
                msg = (
                    f"Missing files in custom configuration: {missing_files} "
                    + f"Please check the configuration. in {self.custom_config.directory}"
                )
                raise ValueError(msg)

        validate()
        strategy_class_name: str = self.custom_config.kwargs["strategy_class"]
        strategy_path = str(component_dir / "strategy").replace("/", ".")
        module = importlib.import_module(strategy_path)
        strategy_class = getattr(module, strategy_class_name)
        self.strategy.trading_strategy = strategy_class(**self.strategy.strategy_init_kwargs)

        self.context.logger.debug("Strategy Kwargs:")
        for k, v in self.strategy.strategy_init_kwargs.items():
            self.context.logger.debug(f"    {k}: {v}")

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy


class ErrorRound(BaseBehaviour):
    """This class implements the ErrorRound state."""

    async def act(self) -> None:
        """Perform the action of the state."""
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        await asyncio.sleep(0)


class CoolDownRound(BaseBehaviour):
    """This class implements the ErrorRound state."""

    async def act(self) -> None:
        """Perform the action of the state."""
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        self.strategy.error_count += 1
        sleep_time = self.strategy.cool_down_period * (2**self.strategy.error_count)
        self.context.logger.info(
            f"In cool down sleeping for {sleep_time} seconds on error attempt {self.strategy.error_count}"
        )
        await asyncio.sleep(sleep_time)


class ExecuteOrdersRound(BaseConnectionRound):
    """This class implements the ExecuteOrdersRound state."""

    matching_round = "executeordersround"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._is_done = False  # Initially, the state is not done
        self.started = False
        self._message = None

    def act(self) -> None:
        """Perform the action of the state."""
        if self.started:
            return
        self.started = True

        submitted = []
        failed_orders = []

        self.context.logger.info(f"Executing Total of {len(self.strategy.state.new_orders)} orders")
        while self.strategy.state.new_orders:
            order = self.strategy.state.new_orders.pop(0)
            self.context.logger.info(f"Creating order: {order}")
            is_entry_order = len(submitted) == 0
            is_exit_order = len(submitted) == 1

            response = yield from self.send_create_order(
                order=order,
                is_entry_order=is_entry_order,
                is_exit_order=is_exit_order,
            )
            if not response:
                self.context.logger.error(f"Error creating order: {order}")
                failed_orders.append(order)
                break

            result_order = response.order
            result = self.handle_submitted_order_response(
                order=result_order,
            )
            if result is None:
                self.context.logger.error(f"Error creating order: {order}")
                failed_orders.append(order)
                continue
            submitted.append(result_order)
            self.context.logger.info(f"Order created: {result_order}")

        self.strategy.state.submitted_orders = submitted
        self.strategy.state.failed_orders = failed_orders

        if not failed_orders:
            self._event = ArbitrageabciappEvents.DONE
            self._is_done = True

    def _handle_failed_entry_order(
        self,
        order: Order,
        msg: str = "Error creating order",
    ) -> None:
        self.context.logger.error(msg)
        self.context.logger.error(f"Error creating order: {order}")
        self._is_done = True
        self._event = ArbitrageabciappEvents.ENTRY_EXIT_ERROR

    def _handle_failed_exit_order(
        self,
        msg: str,
    ) -> None:
        self.context.logger.error(msg)
        raise UnexpectedStateException(msg)

    def send_create_order(
        self,
        order: Order,
        is_entry_order: bool,
        is_exit_order: bool,
    ) -> Generator:
        """Send the create order message."""
        response = yield from self.get_response(
            OrdersMessage.Performative.CREATE_ORDER,
            connection_id=CCXT_PUBLIC_ID if order.ledger_id == "cex" else DCXT_PUBLIC_ID,
            order=order,
            ledger_id=order.ledger_id,
            exchange_id=order.exchange_id,
        )
        if response is None:
            self.context.logger.error(f"Timeout creating order: {order}")
            if is_entry_order:
                return self._handle_failed_entry_order(order)
            if is_exit_order:
                msg = (
                    "Recovery orders are not yet supported."
                    + "Timeout creating order, Hard exiting as manual adjustment needed!"
                )
                return self._handle_failed_exit_order(msg)
        if response.performative is OrdersMessage.Performative.ERROR or response.order.status is OrderStatus.FAILED:
            self.context.logger.error(f"Error creating order: {order} response: {response}")
            if is_entry_order:
                return self._handle_failed_entry_order(order)
            if is_exit_order:
                msg = f"Error creating order: {response} {order}"
                return self._handle_failed_exit_order(msg)
        return response

    def handle_submitted_order_response(
        self,
        order: Order,
    ) -> bool:
        """Handle the order submission response."""

        if order.status == OrderStatus.PARTIALLY_FILLED:
            msg = "Partially filled orders are not yet supported."
            raise UnexpectedStateException(msg)

        if order.status in (
            {
                OrderStatus.FILLED,
                OrderStatus.OPEN,
                OrderStatus.NEW,
            }
        ):
            self.context.logger.info(f"Order created: {order}")
            self.context.logger.info(
                dedent(f"""
            Id: {order.id}
            Exchange: {order.exchange_id}
            Market:   {order.symbol}
            Status:   {order.status}
            Side:     {order.side}
            Price:    {order.price}
            Amount:   {order.amount}
            Filled Amount:   {order.filled}
            """)
            )
            if order.status == OrderStatus.FILLED:
                self.context.logger.info("Order filled.")
                return True
            if order.status in {
                OrderStatus.OPEN,
                OrderStatus.NEW,
            }:
                self.context.logger.info("Order created.")
                self.strategy.state.submitted_orders.append(order)
                return True
            msg = f"This is a completely unexpected error. Order {order}"
            raise UnexpectedStateException(msg)
        msg = "This is a placeholder for currently unhandled methods."
        raise UnexpectedStateException(msg)

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy

    def handle_order(self, order: Order) -> None:
        """Handle the order."""


class ArbitrageabciappFsmBehaviour(FSMBehaviour):
    """This class implements a simple Finite State Machine behaviour."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.register_state("setupround", SetupRound(**kwargs), True)

        self.register_state("errorround", ErrorRound(**kwargs))
        self.register_state("posttraderound", PostTradeRound(**kwargs), False)
        self.register_state("noopportunityround", NoOpportunityRound(**kwargs))
        self.register_state("cooldownround", CoolDownRound(**kwargs))

        self.register_state(
            "identifyopportunityround",
            IdentifyOpportunityRound(**kwargs),
        )
        self.register_state(
            "executeordersround",
            ExecuteOrdersRound(**kwargs),
        )
        self.register_state("collectdataround", CollectDataRound(**kwargs))

        self.register_transition(source="setupround", event=ArbitrageabciappEvents.DONE, destination="collectdataround")
        self.register_transition(
            source="collectdataround", event=ArbitrageabciappEvents.DONE, destination="identifyopportunityround"
        )
        self.register_transition(
            source="collectdataround", event=ArbitrageabciappEvents.TIMEOUT, destination="cooldownround"
        )
        self.register_transition(
            source="cooldownround", event=ArbitrageabciappEvents.DONE, destination="collectdataround"
        )
        self.register_transition(
            source="identifyopportunityround",
            event=ArbitrageabciappEvents.OPPORTUNITY_FOUND,
            destination="executeordersround",
        )
        self.register_transition(
            source="identifyopportunityround", event=ArbitrageabciappEvents.DONE, destination="noopportunityround"
        )
        self.register_transition(
            source="executeordersround", event=ArbitrageabciappEvents.DONE, destination="posttraderound"
        )
        self.register_transition(source="posttraderound", event=ArbitrageabciappEvents.DONE, destination="setupround")
        # register a transation from noopportunityround to setupround
        self.register_transition(
            source="noopportunityround", event=ArbitrageabciappEvents.DONE, destination="setupround"
        )
        # register a transation from executeordersround to errorround
        self.register_transition(
            source="executeordersround", event=ArbitrageabciappEvents.ENTRY_EXIT_ERROR, destination="setupround"
        )

    def setup(self) -> None:
        """Implement the setup."""
        self.context.logger.debug("Setting up Arbitrageabciapp FSM behaviour.")
        # We need to setup all the states.
        for state_name in self.states:
            state = self.get_state(state_name)
            state._is_done = False  # noqa
            state.setup()

        self.current_task = None

    def teardown(self) -> None:
        """Implement the teardown."""
        self.context.logger.info("Tearing down Arbitrageabciapp FSM behaviour.")

    def act(self) -> None:
        """Implement the behaviour."""
        if self.current is None:
            self.context.logger.info("No state to act on.")
            self.terminate()
            return

        if self.current_task:
            if not self.current_task.done():
                return
            failed = self.current_task.exception()
            if failed:
                self.context.logger.error(f"Error in state {self.current}: {self.current_task.print_stack()}")
                self.context.logger.info(f"Breaking on error. {self.current} -> errorround")
                self.current_task = None
                self.current = "errorround"
                return
            self.current_task = None

        current_state = self.get_state(self.current)
        if current_state is None:
            return

        # We check if we need to run the state.
        if not current_state.started:
            self.context.logger.debug(f"Starting state {self.current}")
            loop = asyncio.get_event_loop()
            self.current_task = loop.create_task(current_state.act())
            self.current_behaviour = current_state
            self.strategy.state.current_round = str(self.current)

        if current_state.is_done():
            self.context.logger.debug(f"State {self.current} is done.")
            if current_state in self._final_states:
                # we reached a final state - return.
                self.logger.info("Reached a final state.")
                self.current = None
                return
            event = current_state.event
            next_state = self.transitions.get(self.current, {}).get(event, None)
            self.context.logger.debug(
                f"Transitioning from state {self.current} with event {event}. Next state: {next_state}"
            )
            self.current = next_state
            self.strategy.state.last_transition_time = datetime.now(tz=TZ)

    def terminate(self) -> None:
        """Implement the termination."""
        os._exit(0)

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy
