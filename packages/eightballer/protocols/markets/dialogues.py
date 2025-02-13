"""This module contains the classes required for markets dialogue management.

- MarketsDialogue: The dialogue class maintains state of a dialogue and manages it.
- MarketsDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.markets.message import MarketsMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message."""
    del sender, message
    return MarketsDialogue.Role.AGENT


class MarketsDialogue(Dialogue):
    """The markets dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset({MarketsMessage.Performative.GET_ALL_MARKETS})
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {MarketsMessage.Performative.ALL_MARKETS, MarketsMessage.Performative.MARKET, MarketsMessage.Performative.ERROR}
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        MarketsMessage.Performative.ALL_MARKETS: frozenset(),
        MarketsMessage.Performative.ERROR: frozenset(),
        MarketsMessage.Performative.GET_ALL_MARKETS: frozenset(
            {MarketsMessage.Performative.ALL_MARKETS, MarketsMessage.Performative.ERROR}
        ),
        MarketsMessage.Performative.GET_MARKET: frozenset(
            {MarketsMessage.Performative.MARKET, MarketsMessage.Performative.ERROR}
        ),
        MarketsMessage.Performative.MARKET: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a markets dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a markets dialogue."""

        MARKET = 0
        ALL_MARKETS = 1
        ERROR = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[MarketsMessage] = MarketsMessage,
    ) -> None:
        """Initialize a dialogue.



        Args:
        ----
               dialogue_label:  the identifier of the dialogue
               self_address:  the address of the entity for whom this dialogue is maintained
               role:  the role of the agent this dialogue is maintained for
               message_class:  the message class used

        """
        Dialogue.__init__(
            self, dialogue_label=dialogue_label, message_class=message_class, self_address=self_address, role=role
        )


class BaseMarketsDialogues(Dialogues, ABC):
    """This class keeps track of all markets dialogues."""

    END_STATES = frozenset(
        {MarketsDialogue.EndState.MARKET, MarketsDialogue.EndState.ALL_MARKETS, MarketsDialogue.EndState.ERROR}
    )
    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[MarketsDialogue] = MarketsDialogue,
    ) -> None:
        """Initialize dialogues.



        Args:
        ----
               self_address:  the address of the entity for whom dialogues are maintained
               dialogue_class:  the dialogue class used
               role_from_first_message:  the callable determining role from first message

        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(frozenset[Dialogue.EndState], self.END_STATES),
            message_class=MarketsMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class MarketsDialogues(BaseMarketsDialogues, Model):
    """This class defines the dialogues used in Markets."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseMarketsDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
