"""
This module contains the classes required for tickers dialogue management.

- TickersDialogue: The dialogue class maintains state of a dialogue and manages it.
- TickersDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Dict, Type, Callable, FrozenSet, cast

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel
from packages.eightballer.protocols.tickers.message import TickersMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message"""
    del sender, message
    return TickersDialogue.Role.AGENT


class TickersDialogue(Dialogue):
    """The tickers dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {TickersMessage.Performative.GET_ALL_TICKERS, TickersMessage.Performative.GET_TICKER}
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {TickersMessage.Performative.TICKER, TickersMessage.Performative.ALL_TICKERS, TickersMessage.Performative.ERROR}
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        TickersMessage.Performative.ALL_TICKERS: frozenset(),
        TickersMessage.Performative.ERROR: frozenset(),
        TickersMessage.Performative.GET_ALL_TICKERS: frozenset(
            {TickersMessage.Performative.ALL_TICKERS, TickersMessage.Performative.ERROR}
        ),
        TickersMessage.Performative.GET_TICKER: frozenset(
            {TickersMessage.Performative.TICKER, TickersMessage.Performative.ERROR}
        ),
        TickersMessage.Performative.TICKER: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a tickers dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a tickers dialogue."""

        TICKER = 0
        ALL_TICKERS = 1
        ERROR = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[TickersMessage] = TickersMessage,
    ) -> None:
        """
        Initialize a dialogue.



        Args:
               dialogue_label:  the identifier of the dialogue
               self_address:  the address of the entity for whom this dialogue is maintained
               role:  the role of the agent this dialogue is maintained for
               message_class:  the message class used

        """
        Dialogue.__init__(
            self, dialogue_label=dialogue_label, message_class=message_class, self_address=self_address, role=role
        )


class BaseTickersDialogues(Dialogues, ABC):
    """This class keeps track of all tickers dialogues."""

    END_STATES = frozenset(
        {TickersDialogue.EndState.TICKER, TickersDialogue.EndState.ALL_TICKERS, TickersDialogue.EndState.ERROR}
    )
    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: Type[TickersDialogue] = TickersDialogue,
    ) -> None:
        """
        Initialize dialogues.



        Args:
               self_address:  the address of the entity for whom dialogues are maintained
               dialogue_class:  the dialogue class used
               role_from_first_message:  the callable determining role from first message

        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=TickersMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class TickersDialogues(BaseTickersDialogues, Model):
    """This class defines the dialogues used in Tickers."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseTickersDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
