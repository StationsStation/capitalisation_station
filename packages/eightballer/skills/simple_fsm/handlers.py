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

"""This package contains a scaffold of a handler."""

from typing import cast

from aea.skills.base import Handler

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.skills.simple_fsm.strategy import ArbitrageStrategy
from packages.eightballer.protocols.approvals.message import ApprovalsMessage
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.zarathustra.protocols.asset_bridging.message import (
    AssetBridgingMessage,
)
from packages.eightballer.protocols.user_interaction.message import UserInteractionMessage
from packages.eightballer.skills.abstract_round_abci.handlers import (
    HttpHandler as BaseHttpHandler,
    IpfsHandler as BaseIpfsHandler,
    SigningHandler as BaseSigningHandler,
    ABCIRoundHandler as BaseABCIRoundHandler,
    LedgerApiHandler as BaseLedgerApiHandler,
    TendermintHandler as BaseTendermintHandler,
    ContractApiHandler as BaseContractApiHandler,
    AbstractResponseHandler,
)
from packages.eightballer.protocols.user_interaction.dialogues import UserInteractionDialogues


ABCIHandler = BaseABCIRoundHandler
HttpHandler = BaseHttpHandler
SigningHandler = BaseSigningHandler
LedgerApiHandler = BaseLedgerApiHandler
ContractApiHandler = BaseContractApiHandler
TendermintHandler = BaseTendermintHandler
IpfsHandler = BaseIpfsHandler


class DexMarketsHandler(AbstractResponseHandler):
    """This class implements a handler for DexMarketsHandler messages."""

    SUPPORTED_PROTOCOL = MarketsMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            MarketsMessage.Performative.ALL_MARKETS,
            MarketsMessage.Performative.MARKET,
            MarketsMessage.Performative.ERROR,
        }
    )


class DexOrdersHandler(AbstractResponseHandler):
    """This class implements a handler for DexOrdersHandler messages."""

    SUPPORTED_PROTOCOL = OrdersMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            OrdersMessage.Performative.ORDERS,
            OrdersMessage.Performative.ORDER,
            OrdersMessage.Performative.ORDER_CREATED,
            OrdersMessage.Performative.ORDER_CANCELLED,
            OrdersMessage.Performative.ERROR,
        }
    )


class DexApprovalsHandler(AbstractResponseHandler):
    """This class implements a handler for DexApprovalsHandler messages."""

    SUPPORTED_PROTOCOL = ApprovalsMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            ApprovalsMessage.Performative.APPROVAL_RESPONSE,
            ApprovalsMessage.Performative.ERROR,
        }
    )


class DexBalancesHandler(AbstractResponseHandler):
    """This class implements a handler for DexBalancesHandler messages."""

    SUPPORTED_PROTOCOL = BalancesMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            BalancesMessage.Performative.ALL_BALANCES,
            BalancesMessage.Performative.BALANCE,
            BalancesMessage.Performative.ERROR,
        }
    )


class DexPositionsHandler(AbstractResponseHandler):
    """This class implements a handler for DexPositionsHandler messages."""

    SUPPORTED_PROTOCOL = PositionsMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            PositionsMessage.Performative.ALL_POSITIONS,
            PositionsMessage.Performative.POSITION,
            PositionsMessage.Performative.ERROR,
        }
    )


class DexTickersHandler(AbstractResponseHandler):
    """This class implements a handler for DexTickersHandler messages."""

    SUPPORTED_PROTOCOL = TickersMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            TickersMessage.Performative.ALL_TICKERS,
            TickersMessage.Performative.TICKER,
            TickersMessage.Performative.ERROR,
        }
    )


class UserInteractionHandler(Handler):
    """This class implements a handler for DexMarketsHandler messages."""

    SUPPORTED_PROTOCOL = UserInteractionMessage.protocol_id

    def setup(self):
        """Set up the handler."""

    def handle(self, message: UserInteractionMessage):
        """Handle a message."""
        dialogues = cast(UserInteractionDialogues, self.context.user_interaction_dialogues)
        dialogues.update(message)

    def teardown(self):
        """Tear down the handler."""


class DexAssetBridgingHandler(AbstractResponseHandler):
    """This class implements a handler for AssetBridgingHandler messages."""

    SUPPORTED_PROTOCOL = AssetBridgingMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            AssetBridgingMessage.Performative.BRIDGE_STATUS,
            AssetBridgingMessage.Performative.ERROR,
            AssetBridgingMessage.Performative.REQUEST_STATUS,
        }
    )

    def handle(self, message):
        """We log the message and pass it to the dialogue manager."""
        self.context.logger.info(f"Handling message: {message}")
        if self.strategy.state.bridge_requests:
            self.context.logger.info(f"Bridge requests before handling: {self.strategy.state.bridge_requests}")
            self.strategy.state.bridge_requests = []
        return super().handle(message)

    @property
    def strategy(self) -> ArbitrageStrategy:
        """Return the strategy."""
        return self.context.arbitrage_strategy
