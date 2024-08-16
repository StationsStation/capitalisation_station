# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 eightballer
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
This module contains the classes required for spot_asset dialogue management.

- SpotAssetDialogue: The dialogue class maintains state of a dialogue and manages it.
- SpotAssetDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Dict, Type, Callable, FrozenSet, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.spot_asset.message import SpotAssetMessage


class SpotAssetDialogue(Dialogue):
    """The spot_asset dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            SpotAssetMessage.Performative.GET_SPOT_ASSET,
            SpotAssetMessage.Performative.GET_SPOT_ASSETS,
        }
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            SpotAssetMessage.Performative.SPOT_ASSET,
            SpotAssetMessage.Performative.END,
            SpotAssetMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        SpotAssetMessage.Performative.END: frozenset(),
        SpotAssetMessage.Performative.ERROR: frozenset(),
        SpotAssetMessage.Performative.GET_SPOT_ASSET: frozenset(
            {
                SpotAssetMessage.Performative.SPOT_ASSET,
                SpotAssetMessage.Performative.ERROR,
            }
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
        message_class: Type[SpotAssetMessage] = SpotAssetMessage,
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


class SpotAssetDialogues(Dialogues, ABC):
    """This class keeps track of all spot_asset dialogues."""

    END_STATES = frozenset(
        {
            SpotAssetDialogue.EndState.END,
            SpotAssetDialogue.EndState.ERROR,
            SpotAssetDialogue.EndState.SPOT_ASSET,
        }
    )

    _keep_terminal_state_dialogues = True

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[SpotAssetDialogue] = SpotAssetDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :param dialogue_class: the dialogue class used
        :param role_from_first_message: the callable determining role from first message
        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=SpotAssetMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )
