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

"""Apprise connection and channel."""

import asyncio
import logging
from abc import abstractmethod
from typing import Any, cast
from asyncio.events import AbstractEventLoop
from collections.abc import Callable

import apprise
from aea.common import Address
from aea.mail.base import Message, Envelope
from aea.connections.base import Connection, ConnectionStates
from aea.configurations.base import PublicId
from aea.protocols.dialogue.base import Dialogue

from packages.eightballer.protocols.user_interaction.message import UserInteractionMessage
from packages.eightballer.protocols.user_interaction.dialogues import (
    UserInteractionDialogue,
    BaseUserInteractionDialogues,
)
from packages.eightballer.protocols.user_interaction.custom_types import ErrorCode


def clean_env_var(val: str) -> str:
    """Clean the environment variable."""
    if val is None:
        return None
    if val == "":
        return None
    res = val.strip(val[0]) if val[:1] == val[-1:] and val[:1] in "'\"" else val
    if res in {"None", "null"}:
        return None
    return res


CONNECTION_ID = PublicId.from_str("eightballer/apprise_wrapper:0.1.0")


_default_logger = logging.getLogger("aea.packages.eightballer.connections.apprise")


class UserInteractionDialogues(BaseUserInteractionDialogues):
    """The dialogues class keeps track of all apprise dialogues."""

    def __init__(self, self_address: Address, **kwargs) -> None:
        """Initialize dialogues."""

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> Dialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message."""
            assert message, receiver_address
            return UserInteractionDialogue.Role.USER

        del kwargs
        BaseUserInteractionDialogues.__init__(
            self,
            self_address=self_address,
            role_from_first_message=role_from_first_message,
        )


class BaseAsyncChannel:
    """BaseAsyncChannel."""

    def __init__(
        self,
        agent_address: Address,
        connection_id: PublicId,
        message_type: Message,
    ):
        """Initialize the BaseAsyncChannel channel."""

        self.agent_address = agent_address
        self.connection_id = connection_id
        self.message_type = message_type

        self.is_stopped = True
        self._connection = None
        self._tasks: set[asyncio.Task] = set()
        self._in_queue: asyncio.Queue | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self.logger = _default_logger

    @property
    @abstractmethod
    def performative_handlers(self) -> dict[Message.Performative, Callable[[Message, Dialogue], Message]]:
        """Performative to message handler mapping."""

    @abstractmethod
    async def connect(self, loop: AbstractEventLoop) -> None:
        """Connect channel using loop."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect channel."""

    async def send(self, envelope: Envelope) -> None:
        """Send an envelope with a protocol message.

        It sends the envelope, waits for and receives the result.
        The result is translated into a response envelope.
        Finally, the response envelope is sent to the in-queue.

        """

        if self._loop is None or self._connection is None:
            msg = f"{self.__class__.__name__} not connected, call connect first!"
            raise ConnectionError(msg)

        if not isinstance(envelope.message, self.message_type):
            msg = f"Message not of type {self.message_type}"
            raise TypeError(msg)

        message = envelope.message

        if message.performative not in self.performative_handlers:
            log_msg = "Message with unexpected performative `{message.performative}` received."
            self.logger.error(log_msg)
            return

        handler = self.performative_handlers[message.performative]

        dialogue = cast(Dialogue, self._dialogues.update(message))
        if dialogue is None:
            self.logger.warning(f"Could not create dialogue for message={message}")
            return

        response_message = handler(message, dialogue)
        self.logger.debug(f"returning message: {response_message}")

        response_envelope = Envelope(
            to=str(envelope.sender),
            sender=str(self.connection_id),
            message=response_message,
            protocol_specification_id=self.message_type.protocol_specification_id,
        )

        await self._in_queue.put(response_envelope)

    async def get_message(self) -> Envelope | None:
        """Check the in-queue for envelopes."""

        if self.is_stopped:
            return None
        try:
            return self._in_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def _cancel_tasks(self) -> None:
        """Cancel all requests tasks pending."""

        for task in list(self._tasks):
            if task.done():  # pragma: nocover
                continue
            task.cancel()

        for task in list(self._tasks):
            try:
                await task
            except KeyboardInterrupt:
                raise
            except BaseException:  # noqa
                pass  # nosec


