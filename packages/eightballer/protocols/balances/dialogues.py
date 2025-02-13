"""This module contains the classes required for balances dialogue management.

- BalancesDialogue: The dialogue class maintains state of a dialogue and manages it.
- BalancesDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.balances.message import BalancesMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message."""
    del sender, message
    return BalancesDialogue.Role.AGENT


class BalancesDialogue(Dialogue):
    """The balances dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {BalancesMessage.Performative.GET_ALL_BALANCES, BalancesMessage.Performative.GET_BALANCE}
    )
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            BalancesMessage.Performative.BALANCE,
            BalancesMessage.Performative.ALL_BALANCES,
            BalancesMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        BalancesMessage.Performative.ALL_BALANCES: frozenset(),
        BalancesMessage.Performative.BALANCE: frozenset(),
        BalancesMessage.Performative.ERROR: frozenset(),
        BalancesMessage.Performative.GET_ALL_BALANCES: frozenset(
            {BalancesMessage.Performative.ALL_BALANCES, BalancesMessage.Performative.ERROR}
        ),
        BalancesMessage.Performative.GET_BALANCE: frozenset(
            {BalancesMessage.Performative.BALANCE, BalancesMessage.Performative.ERROR}
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a balances dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a balances dialogue."""

        BALANCE = 0
        ALL_BALANCES = 1
        ERROR = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[BalancesMessage] = BalancesMessage,
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


class BaseBalancesDialogues(Dialogues, ABC):
    """This class keeps track of all balances dialogues."""

    END_STATES = frozenset(
        {BalancesDialogue.EndState.BALANCE, BalancesDialogue.EndState.ALL_BALANCES, BalancesDialogue.EndState.ERROR}
    )
    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[BalancesDialogue] = BalancesDialogue,
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
            message_class=BalancesMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class BalancesDialogues(BaseBalancesDialogues, Model):
    """This class defines the dialogues used in Balances."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseBalancesDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
