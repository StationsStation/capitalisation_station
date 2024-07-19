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
This module contains the classes required for balances dialogue management.

- BalancesDialogue: The dialogue class maintains state of a dialogue and manages it.
- BalancesDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, Dict, FrozenSet, Optional, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues
from aea.skills.base import Model

from packages.eightballer.protocols.balances.message import BalancesMessage


class BalancesDialogue(Dialogue):
    """The balances dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            BalancesMessage.Performative.GET_ALL_BALANCES,
            BalancesMessage.Performative.GET_BALANCE,
        }
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            BalancesMessage.Performative.BALANCE,
            BalancesMessage.Performative.ALL_BALANCES,
            BalancesMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        BalancesMessage.Performative.ALL_BALANCES: frozenset(),
        BalancesMessage.Performative.BALANCE: frozenset(),
        BalancesMessage.Performative.ERROR: frozenset(),
        BalancesMessage.Performative.GET_ALL_BALANCES: frozenset(
            {
                BalancesMessage.Performative.ALL_BALANCES,
                BalancesMessage.Performative.ERROR,
            }
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
        message_class: Type[BalancesMessage] = BalancesMessage,
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


class BaseBalancesDialogues(Dialogues, ABC):
    """This class keeps track of all balances dialogues."""

    END_STATES = frozenset(
        {
            BalancesDialogue.EndState.BALANCE,
            BalancesDialogue.EndState.ALL_BALANCES,
            BalancesDialogue.EndState.ERROR,
        }
    )

    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Optional[
            Callable[[Message, Address], Dialogue.Role]
        ] = None,
        dialogue_class: Type[BalancesDialogue] = BalancesDialogue,
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
            return BalancesDialogue.Role.AGENT

        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=BalancesMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=_role_from_first_message,
        )


class BalancesDialogues(BaseBalancesDialogues, Model):
    """This class keeps track of all balances dialogues."""

    def __init__(self, **kwargs):
        """Initialize dialogues."""
        Model.__init__(self, keep_terminal_state_dialogues=False, **kwargs)
        BaseBalancesDialogues.__init__(self, self_address=str(self.context.skill_id))
