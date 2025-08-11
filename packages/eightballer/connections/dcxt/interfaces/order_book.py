"""Interface for the order book protocol."""

import asyncio

from aea.skills.base import Envelope

from packages.eightballer.protocols.order_book.message import OrderBookMessage
from packages.eightballer.protocols.order_book.dialogues import OrderBookDialogue, BaseOrderBookDialogues
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


DEFAULT_INTERVAL = 0.1


class OrderBookInterface(BaseInterface):
    """Interface for positions protocol."""

    protocol_id = OrderBookMessage.protocol_id
    dialogue_class = OrderBookDialogue
    dialogues_class = BaseOrderBookDialogues

    async def subscribe(
        self, message: OrderBookMessage, dialogue: OrderBookDialogue, connection
    ) -> OrderBookMessage | None:
        """Get a position from the exchange."""
        exchange = connection.exchanges[message.exchange_id]
        connection.logger.info(f"Subscribing to {message.exchange_id} order book. Symbol: {message.symbol}")
        try:
            while True:
                book = await exchange.watch_order_book(
                    message.symbol,
                )
                response_message = dialogue.reply(
                    performative=OrderBookMessage.Performative.ORDER_BOOK_UPDATE,
                    target_message=message,
                    order_book=book,
                )
                envelope = Envelope(
                    to=response_message.to,
                    sender=response_message.sender,
                    message=response_message,
                )
                await connection.queue.put(envelope)
                await asyncio.sleep(DEFAULT_INTERVAL)
        except Exception:  # noqa
            response_message = dialogue.reply(
                performative=OrderBookMessage.Performative.ERROR,
                target_message=message,
            )
        return response_message
