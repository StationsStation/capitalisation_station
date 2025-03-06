"""Order protocol handler."""

import os
import site
import asyncio
import importlib

from aea.skills.base import Envelope

from packages.eightballer.protocols.order_book.message import OrderBookMessage
from packages.eightballer.protocols.order_book.dialogues import OrderBookDialogue, BaseOrderBookDialogues
from packages.eightballer.protocols.order_book.custom_types import OrderBook
from packages.eightballer.connections.ccxt_wrapper.interfaces.interface_base import BaseInterface


site_packages_path = site.getsitepackages()[0]
ccxt_path = os.path.join(site_packages_path, "ccxt")

ccxt_spec = importlib.util.spec_from_file_location(
    "ccxt", os.path.join(ccxt_path, "ccxt", "async_support", "__init__.py")
)
ccxt = importlib.util.module_from_spec(ccxt_spec)


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
        try:
            while True:
                try:
                    book = await exchange.watch_order_book(
                        message.symbol,
                    )
                    book = OrderBook(
                        **book,
                        exchange_id=message.exchange_id,
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
                except ccxt.ExchangeError as error:
                    if "out-of-order nonce" in str(error):
                        connection.logger.warning(f"Out of order nonce error for {message.exchange_id}. Retrying...")
                        continue

                    raise
                finally:
                    await asyncio.sleep(DEFAULT_INTERVAL)

        except ccxt.RequestTimeout:
            response_message = dialogue.reply(
                performative=OrderBookMessage.Performative.ERROR,
                target_message=message,
            )
        return response_message
