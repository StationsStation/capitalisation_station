# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
#   Copyright 2018-2021 Fetch.AI Limited
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
"""This module contains the tests of the HTTP Server connection module."""

# pylint: disable=W0201
import os
import logging
from unittest.mock import MagicMock

import pytest
from aea.common import Address
from async_timeout import timeout
from aea.identity.base import Identity
from aea.protocols.base import Message
from aea.configurations.base import ConnectionConfig
from aea.protocols.dialogue.base import Dialogue, Dialogues

from packages.eightballer.connections.ccxt_wrapper.connection import CcxtConnection


logger = logging.getLogger(__name__)

DEFAULT_EXCHANGE_ID = "deribit"


default_test_exchanges = [
    {
        "name": DEFAULT_EXCHANGE_ID,
        "api_key": os.environ.get("API_KEY"),
        "api_secret": os.environ.get("API_SECRET"),
        "sub_account": os.environ.get("API_SUB_ACCOUNT"),
    }
]


def with_timeout(t):
    """Return the."""

    def wrapper(corofunc):
        async def run(*args, **kwargs):
            with timeout(t):
                return await corofunc(*args, **kwargs)

        return run

    return wrapper


def get_dialogues(target_dialogues: type[Dialogues], target_dialogue: type[Dialogue]) -> object:
    """Factory method to generate dialogue classes."""

    class MetaClass(target_dialogues):
        """The dialogues class keeps track of all ccxt dialogues."""

        def __init__(self, address: type[Address]) -> None:
            """Initialize dialogues."""
            self._address = address

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
                del receiver_address, message  # pragma: nocover
                return target_dialogue.Role.AGENT

            target_dialogues.__init__(
                self,
                self_address=str(self._address),
                role_from_first_message=role_from_first_message,
                dialogue_class=target_dialogue,
            )

    return MetaClass


class BaseCcxtConnectionTest:
    """Tests the http client connection's 'connect' functionality."""

    connection: CcxtConnection
    client_skill_id: str
    agent_identity: Identity

    def setup(self) -> None:
        """Initialise the class."""
        self.client_skill_id = "some/skill:0.1.0"
        self.agent_identity = Identity("name", address="some string", public_key="some public_key")
        configuration = ConnectionConfig(
            target_skill_id=self.client_skill_id,
            exchanges=default_test_exchanges,
            connection_id=CcxtConnection.connection_id,
        )
        self.connection = CcxtConnection(
            configuration=configuration,
            data_dir=MagicMock(),
            identity=self.agent_identity,
        )


@pytest.mark.asyncio
class TestCcxtConnection(BaseCcxtConnectionTest):
    """Tests the ccxt connection."""

    async def test_all_protocols_supported(self):
        """Test if all protocols are supported."""

    async def test_connects(self):
        """Test if all protocols are supported."""
        await self.connection.connect()

    async def test_multiple_exchanges(self):
        """Test can start multiple exchanges."""

    async def test_custom_exchanges(self):
        """Test can start custom class."""
