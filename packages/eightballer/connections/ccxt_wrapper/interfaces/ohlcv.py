"""Interface for the ohlcv."""

import asyncio
from typing import Any, cast

from packages.eightballer.protocols.ohlcv.message import OhlcvMessage
from packages.eightballer.protocols.ohlcv.dialogues import OhlcvDialogue, BaseOhlcvDialogues
from packages.eightballer.connections.ccxt_wrapper.interfaces.market import Market
from packages.eightballer.connections.ccxt_wrapper.interfaces.interface_base import BaseInterface


def _seconds_to_timeframe(seconds=60):
    """Seconds to timeframe."""
    mapping = {60: "1m", 15: "15s"}
    if seconds not in mapping:
        msg = f"Seconds not in timeframe mapping {seconds}"
        raise ValueError(msg)
    return mapping[seconds]


class OhlcvInterface(BaseInterface):
    """Interface of ohlcv protocol."""

    protocol_id = OhlcvMessage.protocol_id
    dialogue_class = OhlcvDialogue
    dialogues_class = BaseOhlcvDialogues

    @staticmethod
    def _parse_data_to_msg(ccxt_data: list[list[int]], market: Any):
        """Parse ccxt data to msg."""
        keys = ["timestamp", "open", "high", "low", "close", "volume"]
        candle = dict(zip(keys, ccxt_data[-1], strict=False))

        return OhlcvMessage(
            performative=OhlcvMessage.Performative.CANDLESTICK,
            exchange_id=market.exchange_id,
            market_name=market.market_name,
            interval=market.interval,
            **candle,
        )

    async def _poll_market(self, market: Market, connection):
        """Poll market."""
        connection.logger.info(f"Starting to poll : {market.market_name} on {market.exchange_id}")
        exchange = connection.exchanges[market.exchange_id]
        while True:
            res = await exchange.fetchOHLCV(
                market.market_name,
                timeframe=_seconds_to_timeframe(market.interval),
            )
            connection.logger.info(f"Length of candles from api call : {len(res)}")
            response_message = self._parse_data_to_msg(res, market)
            response_envelope = connection.build_envelope(request=market, response_message=response_message)
            await connection.queue.put(response_envelope)
            connection.logger.info(f"Starting to sleep until: {market.interval} for ")
            await asyncio.sleep(market.interval)

    async def subscribe(self, message: OhlcvMessage, dialogue: OhlcvDialogue, connection) -> OhlcvMessage | None:
        """Register market to begin polling for ohlcv."""
        task = connection.loop.create_task(self._poll_market(message, connection))
        connection.polling_tasks.append(task)
        return cast(
            OhlcvMessage | None,
            dialogue.reply(
                performative=OhlcvMessage.Performative.END,
                target_message=message,
            ),
        )
