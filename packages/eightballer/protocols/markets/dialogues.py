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
This module contains the classes required for markets dialogue management.

- MarketsDialogue: The dialogue class maintains state of a dialogue and manages it.
- MarketsDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, Dict, FrozenSet, Optional, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues
from aea.skills.base import Model

from packages.eightballer.protocols.markets.message import MarketsMessage


class MarketsDialogue(Dialogue):
    """The markets dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            MarketsMessage.Performative.GET_MARKET,
            MarketsMessage.Performative.GET_ALL_MARKETS,
        }
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            MarketsMessage.Performative.ALL_MARKETS,
            MarketsMessage.Performative.MARKET,
            MarketsMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        MarketsMessage.Performative.ALL_MARKETS: frozenset(),
        MarketsMessage.Performative.ERROR: frozenset(),
        MarketsMessage.Performative.GET_ALL_MARKETS: frozenset(
            {MarketsMessage.Performative.ALL_MARKETS, MarketsMessage.Performative.ERROR}
        ),
        MarketsMessage.Performative.GET_MARKET: frozenset(
            {MarketsMessage.Performative.MARKET, MarketsMessage.Performative.ERROR}
        ),
        MarketsMessage.Performative.MARKET: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a markets dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a markets dialogue."""

        MARKET = 0
        ALL_MARKETS = 1
        ERROR = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[MarketsMessage] = MarketsMessage,
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


class BaseMarketsDialogues(Dialogues, ABC):
    """This class keeps track of all markets dialogues."""

    END_STATES = frozenset(
        {
            MarketsDialogue.EndState.MARKET,
            MarketsDialogue.EndState.ALL_MARKETS,
            MarketsDialogue.EndState.ERROR,
        }
    )

    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Optional[Callable[[Message, Address], Dialogue.Role]] = None,
        dialogue_class: Type[MarketsDialogue] = MarketsDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :param dialogue_class: the dialogue class used
        :param role_from_first_message: the callable determining role from first message
        """
        del role_from_first_message

        def _role_from_first_message(message: Message, sender: Address) -> Dialogue.Role:  # pylint:
            """Infer the role of the agent from an incoming/outgoing first message."""
            del sender, message
            return MarketsDialogue.Role.AGENT

        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=MarketsMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=_role_from_first_message,
        )


class MarketsDialogues(BaseMarketsDialogues, Model):
    """Dialogue class for Markets."""

    def __init__(self, **kwargs):
        """Initialize the Dialogue."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseMarketsDialogues.__init__(self, self_address=str(self.context.skill_id))
