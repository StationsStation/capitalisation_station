# Auto-generated by tool

"""This module contains the classes required for positions dialogue management.

- PositionsDialogue: The dialogue class maintains state of a dialogue and manages it.
- PositionsDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.positions.message import PositionsMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:  # noqa: ARG001
    """Infer the role of the agent from an incoming/outgoing first message."""
    return PositionsDialogue.Role.AGENT


class PositionsDialogue(Dialogue):
    """The positions dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            PositionsMessage.Performative.GET_ALL_POSITIONS,
            PositionsMessage.Performative.GET_POSITION,
        }
    )
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            PositionsMessage.Performative.POSITION,
            PositionsMessage.Performative.ALL_POSITIONS,
            PositionsMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        PositionsMessage.Performative.GET_ALL_POSITIONS: frozenset(
            {
                PositionsMessage.Performative.ALL_POSITIONS,
                PositionsMessage.Performative.ERROR,
            }
        ),
        PositionsMessage.Performative.GET_POSITION: frozenset(
            {
                PositionsMessage.Performative.POSITION,
                PositionsMessage.Performative.ERROR,
            }
        ),
        PositionsMessage.Performative.POSITION: frozenset(),
        PositionsMessage.Performative.ALL_POSITIONS: frozenset(),
        PositionsMessage.Performative.ERROR: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a positions dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a positions dialogue."""

        POSITION = 0
        ALL_POSITIONS = 1
        ERROR = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[PositionsMessage] = PositionsMessage,
    ) -> None:
        """Initialize a dialogue.

        Args:
        ----
            dialogue_label: the identifier of the dialogue
            self_address: the address of the entity for whom this dialogue is maintained
            role: the role of the agent this dialogue is maintained for
            message_class: the message class used

        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            self_address=self_address,
            role=role,
        )


class BasePositionsDialogues(Dialogues, ABC):
    """This class keeps track of all positions dialogues."""

    END_STATES = frozenset(
        {
            PositionsDialogue.EndState.POSITION,
            PositionsDialogue.EndState.ALL_POSITIONS,
            PositionsDialogue.EndState.ERROR,
        }
    )
    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[PositionsDialogue] = PositionsDialogue,
    ) -> None:
        """Initialize dialogues.

        Args:
        ----
            self_address: the address of the entity for whom dialogues are maintained
            dialogue_class: the dialogue class used
            role_from_first_message: the callable determining role from first message

        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(frozenset[Dialogue.EndState], self.END_STATES),
            message_class=PositionsMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class PositionsDialogues(BasePositionsDialogues, Model):
    """This class defines the dialogues used in positions."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BasePositionsDialogues.__init__(
            self,
            self_address=str(self.context.skill_id),
            role_from_first_message=_role_from_first_message,
        )
