"""This module contains the classes required for orders dialogue management.

- OrdersDialogue: The dialogue class maintains state of a dialogue and manages it.
- OrdersDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.orders.message import OrdersMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message."""
    del sender, message
    return OrdersDialogue.Role.AGENT


class OrdersDialogue(Dialogue):
    """The orders dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            OrdersMessage.Performative.CREATE_ORDER,
            OrdersMessage.Performative.CANCEL_ORDER,
            OrdersMessage.Performative.GET_ORDER,
            OrdersMessage.Performative.GET_ORDERS,
            OrdersMessage.Performative.GET_SETTLEMENTS,
        }
    )
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            OrdersMessage.Performative.ERROR,
            OrdersMessage.Performative.ORDER,
            OrdersMessage.Performative.ORDERS,
            OrdersMessage.Performative.ORDER_CREATED,
            OrdersMessage.Performative.ORDER_CANCELLED,
        }
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        OrdersMessage.Performative.CANCEL_ORDER: frozenset(
            {OrdersMessage.Performative.ORDER_CANCELLED, OrdersMessage.Performative.ERROR}
        ),
        OrdersMessage.Performative.CREATE_ORDER: frozenset(
            {OrdersMessage.Performative.ORDER_CREATED, OrdersMessage.Performative.ERROR}
        ),
        OrdersMessage.Performative.ERROR: frozenset(),
        OrdersMessage.Performative.GET_ORDER: frozenset(
            {OrdersMessage.Performative.ORDER, OrdersMessage.Performative.ERROR}
        ),
        OrdersMessage.Performative.GET_ORDERS: frozenset(
            {OrdersMessage.Performative.ORDERS, OrdersMessage.Performative.ERROR}
        ),
        OrdersMessage.Performative.GET_SETTLEMENTS: frozenset(
            {OrdersMessage.Performative.ORDERS, OrdersMessage.Performative.ERROR}
        ),
        OrdersMessage.Performative.ORDER: frozenset(),
        OrdersMessage.Performative.ORDER_CANCELLED: frozenset(),
        OrdersMessage.Performative.ORDER_CREATED: frozenset(),
        OrdersMessage.Performative.ORDERS: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a orders dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a orders dialogue."""

        ERROR = 0

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[OrdersMessage] = OrdersMessage,
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


class BaseOrdersDialogues(Dialogues, ABC):
    """This class keeps track of all orders dialogues."""

    END_STATES = frozenset({OrdersDialogue.EndState.ERROR})
    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[OrdersDialogue] = OrdersDialogue,
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
            message_class=OrdersMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class OrdersDialogues(BaseOrdersDialogues, Model):
    """This class defines the dialogues used in Orders."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseOrdersDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
