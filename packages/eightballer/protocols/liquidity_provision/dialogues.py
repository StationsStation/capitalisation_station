"""This module contains the classes required for liquidity_provision dialogue management.

- LiquidityProvisionDialogue: The dialogue class maintains state of a dialogue and manages it.
- LiquidityProvisionDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.liquidity_provision.message import LiquidityProvisionMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message."""
    del sender, message
    return LiquidityProvisionDialogue.Role.LIQUIDITY_PROVIDER


class LiquidityProvisionDialogue(Dialogue):
    """The liquidity_provision dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            LiquidityProvisionMessage.Performative.ADD_LIQUIDITY,
            LiquidityProvisionMessage.Performative.REMOVE_LIQUIDITY,
            LiquidityProvisionMessage.Performative.QUERY_LIQUIDITY,
        }
    )
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            LiquidityProvisionMessage.Performative.LIQUIDITY_ADDED,
            LiquidityProvisionMessage.Performative.LIQUIDITY_REMOVED,
            LiquidityProvisionMessage.Performative.LIQUIDITY_STATUS,
            LiquidityProvisionMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        LiquidityProvisionMessage.Performative.ADD_LIQUIDITY: frozenset(
            {LiquidityProvisionMessage.Performative.LIQUIDITY_ADDED, LiquidityProvisionMessage.Performative.ERROR}
        ),
        LiquidityProvisionMessage.Performative.ERROR: frozenset(),
        LiquidityProvisionMessage.Performative.LIQUIDITY_ADDED: frozenset(),
        LiquidityProvisionMessage.Performative.LIQUIDITY_REMOVED: frozenset(),
        LiquidityProvisionMessage.Performative.LIQUIDITY_STATUS: frozenset(),
        LiquidityProvisionMessage.Performative.QUERY_LIQUIDITY: frozenset(
            {LiquidityProvisionMessage.Performative.LIQUIDITY_STATUS, LiquidityProvisionMessage.Performative.ERROR}
        ),
        LiquidityProvisionMessage.Performative.REMOVE_LIQUIDITY: frozenset(
            {LiquidityProvisionMessage.Performative.LIQUIDITY_REMOVED, LiquidityProvisionMessage.Performative.ERROR}
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a liquidity_provision dialogue."""

        LIQUIDITY_PROVIDER = "liquidity_provider"
        LIQUIDITY_SEEKER = "liquidity_seeker"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a liquidity_provision dialogue."""

        LIQUIDITY_ADDED = 0
        LIQUIDITY_REMOVED = 1
        LIQUIDITY_STATUS = 2
        ERROR = 3

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[LiquidityProvisionMessage] = LiquidityProvisionMessage,
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


class BaseLiquidityProvisionDialogues(Dialogues, ABC):
    """This class keeps track of all liquidity_provision dialogues."""

    END_STATES = frozenset(
        {
            LiquidityProvisionDialogue.EndState.LIQUIDITY_ADDED,
            LiquidityProvisionDialogue.EndState.LIQUIDITY_REMOVED,
            LiquidityProvisionDialogue.EndState.LIQUIDITY_STATUS,
            LiquidityProvisionDialogue.EndState.ERROR,
        }
    )
    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[LiquidityProvisionDialogue] = LiquidityProvisionDialogue,
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
            message_class=LiquidityProvisionMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class LiquidityProvisionDialogues(BaseLiquidityProvisionDialogues, Model):
    """This class defines the dialogues used in Liquidity_provision."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseLiquidityProvisionDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