class AppriseAsyncChannel(BaseAsyncChannel):  # pylint: disable=too-many-instance-attributes
    """A channel handling incomming communication from the Apprise connection."""

    def __init__(
        self,
        agent_address: Address,
        connection_id: PublicId,
        **kwargs,
    ):
        """Initialize the Apprise channel."""

        super().__init__(agent_address, connection_id, message_type=UserInteractionMessage)
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._dialogues = UserInteractionDialogues(str(AppriseConnection.connection_id))
        self.logger.debug("Initialised the Apprise channel")

    async def connect(self, loop: AbstractEventLoop) -> None:
        """Connect channel using loop."""

        if self.is_stopped:
            self._loop = loop
            self._in_queue = asyncio.Queue()
            self.is_stopped = False
            try:
                self._connection = apprise.Apprise()
                for endpoint in self.endpoints:
                    cleaned_endpoint = clean_env_var(endpoint)
                    if cleaned_endpoint is None:
                        continue
                    self._connection.add(cleaned_endpoint)
                self.logger.info("Apprise has connected.")
            except Exception as e:  # pragma: nocover # pylint: disable=broad-except
                self.is_stopped = True
                self._in_queue = None
                msg = f"Failed to start Apprise: {e}"
                raise ConnectionError(msg) from e

    async def disconnect(self) -> None:
        """Disconnect channel."""

        if self.is_stopped:
            return

        await self._cancel_tasks()
        self._tasks.clear()
        self.is_stopped = True
        self.logger.info("Apprise has shutdown.")

    @property
    def performative_handlers(
        self,
    ) -> dict[
        UserInteractionMessage.Performative,
        Callable[[UserInteractionMessage, UserInteractionDialogue], UserInteractionMessage],
    ]:
        """Return the mapping of performative to handler."""
        return {
            UserInteractionMessage.Performative.NOTIFICATION: self.notification,
        }

    def notification(
        self, message: UserInteractionMessage, dialogue: UserInteractionDialogue
    ) -> UserInteractionMessage:
        """Handle UserInteractionMessage with NOTIFICATION Perfomative."""

        title = message.title
        body = message.body or ""
        attach = message.attach or ""

        success = self._connection.notify(body=message.body, title=message.title, attach=message.attach)

        result = UserInteractionMessage.Performative.END if success else UserInteractionMessage.Performative.ERROR
        params = {
            "performative": result,
        }
        if not success:
            params["error_code"] = ErrorCode.NOTIFICATION_FAILED
            params["error_msg"] = "Failed to send notification"
            params["error_data"] = {"title": title.encode(), "body": body.encode(), "attach": attach.encode()}
        return dialogue.reply(**params)


class AppriseConnection(Connection):
    """Proxy to the functionality of a Apprise connection."""

    connection_id = CONNECTION_ID

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a Apprise connection."""

        keys = ["endpoints"]
        config = kwargs["configuration"].config
        custom_kwargs = {key: config.pop(key) for key in keys}
        super().__init__(**kwargs)

        self.channel = AppriseAsyncChannel(
            self.address,
            connection_id=self.connection_id,
            **custom_kwargs,
        )

    async def connect(self) -> None:
        """Connect to a Apprise."""

        if self.is_connected:  # pragma: nocover
            return

        with self._connect_context():
            self.channel.logger = self.logger
            await self.channel.connect(self.loop)

    async def disconnect(self) -> None:
        """Disconnect from a Apprise."""

        if self.is_disconnected:
            return  # pragma: nocover
        self.state = ConnectionStates.disconnecting
        await self.channel.disconnect()
        self.state = ConnectionStates.disconnected

    async def send(self, envelope: Envelope) -> None:
        """Send an envelope."""

        self._ensure_connected()
        return await self.channel.send(envelope)

    async def receive(self, *args: Any, **kwargs: Any) -> Envelope | None:
        """Receive an envelope. Blocking."""
        del args, kwargs

        self._ensure_connected()
        try:
            return await self.channel.get_message()
        except Exception as e:  # noqa
            self.logger.info(f"Exception on receive {e}")
            return None
