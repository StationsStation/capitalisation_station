"""base Behaviour."""

import datetime
from time import time
from typing import Any
from collections.abc import Callable, Generator

from aea.mail.base import Message
from aea.skills.behaviours import State
from aea.configurations.base import PublicId
from aea.protocols.dialogue.base import Dialogue as BaseDialogue

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.skills.simple_fsm.strategy import TZ, ArbitrageStrategy
from packages.eightballer.protocols.approvals.message import ApprovalsMessage
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.eightballer.skills.abstract_round_abci.behaviour_utils import (
    BaseBehaviour as BaseBehaviourUtils,
)


class BaseBehaviour(State):
    """This class implements the PostTradeRound state."""

    supported_protocols: dict[PublicId, list] = {}

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

    async def async_act(self) -> None:
        """Perform the action of the state."""
        msg = "The act method should be implemented in the derived class."
        raise NotImplementedError(msg)

    def act(self) -> None:
        """Perform the action of the state."""
        msg = "The act method should be implemented in the derived class."
        raise NotImplementedError(msg)

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy


class BaseConnectionRound(BaseBehaviourUtils, State):
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
            ApprovalsMessage.Performative.SET_APPROVAL: self.context.approvals_dialogues,
            AssetBridgingMessage.Performative.REQUEST_BRIDGE: self.context.asset_bridging_dialogues,
            AssetBridgingMessage.Performative.REQUEST_STATUS: self.context.asset_bridging_dialogues,
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
        self._dialogue_to_response_msgs = {dialogue.dialogue_label.dialogue_starter_reference: None}
        response = yield from self._do_request(msg, dialogue, timeout)
        return response

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

    def non_blocking_sleep(self, duration):
        """Sleep for a given duration without blocking the event loop."""
        end_time = time() + duration
        while time() < end_time:
            yield  # yield control back to the framework

    def submit_msg(
        self,
        protocol_performative: Message.Performative,
        connection_id: str,
        timeout: float = 10.0,
        **kwargs,
    ) -> BaseDialogue:
        """Get a ccxt response."""

        dialogue_class: BaseDialogue = self._performative_to_dialogue_class[protocol_performative]

        msg, dialogue = dialogue_class.create(
            counterparty=str(connection_id),
            performative=protocol_performative,
            **kwargs,
        )
        dialogue.deadline = datetime.datetime.now(tz=TZ) + datetime.timedelta(0, timeout)
        msg._sender = str(self.context.skill_id)  # noqa

        request_nonce = self._get_request_nonce_from_dialogue(dialogue)
        self.context.requests.request_id_to_callback[request_nonce] = self.get_dialogue_callback_request()
        self.context.outbox.put_message(message=msg)
        return dialogue

    def get_dialogue_callback_request(self) -> Callable[[Message, "BaseBehaviour"], None]:
        """Wrapper for callback request which depends on whether the message has not been handled on time."""

        def callback_request(message: Message, dialogue: BaseDialogue, behaviour: BaseBehaviour) -> None:
            """The callback request."""
            if message.protocol_id in self.supported_protocols:
                self.context.logger.debug(f"Message: {message} {dialogue}: {behaviour}")
                self.supported_protocols.get(message.protocol_id).append(message)
                return
            self.context.logger.error(
                f"Message not supported: {message.protocol_id}. Supported protocols: {self.supported_protocols}"
            )

        return callback_request
