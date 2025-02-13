# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""This module contains the handlers for the skill of DexDataRetrievalAbciApp."""

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.protocols.markets.message import MarketsMessage
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.valory.skills.abstract_round_abci.handlers import (
    HttpHandler as BaseHttpHandler,
    IpfsHandler as BaseIpfsHandler,
    SigningHandler as BaseSigningHandler,
    ABCIRoundHandler as BaseABCIRoundHandler,
    LedgerApiHandler as BaseLedgerApiHandler,
    TendermintHandler as BaseTendermintHandler,
    ContractApiHandler as BaseContractApiHandler,
    AbstractResponseHandler,
)


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
