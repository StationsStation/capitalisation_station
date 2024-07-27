"""
Dialogs for the application.
"""

from typing import Any

from aea.protocols.base import Address, Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue
from aea.skills.base import Model

from packages.eightballer.protocols.orders.dialogues import OrdersDialogue as BaseOrdersDialogue
from packages.eightballer.protocols.orders.dialogues import OrdersDialogues as BaseOrdersDialogues
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue as BasePositionsDialogue
from packages.eightballer.protocols.positions.dialogues import PositionsDialogues as BasePositionsDialogues
from packages.valory.protocols.http.dialogues import HttpDialogue as BaseHttpDialogue
from packages.valory.protocols.http.dialogues import HttpDialogues as BaseHttpDialogues

HttpDialogue = BaseHttpDialogue


class HttpDialogues(Model, BaseHttpDialogues):
    """This class keeps track of all http dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.

        :param kwargs: keyword arguments
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
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
