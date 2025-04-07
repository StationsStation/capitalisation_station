"""Post trade round behaviour."""

import asyncio
from typing import Any, cast
from textwrap import dedent

from packages.eightballer.skills.simple_fsm.enums import ArbitrageabciappEvents
from packages.eightballer.protocols.orders.custom_types import Order
from packages.eightballer.connections.apprise.connection import CONNECTION_ID as APPRISE_PUBLIC_ID
from packages.eightballer.protocols.user_interaction.message import UserInteractionMessage
from packages.eightballer.protocols.user_interaction.dialogues import UserInteractionDialogues
from packages.eightballer.skills.simple_fsm.behaviour_classes.base import BaseBehaviour


class PostTradeRound(BaseBehaviour):
    """This class implements the PostTradeRound state."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.setup()

    def setup(self) -> None:
        """Setup the state."""
        self._is_done = False  # Initially, the state is not done
        self.started = False

    @property
    def strategy(self):
        """Return the strategy."""
        return self.context.arbitrage_strategy

    async def act(self) -> None:
        """Perform the action of the state."""
        if self.started:
            return
        self.started = True
        self._is_done = True
        self._event = ArbitrageabciappEvents.DONE
        sell_order, buy_order = self.strategy.state.submitted_orders

        def get_explorer_link(order: Order) -> str:
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
        self.send_notification_to_user(
            title="Post Successful Arbitrage Execution!",
            msg=report_msg_table,
        )
        self.context.logger.info(f"Sleeping for {self.strategy.cool_down_period} seconds.")
        await asyncio.sleep(self.strategy.cool_down_period)

    def send_notification_to_user(self, title: str, msg: str, attach: str | None = None) -> None:
        """Send notification to user."""
        dialogues = cast(UserInteractionDialogues, self.context.user_interaction_dialogues)
        msg, _ = dialogues.create(
            counterparty=str(APPRISE_PUBLIC_ID),
            performative=UserInteractionMessage.Performative.NOTIFICATION,
            title=title,
            body=msg,
            attach=attach,
        )
        self.context.outbox.put_message(message=msg)
