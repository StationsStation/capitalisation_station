# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
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


"""This module contains the tests of the Apprise connection module."""
# pylint: skip-file

import asyncio
from unittest.mock import MagicMock

import pytest
from aea.common import Address
from aea.mail.base import Message, Envelope
from aea.identity.base import Identity
from aea.configurations.base import ConnectionConfig
from aea.protocols.dialogue.base import Dialogue as BaseDialogue

from packages.eightballer.protocols.user_interaction.message import UserInteractionMessage
from packages.eightballer.protocols.user_interaction.dialogues import (
    UserInteractionDialogue,
    BaseUserInteractionDialogues,
)
from packages.eightballer.connections.apprise_wrapper.connection import (
    CONNECTION_ID as CONNECTION_PUBLIC_ID,
    AppriseConnection,
)


def envelope_it(message: UserInteractionMessage):
    """Envelope the message."""

    return Envelope(
        to=message.to,
        sender=message.sender,
        message=message,
    )


class UserInteractionDialogues(BaseUserInteractionDialogues):
    """The dialogues class keeps track of all apprise dialogues."""

    def __init__(self, self_address: Address, **kwargs) -> None:
        """Initialize dialogues."""

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message."""
            del receiver_address, message
            return UserInteractionDialogue.Role.AGENT

        BaseUserInteractionDialogues.__init__(
            self,
            self_address=self_address,
            role_from_first_message=role_from_first_message,
            **kwargs,
        )


class TestAppriseConnection:
    """Test the Apprise connection."""

    def setup(self):
        """Initialise the test case."""

        self.identity = Identity("dummy_name", address="dummy_address", public_key="dummy_public_key")
        self.agent_address = self.identity.address

        self.connection_id = AppriseConnection.connection_id
        self.protocol_id = UserInteractionMessage.protocol_id
        self.target_skill_id = "dummy_author/dummy_skill:0.1.0"

        kwargs = {
            "endpoints": [
                "ntfy://ntfy.sh/1234567890",
            ],
        }

        self.configuration = ConnectionConfig(
            target_skill_id=self.target_skill_id,
            connection_id=AppriseConnection.connection_id,
            restricted_to_protocols={UserInteractionMessage.protocol_id},
            **kwargs,
        )

        self.apprise_connection = AppriseConnection(
            configuration=self.configuration,
            data_dir=MagicMock(),
            identity=self.identity,
        )

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.apprise_connection.connect())
        self.connection_address = str(AppriseConnection.connection_id)
        self._dialogues = UserInteractionDialogues(self.target_skill_id)

    @pytest.mark.asyncio
    async def test_apprise_connection_connect(self):
        """Test the connect."""
        await self.apprise_connection.connect()
        assert not self.apprise_connection.channel.is_stopped

    @pytest.mark.asyncio
    async def test_apprise_connection_disconnect(self):
        """Test the disconnect."""
        await self.apprise_connection.disconnect()
        assert self.apprise_connection.channel.is_stopped

    @pytest.mark.asyncio
    async def test_handles_inbound_query(self):
        """Test the connect."""
        await self.apprise_connection.connect()

        msg, _dialogue = self._dialogues.create(
            counterparty=str(CONNECTION_PUBLIC_ID),
            performative=UserInteractionMessage.Performative.NOTIFICATION,
            title="test title",
            body="test body",
        )

        await self.apprise_connection.send(envelope_it(msg))
