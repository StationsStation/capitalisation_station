"""base Behaviour."""

import datetime
from typing import Any
from collections.abc import Callable, Generator

from aea.mail.base import Message
from aea.skills.behaviours import State

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.skills.simple_fsm.strategy import TZ, ArbitrageStrategy
from packages.eightballer.skills.abstract_round_abci.behaviour_utils import (
    BaseBehaviour as BaseBehaviourUtils,
    TimeoutException,
)


class BaseBehaviour(State):
    """This class implements the PostTradeRound state."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def setup(self) -> None:
        """Setup the state."""
        self._is_done = False  # Initially, the state is not done
        self.started = False

    def is_done(self) -> bool:
        """Return True if the state is done."""
        return self._is_done

    @property
    def event(self) -> str | None:
        """Return the event."""
        return self._event

    async def act(self) -> None:
        """Perform the action of the state."""
        msg = "The act method should be implemented in the derived class."
        raise NotImplementedError(msg)

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy


class BaseConnectionRound(BaseBehaviourUtils):
    """This class implements the BaseConnectionRound state."""

    matching_round = "baseconnectionround"

    def setup(self) -> None:
        """Setup the state."""
        self._performative_to_dialogue_class = {
            OrdersMessage.Performative.GET_ORDERS: self.context.orders_dialogues,
            OrdersMessage.Performative.CREATE_ORDER: self.context.orders_dialogues,
            BalancesMessage.Performative.GET_ALL_BALANCES: self.context.balances_dialogues,
            TickersMessage.Performative.GET_ALL_TICKERS: self.context.tickers_dialogues,
            TickersMessage.Performative.GET_TICKER: self.context.tickers_dialogues,
        }
        self.started = False
        self._is_done = False
        self._message = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._is_done = False  # Initially, the state is not done
        self._message = None

    def is_done(self) -> bool:
        """Return True if the state is done."""
        return self._is_done

    @property
    def current_message(self) -> None:
        """Return the current message."""
        return self._message

    def get_response(
        self,
        protocol_performative: Message.Performative,
        connection_id: str,
        timeout: float = 10.0,
        **kwargs,
    ) -> Generator[None, None, Any]:
        """Get a ccxt response."""

        dialogue_class = self._performative_to_dialogue_class[protocol_performative]

        msg, dialogue = dialogue_class.create(
            counterparty=str(connection_id),
            performative=protocol_performative,
            **kwargs,
        )
        msg._sender = str(self.context.skill_id)  # noqa
        response = yield from self._do_request(msg, dialogue, timeout)
        self._message = None
        return response

    def get_callback_request(self) -> Callable[[Message, "BaseBehaviour"], None]:
        """Wrapper for callback request which depends on whether the message has not been handled on time."""

        def callback_request(message: Message, current_behaviour: BaseBehaviour) -> None:
            """The callback request."""
            self.context.logger.debug(f"Callback request: {message}")
            current_behaviour._message = message  # noqa

        return callback_request

    def wait_for_message(
        self,
        condition: Callable = lambda message: True,  # noqa
        timeout: float | None = None,
    ) -> Any:
        """Wait for message.

        Care must be taken. This method does not handle concurrent requests.
        Use directly after a request is being sent.
        This is a local method that does not depend on the global clock,
        so the usage of datetime.now() is acceptable here.

        """
        if timeout is not None:
            deadline = datetime.datetime.now(tz=TZ) + datetime.timedelta(0, timeout)
        else:
            deadline = datetime.datetime.max

        try:
            while self.current_message is None:
                yield
                if timeout is not None and datetime.datetime.now(tz=TZ) > deadline:
                    raise TimeoutException
            self.context.logger.debug(f"Received message: {self._message}")
            return self.current_message
        except TimeoutException:
            self.context.logger.info("Timeout!")
            return None  # noqa

    @property
    def event(self) -> str | None:
        """Return the event."""
        return self._event

    async def async_act_wrapper(self) -> Generator[Any, None, None]:
        """Wrapper for the async act method."""
        return await self.async_act()

    async def async_act(self) -> None:
        """Perform the action of the state."""
        self.act()
