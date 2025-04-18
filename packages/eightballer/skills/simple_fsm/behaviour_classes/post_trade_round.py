"""Post trade round behaviour."""

import asyncio
from textwrap import dedent

from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.protocols.orders.custom_types import Order
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseBehaviour


class PostTradeRound(BaseBehaviour):
    """This class implements the PostTradeRound state."""

    async def act(self) -> None:
        """Perform the action of the state."""
        if self.started:
            return
        self.started = True
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        sell_order, buy_order = self.strategy.state.submitted_orders

        def get_explorer_link(order: Order) -> None:
            """Get the explorer link."""

            exchange_to_explorer = {
                "cowswap": f"https://explorer.cow.fi/{order.ledger_id}/orders/",
            }
            explorers = {
                "mode": "https://modescan.io/tx/",
                "gnosis": "https://gnosisscan.io/tx/",
                "derive": "https://explorer.derive.xyz/tx/",
                "ethereum": exchange_to_explorer.get(order.exchange_id, "https://etherscan.io/tx/"),
                "base": exchange_to_explorer.get(order.exchange_id, "https://basescan.org/tx/"),
            }
            if order.ledger_id not in explorers:
                return ""
            return f"{explorers[order.ledger_id]}{order.id}"

        delta = -(buy_order.price / sell_order.price * 100 - 100)
        value_captured_gross = -(buy_order.price - sell_order.price) * sell_order.amount
        report_msg_table = dedent(f"""
        [Sell]({get_explorer_link(sell_order)}) {sell_order.symbol} on {sell_order.ledger_id}:{sell_order.exchange_id}
        {sell_order.amount}@{sell_order.price:5f}  total: {sell_order.amount * sell_order.price:5f}
        [Buy]({get_explorer_link(buy_order)}) {buy_order.symbol} on {buy_order.ledger_id}:{buy_order.exchange_id}
        {buy_order.amount}@{buy_order.price:5f}  total: {buy_order.amount * buy_order.price:5f}
        --------------------------
        Delta:          {-delta:5f}%
        Value captured: {value_captured_gross:6f}
        """)
        self.strategy.send_notification_to_user(
            title="Post Successful Arbitrage Execution!",
            msg=report_msg_table,
        )
        self.context.logger.info(f"Sleeping for {self.strategy.cool_down_period} seconds.")
        self.strategy.state.current_period += 1
        await asyncio.sleep(self.strategy.cool_down_period)
