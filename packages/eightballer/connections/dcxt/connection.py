"""Connection for dcxt."""

import asyncio
import traceback
from typing import TYPE_CHECKING, Any, cast
from asyncio import Task
from collections import deque

from aea.mail.base import Envelope
from aea.protocols.base import Message
from aea.connections.base import Connection, ConnectionStates
from aea.configurations.base import PublicId

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.default import DefaultMessage
from packages.eightballer.protocols.default.custom_types import ErrorCode
from packages.eightballer.connections.dcxt.interfaces.interface import (
    ConnectionProtocolInterface,
)


if TYPE_CHECKING:
    from packages.eightballer.protocols.markets.custom_types import Market


POLL_INTERVAL_MS = 50
RETRY_DELAY = POLL_INTERVAL_MS * 2
RETRY_BACKOFF = 2
PUBLIC_ID = PublicId.from_str("eightballer/dcxt:0.1.0")

DEFAULT_ENCODING = "utf-8"


class DcxtConnection(Connection):  # pylint: disable=too-many-instance-attributes
    """Dcxt connection class."""

    connection_id = PUBLIC_ID
    protocol_interface = ConnectionProtocolInterface

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the connection."""
        super().__init__(**kwargs)  # pragma: no cover
        self.exchange_configs = self.configuration.config.get("exchanges")

        self._balances = None

        self._exchanges: dict[str, Any] = {}
        self._markets: dict[str, Market]
        self._orders: asyncio.Queue = asyncio.Queue()

        self.done_task_checker: Task | None = None
        self.task_to_request: dict[Task, Envelope] = {}
        self.executing_tasks: list[Task] = []
        self.done_tasks: deque[Task] = deque()
        self.polling_tasks: list[Task] = []
        self.queue: asyncio.Queue | None = None
        self.exchange_to_orders = {}

    async def connect(self) -> None:
        """Start done task checker as a coroutine."""
        self.queue = asyncio.Queue()
        self.protocol_interface = ConnectionProtocolInterface(
            loop=self.loop,
            logger=self.logger,
            polling_tasks=self.polling_tasks,
            executing_tasks=self.executing_tasks,
            queue=self.queue,
            exchanges=self._exchanges,
            done_callback=self._handle_done_task,
        )

        for exchange_config in self.exchange_configs:
            exchange_name = exchange_config.get("name")
            ledger_id = exchange_config.get("ledger_id")
            self.logger.info(f"Connecting to {exchange_name} with ledger_id {ledger_id}")
            try:
                exchange_class = getattr(dcxt, exchange_name)
                exchange = exchange_class(**exchange_config, logger=self.logger)
            except AttributeError as exc:
                msg = f"Exchange {exchange_name} not found in dcxt"
                raise ValueError(msg) from exc

            ledger_exchanges = self._exchanges.get(ledger_id, {})
            ledger_exchanges.update({exchange_name: exchange})
            self._exchanges.update({ledger_id: ledger_exchanges})
            self.logger.info(f"Successfully connected to {exchange_name} with ledger_id {ledger_id}")
        self.state = ConnectionStates.connected

    async def disconnect(self) -> None:
        """Tear down the connection."""
        if self.is_disconnected:  # pragma: nocover
            return

        self.state = ConnectionStates.disconnecting

        tasks = [
            task
            for task_list in [
                self.task_to_request.values(),
                self.done_task_checker,
                self.task_to_request.keys(),
                self.executing_tasks,
                self.done_tasks,
                self.polling_tasks,
            ]
            if task_list is not None
            for task in task_list
        ]

        for task in tasks:
            if isinstance(task, Envelope):
                continue
            if not task.cancelled():  # pragma: nocover
                task.cancel()

        self.state = ConnectionStates.disconnected
        for exchanges in self._exchanges.values():
            for exchange in exchanges.values():
                await exchange.close()

    async def send(self, envelope: Envelope) -> None:
        """Send an envelope."""
        task = self._handle_req(envelope)
        task.add_done_callback(self._handle_done_task)
        self.executing_tasks.append(task)
        self.task_to_request[task] = envelope

    async def receive(self, *args: Any, **kwargs: Any) -> Envelope:  # noqa: ARG002
        """Receive a message."""
        return cast(Envelope, await self.queue.get())

    async def _execute(self, envelope: Envelope) -> Message:
        try:
            self.protocol_interface.validate_envelope(envelope)
            return await self.protocol_interface.handle_envelope(envelope)
        except Exception as error:  # pylint: disable=broad-except
            self.logger.exception(f"Couldn't execute task, e={error} traceback={traceback.print_exc()}")
            return self.get_error_message(error, envelope.message)

    def _handle_req(self, envelope: Envelope) -> Task:
        """Create a task."""
        return self.loop.create_task(self._execute(envelope))

    def _handle_done_task(self, task: Task) -> None:
        """Handle completed task."""
        request = self.task_to_request.pop(task)
        self.executing_tasks.remove(task)
        response_message: Message | None = task.result()
        response_envelope = self.protocol_interface.build_envelope(request, response_message)
        if response_envelope is None:
            return
        self.logger.debug(f"Placing {response_message} in queue")
        self.queue.put_nowait(response_envelope)

    def get_error_message(self, error: Exception, request: Message):
        """Get the error message."""
        self.logger.error("Unable to handle protocol %s : %s message", request.protocol_id, request.performative)
        return DefaultMessage(
            performative=DefaultMessage.Performative.ERROR,
            error_msg=str(error),
            error_code=ErrorCode.DECODING_ERROR,
            error_data={"body": request.encode()},
        )
