# -*- coding: utf-8 -*-
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
import logging
import os
from typing import Type
from unittest.mock import MagicMock

import pytest
from aea.common import Address
from aea.configurations.base import ConnectionConfig
from aea.identity.base import Identity
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues
from async_timeout import timeout

from packages.eightballer.connections.dcxt.connection import DcxtConnection

logger = logging.getLogger(__name__)

DEFAULT_EXCHANGE_ID = "balancer"

ROOT_DIR = os.path.join(
    os.path.dirname(__file__),
)

TEST_KEY_PATH = os.path.join(ROOT_DIR, "data", "key")

TEST_WALLET = "0x3A5c777edf22107d7FdFB3B02B0Cdfe8b75f3453"
TEST_PRIVATE_KEY = "0xc14f53ee466dd3fc5fa356897ab276acbef4f020486ec253a23b0d1c3f89d4f4"


TEST_EXCHANGES = [
    {
        "name": DEFAULT_EXCHANGE_ID,
        "environment": "test",
        "kwargs": {
            "chain_id": 'mainnet',
            "rpc_url": "https://rpc.ankr.com/eth",
            "etherscan_api_key": "YOUR_ETHERSCAN_API_KEY",
        },
        "key_path": TEST_KEY_PATH,
        "wallet": TEST_WALLET,
    },
]


def with_timeout(t):
    """Return the"""

    def wrapper(corofunc):
        async def run(*args, **kwargs):
            with timeout(t):
                return await corofunc(*args, **kwargs)

        return run

    return wrapper


def get_dialogues(target_dialogues: Type[Dialogues], target_dialogue: Type[Dialogue]) -> object:
    """Factory method to generate dialogue classes."""

    class MetaClass(target_dialogues):
        """The dialogues class keeps track of all ccxt dialogues."""

        def __init__(self, address: Type[Address]) -> None:
            """Initialize dialogues."""
            self._address = address

            def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
            ) -> Dialogue.Role:
                """Infer the role of the agent from an incoming/outgoing first message

                :param message: an incoming/outgoing first message
                :param receiver_address: the address of the receiving agent
                :return: The role of the agent
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


class BaseDcxtConnectionTest:
    """Tests the http client connection's 'connect' functionality."""

    connection: DcxtConnection
    client_skill_id: str
    agent_identity: Identity

    def setup(self) -> None:
        """Initialise the class."""
        self.client_skill_id = "some/skill:0.1.0"
        self.agent_identity = Identity("name", address="some string", public_key="some public_key")
        configuration = ConnectionConfig(
            target_skill_id=self.client_skill_id,
            exchanges=TEST_EXCHANGES,
            connection_id=DcxtConnection.connection_id,
        )
        self.connection = DcxtConnection(
            configuration=configuration,
            data_dir=MagicMock(),
            identity=self.agent_identity,
        )


@pytest.mark.asyncio
class TestDcxtConnection(BaseDcxtConnectionTest):
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
