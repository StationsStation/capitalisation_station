"""
Connection for dcxt.
"""

import os
import asyncio
import traceback
from typing import Any, Dict, List, Deque, Optional, cast
from asyncio import Task
from collections import deque

from aea.mail.base import Envelope
from aea.protocols.base import Message
from aea.connections.base import Connection, ConnectionStates
from aea.configurations.base import PublicId
from aea.protocols.dialogue.base import Dialogue

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.default import DefaultMessage
from packages.eightballer.protocols.default.custom_types import ErrorCode
from packages.eightballer.protocols.markets.custom_types import Market
from packages.eightballer.connections.dcxt.interfaces.interface import ConnectionProtocolInterface


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
        """
        Initialize the connection

        :param kwargs: keyword arguments passed to component base
        """
        super().__init__(**kwargs)  # pragma: no cover
        self.exchange_configs = self.configuration.config.get("exchanges")

        self._balances = None

        self._exchanges: Dict[str, Any] = {}
        self._markets: Dict[str, Market]
        self._orders: asyncio.Queue = asyncio.Queue()

        self.done_task_checker: Optional[Task] = None
        self.task_to_request: Dict[Task, Envelope] = {}
        self.executing_tasks: List[Task] = []
        self.done_tasks: Deque[Task] = deque()
        self.polling_tasks: List[Task] = []
        self.queue: Optional[asyncio.Queue] = None
        self.exchange_to_orders = {}

    async def connect(self) -> None:
        """
        Start done task checker as a coroutine

        :return:
        """
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

        for exchange_id, exchange_config in self.exchange_configs.items():
            exchange_name = exchange_config.get("name")
            ledger_id = exchange_config.get("ledger_id")
            self.logger.info(f"Connecting to {exchange_name} with ledger_id {ledger_id}")
            try:
                exchange_class = getattr(dcxt, exchange_name)
                exchange = exchange_class(**exchange_config)
            except AttributeError as exc:
                raise ValueError(f"Exchange {exchange_name} not found in dcxt") from exc
            self._exchanges.update({exchange_id: exchange})
            self.logger.info(f"Successfully connected to {exchange_id}")
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
        for exchange in self._exchanges.values():
            await exchange.close()

    async def send(self, envelope: Envelope) -> None:
        task = self._handle_req(envelope)
        task.add_done_callback(self._handle_done_task)
        self.executing_tasks.append(task)
        self.task_to_request[task] = envelope

    async def receive(self, *args: Any, **kwargs: Any) -> Optional[Envelope]:
        envelope = cast(
            Envelope,
            await self.queue.get(),
        )
        del args, kwargs
        return envelope

    async def _execute(self, envelope=None) -> Optional[Message]:
        dialogue: Dialogue
        try:
            dialogue = self.protocol_interface.validate_envelope(envelope)
            return await self.protocol_interface.handle_envelope(envelope)
        except Exception as error:  # pylint: disable=broad-except
            self.logger.error(f"Couldn't execute task, e={error} traceback={traceback.print_exc()}")
            return self.get_error_message(error, envelope.message, dialogue)

    def _handle_req(self, envelope) -> Task:
        """Create a task."""
        return self.loop.create_task(self._execute(envelope))

    def _handle_done_task(self, task: Task) -> None:
        """Handle completed task."""
        request = self.task_to_request.pop(task, None)
        self.executing_tasks.remove(task)
        response_message: Optional[Message] = task.result()
        response_envelope = self.protocol_interface.build_envelope(request, response_message)
        if response_envelope is None:
            return
        self.logger.debug(f"Placing {response_message} in queue")
        self.queue.put_nowait(response_envelope)

    def get_error_message(
        self,
        error: str,
        request: Optional[Message],
        response_message: Optional[Message],
    ):
        """Get the error message."""
        self.logger.error("Unable to handle protocol : %s message", request.performative)
        message = DefaultMessage(
            performative=DefaultMessage.Performative.ERROR,
            error_msg=bytes(str(error), "utf-8"),
            error_code=ErrorCode.DECODING_ERROR,
        )
        if response_message:
            return response_message
        return message
