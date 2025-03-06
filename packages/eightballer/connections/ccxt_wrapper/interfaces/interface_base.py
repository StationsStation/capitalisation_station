"""Base interface class."""

from typing import Any
from collections.abc import Callable

from aea.common import Address
from aea.exceptions import enforce
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues
from aea.configurations.data_types import PublicId


class UnknownPerformatives(Exception):
    """Exception for unknown performatives."""


def get_dialogues(target_dialogues: Dialogues, target_dialogue: Dialogue) -> object:
    """Factory method to generate dialogue classes."""

    class MetaClass(target_dialogues):
        """The dialogues class keeps track of all ccxt dialogues."""

        def __init__(self) -> None:
            """Initialize dialogues."""

            def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
            ) -> Dialogue.Role:
                """Infer the role of the agent from an incoming/outgoing first message.

                Args:
                ----
                message(Message): an incoming/outgoing first message
                receiver_address(Address): the address of the receiving agent
                :return(Role): The role of the agent

                """
                del message, receiver_address  # pragma: nocover
                return target_dialogue.Role.AGENT

            target_dialogues.__init__(
                self,
                self_address="eightballer/ccxt_wrapper:0.1.0",
                role_from_first_message=role_from_first_message,
                dialogue_class=target_dialogue,
            )

    return MetaClass()


class BaseInterface:
    """Base interface class."""

    message_type: Any
    dialogue_class: Any
    dialogues_class: Any
    protocol_id = str(PublicId)
    handlers = {}
    supported_protocols = {}
    _dialogues: Any

    def __init__(self):
        self._dialogues = get_dialogues(self.dialogues_class, self.dialogue_class)

    def get_handler(self, performative: Any) -> Callable[[Any], Any]:
        """Get the handler method, given the message performative.

        Args:
        ----
        performative: the message performative.

        :return(Callable): the method that will send the request.

        """
        handler = getattr(self, performative.value, None)
        if handler is None:
            msg = f"Performative not recognized: {performative.value}"
            raise UnknownPerformatives(msg)
        return handler

    def validate_msg(self, message: Any):
        """Validate the message."""
        performative = message.performative
        dialogue = self._dialogues.update(message)
        # noinspection PyUnresolvedReferences
        enforce(
            all(
                [
                    dialogue is not None and message.protocol_id == self.protocol_id,
                ]
            ),
            f"No dialogue created. Message={message} not valid.",
        )
        return message, dialogue, performative
