"""This module contains the classes required for spot_asset dialogue management.

- SpotAssetDialogue: The dialogue class maintains state of a dialogue and manages it.
- SpotAssetDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import cast
from collections.abc import Callable

from aea.common import Address
from aea.skills.base import Model
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.spot_asset.message import SpotAssetMessage


def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:
    """Infer the role of the agent from an incoming/outgoing first message."""
    del sender, message
    return SpotAssetDialogue.Role.AGENT


class SpotAssetDialogue(Dialogue):
    """The spot_asset dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {SpotAssetMessage.Performative.GET_SPOT_ASSET, SpotAssetMessage.Performative.GET_SPOT_ASSETS}
    )
    TERMINAL_PERFORMATIVES: frozenset[Message.Performative] = frozenset(
        {
            SpotAssetMessage.Performative.SPOT_ASSET,
            SpotAssetMessage.Performative.END,
            SpotAssetMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: dict[Message.Performative, frozenset[Message.Performative]] = {
        SpotAssetMessage.Performative.END: frozenset(),
        SpotAssetMessage.Performative.ERROR: frozenset(),
        SpotAssetMessage.Performative.GET_SPOT_ASSET: frozenset(
            {SpotAssetMessage.Performative.SPOT_ASSET, SpotAssetMessage.Performative.ERROR}
        ),
        SpotAssetMessage.Performative.GET_SPOT_ASSETS: frozenset(
            {
                SpotAssetMessage.Performative.SPOT_ASSET,
                SpotAssetMessage.Performative.ERROR,
                SpotAssetMessage.Performative.END,
            }
        ),
        SpotAssetMessage.Performative.SPOT_ASSET: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a spot_asset dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a spot_asset dialogue."""

        END = 0
        ERROR = 1
        SPOT_ASSET = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: type[SpotAssetMessage] = SpotAssetMessage,
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


class BaseSpotAssetDialogues(Dialogues, ABC):
    """This class keeps track of all spot_asset dialogues."""

    END_STATES = frozenset(
        {SpotAssetDialogue.EndState.END, SpotAssetDialogue.EndState.ERROR, SpotAssetDialogue.EndState.SPOT_ASSET}
    )
    _keep_terminal_state_dialogues = True

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role] = _role_from_first_message,
        dialogue_class: type[SpotAssetDialogue] = SpotAssetDialogue,
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
            message_class=SpotAssetMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class SpotAssetDialogues(BaseSpotAssetDialogues, Model):
    """This class defines the dialogues used in Spot_asset."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseSpotAssetDialogues.__init__(
            self, self_address=str(self.context.skill_id), role_from_first_message=_role_from_first_message
        )
