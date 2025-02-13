"""This module contains the classes required for ohlcv dialogue management.

- OhlcvDialogue: The dialogue class maintains state of a dialogue and manages it.
- OhlcvDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.ohlcv.message import OhlcvMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message."""
    del sender, message
    return OhlcvDialogue.Role.AGENT


class OhlcvDialogue(Dialogue):
    """The ohlcv dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset({OhlcvMessage.Performative.SUBSCRIBE})
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {OhlcvMessage.Performative.ERROR, OhlcvMessage.Performative.END}
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        OhlcvMessage.Performative.CANDLESTICK: frozenset({OhlcvMessage.Performative.END}),
        OhlcvMessage.Performative.END: frozenset(),
        OhlcvMessage.Performative.ERROR: frozenset(),
        OhlcvMessage.Performative.HISTORY: frozenset(
            {OhlcvMessage.Performative.CANDLESTICK, OhlcvMessage.Performative.ERROR}
        ),
        OhlcvMessage.Performative.SUBSCRIBE: frozenset(
            {OhlcvMessage.Performative.CANDLESTICK, OhlcvMessage.Performative.ERROR, OhlcvMessage.Performative.END}
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a ohlcv dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a ohlcv dialogue."""

        END = 0
        ERROR = 1

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[OhlcvMessage] = OhlcvMessage,
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


class BaseOhlcvDialogues(Dialogues, ABC):
    """This class keeps track of all ohlcv dialogues."""

    END_STATES = frozenset({OhlcvDialogue.EndState.END, OhlcvDialogue.EndState.ERROR})
    _keep_terminal_state_dialogues = True

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[OhlcvDialogue] = OhlcvDialogue,
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
            message_class=OhlcvMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class OhlcvDialogues(BaseOhlcvDialogues, Model):
    """This class defines the dialogues used in Ohlcv."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseOhlcvDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
