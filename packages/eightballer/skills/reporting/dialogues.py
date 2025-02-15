"""Dialogs for the application."""

from typing import Any

from aea.skills.base import Model
from aea.protocols.base import Address, Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue

from packages.valory.protocols.http.dialogues import (
    HttpDialogue as BaseHttpDialogue,
    HttpDialogues as BaseHttpDialogues,
)
from packages.eightballer.protocols.orders.dialogues import (
    OrdersDialogue as BaseOrdersDialogue,
    OrdersDialogues as BaseOrdersDialogues,
)
from packages.eightballer.protocols.positions.dialogues import (
    PositionsDialogue as BasePositionsDialogue,
    PositionsDialogues as BasePositionsDialogues,
)


HttpDialogue = BaseHttpDialogue


class HttpDialogues(Model, BaseHttpDialogues):
    """This class keeps track of all http dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize dialogues."""
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message."""
            del receiver_address, message
            return BaseHttpDialogue.Role.CLIENT

        BaseHttpDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
        )


OrdersDialogue = BaseOrdersDialogue
OrdersDialogues = BaseOrdersDialogues

PositionsDialogue = BasePositionsDialogue
PositionsDialogues = BasePositionsDialogues
