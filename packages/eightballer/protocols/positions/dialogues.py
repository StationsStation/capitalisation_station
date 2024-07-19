# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""
This module contains the classes required for positions dialogue management.

- PositionsDialogue: The dialogue class maintains state of a dialogue and manages it.
- PositionsDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, Dict, FrozenSet, Optional, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues
from aea.skills.base import Model

from packages.eightballer.protocols.positions.message import PositionsMessage


class PositionsDialogue(Dialogue):
    """The positions dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            PositionsMessage.Performative.GET_ALL_POSITIONS,
            PositionsMessage.Performative.GET_POSITION,
        }
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            PositionsMessage.Performative.POSITION,
            PositionsMessage.Performative.ALL_POSITIONS,
            PositionsMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        PositionsMessage.Performative.ALL_POSITIONS: frozenset(),
        PositionsMessage.Performative.ERROR: frozenset(),
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
        message_class: Type[PositionsMessage] = PositionsMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :param message_class: the message class used
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
        role_from_first_message: Optional[
            Callable[[Message, Address], Dialogue.Role]
        ] = None,
        dialogue_class: Type[PositionsDialogue] = PositionsDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :param dialogue_class: the dialogue class used
        :param role_from_first_message: the callable determining role from first message
        """
        del role_from_first_message

        def _role_from_first_message(
            message: Message, sender: Address
        ) -> Dialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message."""
            del sender, message
            return PositionsDialogue.Role.AGENT

        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=PositionsMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=_role_from_first_message,
        )


class PositionsDialogues(BasePositionsDialogues, Model):
    """Dialogue class"""

    def __init__(self, **kwargs):
        """Initialize the dialogue class"""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BasePositionsDialogues.__init__(self, self_address=str(self.context.skill_id))
