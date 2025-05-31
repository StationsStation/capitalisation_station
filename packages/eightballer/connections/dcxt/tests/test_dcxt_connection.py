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

import yaml
import pytest
from aea.common import Address
from async_timeout import timeout
from aea.identity.base import Identity
from aea.protocols.base import Message
from aea.configurations.base import ConnectionConfig
from aea.protocols.dialogue.base import Dialogue, Dialogues

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.connections.dcxt.connection import DcxtConnection


logger = logging.getLogger(__name__)

DEFAULT_EXCHANGE_ID = "balancer"

ROOT_DIR = os.path.join(
    os.path.dirname(__file__),
)

TEST_KEY_PATH = os.path.join(ROOT_DIR, "data", "key")

TEST_WALLET = "0x3A5c777edf22107d7FdFB3B02B0Cdfe8b75f3453"
TEST_PRIVATE_KEY = "0xc14f53ee466dd3fc5fa356897ab276acbef4f020486ec253a23b0d1c3f89d4f4"

TIMEOUT = 5

TEST_EXCHANGE_DATA = """
- name: cowswap
  key_path: packages/eightballer/connections/dcxt/tests/data/key
  wallet: null
  ledger_id: base
  rpc_url: https://base.drpc.org
- name: balancer
  key_path: packages/eightballer/connections/dcxt/tests/data/key
  wallet: null
  ledger_id: base
  rpc_url: https://base.drpc.org
  etherscan_api_key: YOUR_ETHERSCAN_API_KEY
- name: derive
  key_path: packages/eightballer/connections/dcxt/tests/data/key
  wallet: null
  ledger_id: derive
  rpc_url: https://base.llamarpc.com
  subaccount_id: 132849
  environment: test
- name: one_inch
  key_path: packages/eightballer/connections/dcxt/tests/data/key
  wallet: null
  ledger_id: ethereum
  rpc_url: https://eth.drpc.org
- name: kittypunch
  key_path: packages/eightballer/connections/dcxt/tests/data/key
  wallet: null
  ledger_id: ethereum
  rpc_url: https://eth.drpc.org
"""

TEST_EXCHANGES = {(k["name"], k["ledger_id"]): k for k in yaml.safe_load(TEST_EXCHANGE_DATA)}


def with_timeout(t, *args, **kwargs):  # noqa
    """Return a decorator that adds a timeout to a coroutine function."""

    def wrapper(corofunc, *args, **kwargs):  # noqa
        async def run(*func_args, **func_kwargs):
            async with timeout(t):
                return await corofunc(*func_args, **func_kwargs)

        return run

    return wrapper


def get_dialogues(target_dialogues: type[Dialogues], target_dialogue: type[Dialogue]) -> object:
    """Factory method to generate dialogue classes."""

    class MetaClass(target_dialogues):
        """The dialogues class keeps track of all dcxt dialogues."""

        def __init__(self, address: type[Address]) -> None:
            """Initialize dialogues."""
            self._address = address

            def role_from_first_message(  # pylint: disable=unused-argument
                message: Message, receiver_address: Address
            ) -> Dialogue.Role:
                """Infer the role of the agent from an incoming/outgoing first message."""
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

    def setup_method(self) -> None:
        """Initialise the class."""
        self.client_skill_id = "some/skill:0.1.0"
        self.agent_identity = Identity("name", address="some string", public_key="some public_key")
        configuration = ConnectionConfig(
            target_skill_id=self.client_skill_id,
            exchanges=list(TEST_EXCHANGES.values()),
            connection_id=DcxtConnection.connection_id,
        )
        self.connection = DcxtConnection(
            configuration=configuration,
            data_dir=MagicMock(),
            identity=self.agent_identity,
        )


@pytest.mark.asyncio
class TestDcxtConnection(BaseDcxtConnectionTest):
    """Tests the dcxt connection."""

    async def test_all_protocols_supported(self):
        """Test if all protocols are supported."""

    async def test_connects(self):
        """Test if all protocols are supported."""
        await self.connection.connect()

    async def test_multiple_exchanges(self):
        """Test can start multiple exchanges."""

    async def test_custom_exchanges(self):
        """Test can start custom class."""


EXPECTED_FUNCTIONS = [
    "create_order",
    "fetch_tickers",
    "fetch_ticker",
    "fetch_positions",
    "fetch_open_orders",
    "fetch_balance",
    "parse_order",
]


@pytest.mark.parametrize(
    "exchange_id, function",
    [(exchange["name"], function) for exchange in TEST_EXCHANGES.values() for function in EXPECTED_FUNCTIONS],
)
class TestPluginConsitency:
    """Test the plugin consistency."""

    def test_plugins_have_necessary_functions(self, exchange_id, function):
        """Test exchange plugins are consistent."""

        # we import here to avoid loading all the exchanges
        module = getattr(dcxt, exchange_id)
        assert hasattr(module, function), f"Missing function {function} in {exchange_id}"
