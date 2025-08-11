"""This module contains the classes required for approvals dialogue management.

- ApprovalsDialogue: The dialogue class maintains state of a dialogue and manages it.
- ApprovalsDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.approvals.message import ApprovalsMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message."""
    del sender, message
    return ApprovalsDialogue.Role.AGENT


class ApprovalsDialogue(Dialogue):
    """The approvals dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {ApprovalsMessage.Performative.SET_APPROVAL, ApprovalsMessage.Performative.GET_APPROVAL}
    )
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {ApprovalsMessage.Performative.APPROVAL_RESPONSE, ApprovalsMessage.Performative.ERROR}
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        ApprovalsMessage.Performative.APPROVAL_RESPONSE: frozenset(),
        ApprovalsMessage.Performative.ERROR: frozenset(),
        ApprovalsMessage.Performative.GET_APPROVAL: frozenset(
            {ApprovalsMessage.Performative.APPROVAL_RESPONSE, ApprovalsMessage.Performative.ERROR}
        ),
        ApprovalsMessage.Performative.SET_APPROVAL: frozenset(
            {ApprovalsMessage.Performative.APPROVAL_RESPONSE, ApprovalsMessage.Performative.ERROR}
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a approvals dialogue."""

        AGENT = "agent"
        LEDGER = "ledger"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a approvals dialogue."""

        APPROVAL_RESPONSE = 0
        ERROR = 1

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[ApprovalsMessage] = ApprovalsMessage,
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


class BaseApprovalsDialogues(Dialogues, ABC):
    """This class keeps track of all approvals dialogues."""

    END_STATES = frozenset({ApprovalsDialogue.EndState.APPROVAL_RESPONSE, ApprovalsDialogue.EndState.ERROR})
    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[ApprovalsDialogue] = ApprovalsDialogue,
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
            message_class=ApprovalsMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class ApprovalsDialogues(BaseApprovalsDialogues, Model):
    """This class defines the dialogues used in Approvals."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseApprovalsDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
