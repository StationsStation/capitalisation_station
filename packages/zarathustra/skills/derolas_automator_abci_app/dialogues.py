# ------------------------------------------------------------------------------
#
#   Copyright 2025 zarathustra
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

"""This module contains the classes required for dialogue management.

- DefaultDialogue: The dialogue class maintains state of a dialogue of type default and manages it.
- DefaultDialogues: The dialogues class keeps track of all dialogues of type default.
- HttpDialogue: The dialogue class maintains state of a dialogue of type http and manages it.
- HttpDialogues: The dialogues class keeps track of all dialogues of type http.
"""

from typing import Any

from aea.skills.base import Model
from aea.protocols.base import Address, Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue

from packages.eightballer.protocols.http.dialogues import (
    HttpDialogue as BaseHttpDialogue,
    HttpDialogues as BaseHttpDialogues,
)
from packages.valory.protocols.ledger_api.dialogues import (
    LedgerApiDialogue as BaseLedgerApiDialogue,
    LedgerApiDialogues as BaseLedgerApiDialogues,
)
from packages.eightballer.protocols.default.dialogues import (
    DefaultDialogue as BaseDefaultDialogue,
    DefaultDialogues as BaseDefaultDialogues,
)
from packages.valory.protocols.contract_api.dialogues import (
    ContractApiDialogue as BaseContractApiDialogue,
    ContractApiDialogues as BaseContractApiDialogues,
)


DefaultDialogue = BaseDefaultDialogue
DefaultDialogues = BaseDefaultDialogues


HttpDialogue = BaseHttpDialogue
HttpDialogues = BaseHttpDialogues

LedgerApiDialogue = BaseLedgerApiDialogue


class LedgerApiDialogues(Model, BaseLedgerApiDialogues):
    """This class keeps track of all ledger api dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize dialogues."""
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message."""
            del receiver_address, message
            return BaseLedgerApiDialogue.Role.AGENT

        BaseLedgerApiDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
        )


ContractApiDialogue = BaseContractApiDialogue


class ContractApiDialogues(Model, BaseContractApiDialogues):
    """This class keeps track of all contact api dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize dialogues."""
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message."""
            del receiver_address, message
            return BaseContractApiDialogue.Role.AGENT

        BaseContractApiDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
        )
