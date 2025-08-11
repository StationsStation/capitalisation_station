"""Interface."""

from typing import TYPE_CHECKING, Any

from aea.mail.base import Envelope
from aea.protocols.base import Message

from packages.eightballer.connections.dcxt import PUBLIC_ID
from packages.eightballer.connections.dcxt.interfaces.ohlcv import OhlcvInterface
from packages.eightballer.connections.dcxt.interfaces.order import OrderInterface
from packages.eightballer.connections.dcxt.interfaces.market import MarketInterface
from packages.eightballer.connections.dcxt.interfaces.ticker import TickerInterface
from packages.eightballer.connections.dcxt.interfaces.balance import BalanceInterface
from packages.eightballer.connections.dcxt.interfaces.position import PositionInterface
from packages.eightballer.connections.dcxt.interfaces.approvals import ApprovalsInterface
from packages.eightballer.connections.dcxt.interfaces.order_book import OrderBookInterface
from packages.eightballer.connections.dcxt.interfaces.spot_asset import SpotAssetInterface
from packages.eightballer.connections.dcxt.interfaces.asset_bridging import AssetBridgingInterface


if TYPE_CHECKING:
    from collections.abc import Callable


class ConnectionProtocolInterface:  # pylint: disable=too-many-instance-attributes
    """Interface for the supported protocols."""

    def __init__(self, **kwargs):
        """Initialise the protocol."""
        self.loop = kwargs.get("loop")
        self.logger = kwargs.get("logger")
        self.polling_tasks = kwargs.get("polling_tasks")
        self.executing_tasks = kwargs.get("executing_tasks")
        self.queue = kwargs.get("queue")
        self.exchanges: dict[str, Any] = kwargs.get("exchanges")
        self.supported_protocols = {
            SpotAssetInterface.protocol_id: SpotAssetInterface(),
            ApprovalsInterface.protocol_id: ApprovalsInterface(),
            OhlcvInterface.protocol_id: OhlcvInterface(),
            OrderInterface.protocol_id: OrderInterface(),
            MarketInterface.protocol_id: MarketInterface(),
            BalanceInterface.protocol_id: BalanceInterface(),
            PositionInterface.protocol_id: PositionInterface(),
            TickerInterface.protocol_id: TickerInterface(),
            OrderBookInterface.protocol_id: OrderBookInterface(),
            AssetBridgingInterface.protocol_id: AssetBridgingInterface(),
        }
        self.handle_task_done = kwargs.get("done_callback")

    def validate_envelope(self, envelope: Envelope) -> bool:
        """Handles the message."""
        interface = self.supported_protocols.get(envelope.message.protocol_id)
        return interface is not None

    async def handle_envelope(self, envelope: Envelope) -> Message:
        """Handles the message."""
        interface = self.supported_protocols.get(envelope.message.protocol_id)
        msg, dialogue, performative = interface.validate_msg(envelope.message)
        handler: Callable[[Any], Any] = interface.get_handler(performative)
        return await handler(msg, dialogue, connection=self)

    def build_envelope(self, request: Envelope | None, response_message: Message | None) -> Envelope | None:
        """Build the envelope."""
        response_envelope = None

        if response_message is not None:
            to = request.sender if request is not None else response_message.to  # pylint: disable=C0103
            response_envelope = Envelope(
                to=to,
                sender=str(PUBLIC_ID),
                message=response_message,
            )
        return response_envelope
