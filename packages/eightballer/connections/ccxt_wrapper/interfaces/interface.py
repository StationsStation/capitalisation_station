"""Interface."""

from typing import TYPE_CHECKING, Any

from aea.mail.base import Envelope
from aea.protocols.base import Message

from packages.eightballer.connections.ccxt_wrapper.interfaces.ohlcv import OhlcvInterface
from packages.eightballer.connections.ccxt_wrapper.interfaces.order import OrderInterface
from packages.eightballer.connections.ccxt_wrapper.interfaces.market import MarketInterface
from packages.eightballer.connections.ccxt_wrapper.interfaces.ticker import TickerInterface
from packages.eightballer.connections.ccxt_wrapper.interfaces.balance import BalanceInterface
from packages.eightballer.connections.ccxt_wrapper.interfaces.position import PositionInterface
from packages.eightballer.connections.ccxt_wrapper.interfaces.order_book import OrderBookInterface
from packages.eightballer.connections.ccxt_wrapper.interfaces.spot_asset import SpotAssetInterface


if TYPE_CHECKING:
    from collections.abc import Callable

    import ccxt.async_support as ccxt


class ConnectionProtocolInterface:  # pylint: disable=too-many-instance-attributes
    """Interface for the supported protocols."""

    def __init__(self, **kwargs):
        """Initialise the protocol."""
        self.loop = kwargs.get("loop")
        self.logger = kwargs.get("logger")
        self.polling_tasks = kwargs.get("polling_tasks")
        self.executing_tasks = kwargs.get("executing_tasks")
        self.queue = kwargs.get("queue")
        self.exchanges: dict[str, ccxt.Exchange] = kwargs.get("exchanges")
        self.supported_protocols = {
            SpotAssetInterface.protocol_id: SpotAssetInterface(),
            OhlcvInterface.protocol_id: OhlcvInterface(),
            OrderInterface.protocol_id: OrderInterface(),
            MarketInterface.protocol_id: MarketInterface(),
            BalanceInterface.protocol_id: BalanceInterface(),
            PositionInterface.protocol_id: PositionInterface(),
            TickerInterface.protocol_id: TickerInterface(),
            OrderBookInterface.protocol_id: OrderBookInterface(),
        }
        self.handle_task_done = kwargs.get("done_callback")

    def validate_envelope(self, envelope):
        """Handles the message."""
        interface = self.supported_protocols.get(envelope.message.protocol_id)
        return interface is not None

    async def handle_envelope(self, envelope):
        """Handles the message."""
        interface = self.supported_protocols.get(envelope.message.protocol_id)
        msg, dialogue, performative = interface.validate_msg(envelope.message)
        handler: Callable[[Any], Any] = interface.get_handler(performative)
        return await handler(msg, dialogue, connection=self)

    def build_envelope(self, request: Envelope | None, response_message: Message | None):
        """Build the envelope."""
        response_envelope = None

        if response_message is not None:
            to = request.sender if request is not None else response_message.to  # pylint: disable=C0103
            response_envelope = Envelope(
                to=to,
                sender="eightballer/ccxt:0.1.0",
                message=response_message,
            )
        return response_envelope
