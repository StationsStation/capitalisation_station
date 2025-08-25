"""CowSwap client for swapping tokens on the CowSwap DEX."""

import asyncio
import logging
import datetime
import warnings
from ssl import SSLWantReadError
from enum import Enum
from typing import get_args
from functools import lru_cache

import httpx
import httpcore
import rich_click as click
from rich import print
from aea_ledger_ethereum import Address, EthereumApi, EthereumCrypto
from cowdao_cowpy.cow.swap import (
    CHAIN_TO_EXPLORER,
    Wei,
    Envs,
    Order as CowOrder,
    LocalAccount,
    SigningScheme,
    CompletedOrder,
    ChecksumAddress,
    PreSignSignature,
    post_order,
    sign_order,
)
from aea.configurations.base import PublicId
from cowdao_cowpy.common.chains import Chain as CowChains
from cowdao_cowpy.common.config import SupportedChainId
from cowdao_cowpy.order_book.api import OrderBookApi
from cowdao_cowpy.contracts.order import OrderKind
from cowdao_cowpy.common.constants import CowContractAddress
from cowdao_cowpy.common.api.errors import UnexpectedResponseError
from cowdao_cowpy.order_book.config import OrderBookAPIConfigFactory
from cowdao_cowpy.order_book.generated.model import (
    OrderStatus as CowOrderStatus,
    TokenAmount,
    OrderQuoteSide1,
    OrderQuoteRequest,
    OrderQuoteResponse,
    OrderQuoteSideKindSell,
)

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.orders.custom_types import Order, Orders, OrderSide, OrderType, OrderStatus
from packages.eightballer.connections.dcxt.dcxt.one_inch import (
    InvalidSwapParams,
    InsufficientBalance,
    InsufficientAllowance,
    get_allowance,
    increase_allowance,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.connections.dcxt.dcxt.exceptions import RpcError, ExchangeNotAvailable
from packages.eightballer.connections.dcxt.erc_20.contract import Erc20, Erc20Token
from packages.eightballer.connections.dcxt.dcxt.data.tokens import NATIVE_ETH, LEDGER_TO_WRAPPER, SupportedLedgers
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import BaseErc20Exchange


APP_DATA = "0xf142fb87fd167a929b0aacb90fca1e6bf963fcf0513a57af7e4223897df4d93e"

MAX_ORDER_ATTEMPTS = 5
MAX_QUOTE_ATTEMPTS = 5
SLIPPAGE_TOLERANCE = 0.0025
# 1bps fee applied to all trades
SPENDER = {
    SupportedLedgers.ETHEREUM: CowContractAddress.VAULT_RELAYER.value,
    SupportedLedgers.GNOSIS: CowContractAddress.VAULT_RELAYER.value,
    SupportedLedgers.BASE: CowContractAddress.VAULT_RELAYER.value,
    SupportedLedgers.ARBITRUM: CowContractAddress.VAULT_RELAYER.value,
    SupportedLedgers.POLYGON: CowContractAddress.VAULT_RELAYER.value,
}
LEDGER_TO_CHAIN_ID = {
    SupportedLedgers.ETHEREUM: CowChains.MAINNET.value[0].value,
    SupportedLedgers.GNOSIS: CowChains.GNOSIS.value[0].value,
    SupportedLedgers.BASE: CowChains.BASE.value[0].value,
    SupportedLedgers.ARBITRUM: CowChains.ARBITRUM_ONE.value[0].value,
    SupportedLedgers.POLYGON: CowChains.POLYGON.value[0].value,
}

LEDGER_TO_COW_CHAIN = {
    SupportedLedgers.ETHEREUM: CowChains.MAINNET,
    SupportedLedgers.GNOSIS: CowChains.GNOSIS,
    SupportedLedgers.BASE: CowChains.BASE,
    SupportedLedgers.ARBITRUM: CowChains.ARBITRUM_ONE,
    SupportedLedgers.POLYGON: CowChains.POLYGON,
}

LEDGER_TO_RPC = {
    SupportedLedgers.ETHEREUM: "https://eth.llamarpc.com",
    SupportedLedgers.GNOSIS: "https://gnosis.drpc.org",
    SupportedLedgers.BASE: "https://base.llamarpc.com",
    SupportedLedgers.ARBITRUM: "https://arbitrum.drpc.org",
    SupportedLedgers.POLYGON: "https://polygon.llamarpc.com",
}

warnings.filterwarnings("ignore", category=UserWarning)


class CowAsset(Enum):
    """Enum for CoW assets."""

    ERC20 = "erc20"


async def get_quote(
    buy_token: Erc20Token,
    sell_token: Erc20Token,
    sell_amount_int: int,
    chain: CowChains,
    address: Address,
    order_book_api: OrderBookApi,
    retries: int = MAX_QUOTE_ATTEMPTS,
):
    """Get a quote for a token swap."""
    order_quote_request = OrderQuoteRequest(
        sellToken=sell_token.address,
        buyToken=buy_token.address,
        from_=address,  # type: ignore # pyright doesn't recognize `populate_by_name=True`.
    )
    order_side = OrderQuoteSide1(
        kind=OrderQuoteSideKindSell.sell,
        sellAmountBeforeFee=TokenAmount(str(sell_amount_int)),
    )

    try:
        return await order_book_api.post_quote(order_quote_request, order_side)
    except (
        httpcore.ReadTimeout,
        httpx.ReadTimeout,
        UnexpectedResponseError,
        SSLWantReadError,
        asyncio.CancelledError,
    ) as err:
        if retries > 0:
            await asyncio.sleep(0.1 * (MAX_ORDER_ATTEMPTS - retries))
            return await get_quote(
                buy_token=buy_token,
                sell_token=sell_token,
                sell_amount_int=sell_amount_int,
                chain=chain,
                address=address,
                order_book_api=order_book_api,
                retries=retries - 1,
            )
        msg = "CoW Swap API is not available"
        raise ExchangeNotAvailable(msg) from err


async def swap_tokens(
    amount: Wei,
    account: LocalAccount,
    chain: CowChains,
    order_book_api: OrderBookApi,
    sell_token: ChecksumAddress,
    buy_token: ChecksumAddress,
    safe_address: ChecksumAddress | None = None,
    app_data: str = APP_DATA,
    slippage_tolerance: float = 0.000,
) -> CompletedOrder:
    """Swap tokens using the CoW Protocol.
    `CowContractAddress.VAULT_RELAYER` needs to be approved to spend the sell token before calling this function.
    """
    chain_id = SupportedChainId(chain.value[0])

    order_quote_request = OrderQuoteRequest(
        sellToken=sell_token,
        buyToken=buy_token,
        from_=safe_address if safe_address is not None else account._address,  # noqa
        appData=app_data,
    )
    order_side = OrderQuoteSide1(
        kind=OrderQuoteSideKindSell.sell,
        sellAmountBeforeFee=TokenAmount(str(amount)),
    )

    order_quote: OrderQuoteResponse = await order_book_api.post_quote(order_quote_request, order_side)
    valid_to = order_quote.quote.validTo
    # we set the expiration to be 1 years from now
    valid_to += 7 * 24 * 60 * 60
    order = CowOrder(
        sell_token=sell_token,
        buy_token=buy_token,
        receiver=safe_address if safe_address is not None else account.address,
        valid_to=valid_to,
        app_data=app_data,
        sell_amount=str(amount),  # Since it is a sell order, the sellAmountBeforeFee is the same as the sellAmount.
        buy_amount=str(int(int(order_quote.quote.buyAmount.root) * (1.0 - slippage_tolerance))),
        fee_amount="0",  # CoW Swap does not charge fees.
        kind=OrderQuoteSideKindSell.sell.value,
        sell_token_balance=CowAsset.ERC20.value,
        buy_token_balance=CowAsset.ERC20.value,
    )

    base_url = CHAIN_TO_EXPLORER.get(chain_id, "https://explorer.cow.fi")
    signature = (
        PreSignSignature(
            scheme=SigningScheme.PRESIGN,
            data=safe_address,
        )
        if safe_address is not None
        else sign_order(chain, account, order)
    )
    order_uid = await post_order(account, safe_address, order, signature, order_book_api)
    order_link = f"{base_url}/orders/{order_uid.root!s}".lower()
    order_link = order_book_api.get_order_link(order_uid)
    return CompletedOrder(uid=order_uid, url=order_link)


class CowSwapClient(BaseErc20Exchange):
    """Class for interacting with the 1inch API."""

    last_buy_quote: OrderQuoteResponse | None = None
    last_sell_quote: OrderQuoteResponse | None = None

    async def close(self):
        """Close the client."""

    def _parse_order(
        self,
        order: CowOrder,
        exchange_id: str,
        symbol: str,
        price: float,
        amount: float,
        side: OrderSide,
        status=OrderStatus.OPEN,
        **kwargs,
    ) -> Order:
        """Parse an order."""
        self.logger.debug(f"Raw Order: {order}")
        del kwargs
        order = Order(
            exchange_id=exchange_id,
            ledger_id=self.ledger_id,
            symbol=symbol,
            price=price,
            amount=amount if side == OrderSide.SELL else amount / price,
            side=side,
            id=str(order.uid.root),
            type=OrderType.LIMIT,
            status=status,
        )
        self.logger.debug(f"Parsed Order: {order}")
        return order

    def parse_order(self, order: Order, *args, **kwargs) -> Order:
        """Parse an order."""
        del kwargs, args
        return order

    async def fetch_tickers(self, **kwargs):
        """Fetch tickers."""
        del kwargs
        return Tickers(tickers=[])

    async def fetch_ticker(self, **kwargs):
        """Fetch a ticker."""
        if kwargs.get("symbol") is None:
            symbol_a = kwargs.get("asset_a")
            symbol_b = kwargs.get("asset_b")
            if symbol_a is None or symbol_b is None:
                msg = "Symbol or asset_a and asset_b must be provided"
                raise ValueError(msg)
            symbol = f"{symbol_a}/{symbol_b}"
        else:
            symbol = kwargs.get("symbol")
            symbol_a, symbol_b = symbol.split("/")

        asset_a, asset_b = self.get_assets_from_symbols(symbol_a, symbol_b)
        params = kwargs.get("params", {})
        amount = amoun if params and (amoun := params.get("amount")) else 0.5
        sell_amount_int = int(asset_a.to_machine(amount))
        buy_quote = await self._get_quote(asset_a, asset_b, sell_amount_int)
        bid_price = self.from_quote_to_rates(buy_quote, asset_a, asset_b, is_buying=True)

        sell_quote = await self._get_quote(asset_b, asset_a, int(buy_quote.quote.buyAmount.root))
        ask_price = self.from_quote_to_rates(sell_quote, asset_b, asset_a, is_buying=False)

        self.last_buy_quote = buy_quote
        self.last_sell_quote = sell_quote

        timestamp = datetime.datetime.now(tz=datetime.UTC)
        return Ticker(
            symbol=symbol,
            asset_a=asset_a.address,
            asset_b=asset_b.address,
            high=ask_price,
            low=bid_price,
            ask=ask_price,
            bid=bid_price,
            timestamp=int(timestamp.timestamp()),
            datetime=timestamp.isoformat(),
        )

    async def _get_quote(self, asset_a, asset_b, sell_amount_int):
        try:
            return await get_quote(
                buy_token=asset_b,
                sell_token=asset_a,
                sell_amount_int=sell_amount_int,
                chain=self.chain,
                address=self.account.entity.address,
                order_book_api=self.order_book_api,
            )
        except UnexpectedResponseError as error:
            self.logger.exception(f"Failed to get quote: {error}")
            raise RpcError from error
        except Exception as error:
            self.logger.exception(f"Failed to get quote: {error}")
            msg = "CoW Swap API is not available"
            raise ExchangeNotAvailable(msg) from error

    def from_quote_to_rates(self, quote, asset_a, asset_b, is_buying=True):
        """Convert a quote to rates."""
        if not quote:
            print("Failed to get quote")
        output_human = asset_b.to_human(int(quote.quote.buyAmount.root))
        input_less_fees_human = asset_a.to_human(int(quote.quote.sellAmount.root))
        calculated_rate = input_less_fees_human / output_human
        inverted_rate = 1 / calculated_rate
        if is_buying:
            return inverted_rate
        return calculated_rate

    async def create_order(self, cooldown=1, attempts=0, **kwargs):
        """Create an order."""
        if attempts >= MAX_ORDER_ATTEMPTS:
            msg = "Failed to submit order"
            raise ValueError(msg)
        symbol = kwargs.get("symbol")
        price = kwargs.get("price")
        if not price:
            msg = "Price must be provided"
            raise ValueError(msg)
        symbol_a, symbol_b = symbol.split("/")
        asset_a, asset_b = self.get_assets_from_symbols(symbol_a, symbol_b)
        amount = kwargs.get("amount")
        side = OrderSide[kwargs.get("side").upper()]
        if side == OrderSide.BUY:
            buy_token = asset_a
            sell_token = asset_b
            amount *= price
        elif side == OrderSide.SELL:
            buy_token = asset_b
            sell_token = asset_a
        else:
            msg = "Invalid side"
            raise ValueError(msg)
        amount_int = sell_token.to_machine(amount)

        print(f""""
        amount={amount_int},
        buy_token={buy_token.address},
        sell_token={sell_token.address},
        chain={LEDGER_TO_COW_CHAIN[self.supported_ledger]},
        account={self.account.entity.address},
        price={price},
        side={side},
        """)
        self.logger.info(f"Submitting {side} order for {amount} {sell_token.symbol} for {buy_token.symbol}")

        try:
            raw_order = await swap_tokens(
                order_book_api=self.order_book_api,
                buy_token=buy_token.address,
                sell_token=sell_token.address,
                amount=amount_int,
                chain=self.chain,
                account=self.account.entity,
                slippage_tolerance=SLIPPAGE_TOLERANCE,  # we need it to be exact!
            )
        except Exception as error:
            await asyncio.sleep(cooldown * attempts)
            self.logger.exception(f"Failed to submit order: {error}")
            return await self.create_order(attempts=attempts + 1, **kwargs)

        return self._parse_order(
            order=raw_order,
            exchange_id=self.exchange_id,
            symbol=symbol,
            price=price,
            amount=amount,
            side=side,
            ledger_id=self.ledger_id,
        )

    @lru_cache(maxsize=128)  # noqa
    def get_assets_from_symbols(self, symbol_a, symbol_b):
        """Get assets from symbols."""
        asset_a = self.look_up_by_symbol(symbol_a, ledger=SupportedLedgers(self.ledger_id))
        asset_b = self.look_up_by_symbol(symbol_b, ledger=SupportedLedgers(self.ledger_id))
        return asset_a, asset_b

    def _process_submitted_orders(self, orders: list[CowOrder]):  # noqa
        """Process submitted orders."""

        def lookup_symbol(order: CowOrder):
            is_sell = OrderKind(order.kind.value) == OrderKind.SELL
            symbol_a = self.get_token(str(order.sellToken.root))
            symbol_b = self.get_token(str(order.buyToken.root))
            if is_sell:
                return f"{symbol_b.symbol}/{symbol_a.symbol}"
            return f"{symbol_a.symbol}/{symbol_b.symbol}"

        def get_order_side(order: CowOrder):
            if order.kind == OrderQuoteSideKindSell.sell:
                return OrderSide.SELL
            return OrderSide.BUY

        def get_order_status(order: CowOrder):
            if order.status is CowOrderStatus.open:
                return OrderStatus.OPEN
            if order.status is CowOrderStatus.cancelled:
                return OrderStatus.CANCELLED
            if order.status is CowOrderStatus.fulfilled:
                return OrderStatus.FILLED
            if order.status is CowOrderStatus.expired:
                return OrderStatus.EXPIRED
            msg = f"Unknown order status: {order.status}"
            raise ValueError(msg)

        def from_order_to_rates(
            order: CowOrder,
        ):
            """Similar to from_quote_to_rates but for orders."""
            is_sell = OrderKind(order.kind.value) == OrderKind.SELL
            if order.status is CowOrderStatus.fulfilled:
                # Order is already fulfilled, no need to parse it.
                amount = int(order.executedBuyAmount.root)
                output_human = self.get_token(order.buyToken.root).to_human(int(amount))
            else:
                output_human = self.get_token(order.buyToken.root).to_human(int(order.buyAmount.root))
            input_less_fees_human = self.get_token(order.sellToken.root).to_human(int(order.sellAmount.root))
            calculated_rate = input_less_fees_human / output_human
            inverted_rate = 1 / calculated_rate
            return inverted_rate if not is_sell else calculated_rate

        def from_order_to_amount(order: CowOrder):
            """Convert order to amount."""
            is_sell = OrderKind(order.kind.value) == OrderKind.SELL
            token_a = self.get_token(order.sellToken.root)
            token_b = self.get_token(order.buyToken.root)
            if order.status is CowOrderStatus.fulfilled:
                # Order is already fulfilled, no need to parse it.
                amount = int(order.executedSellAmountBeforeFees.root) if is_sell else int(order.executedBuyAmount.root)
            else:
                amount = int(order.sellAmount.root) if is_sell else int(order.buyAmount.root)
            return token_a.to_human(amount) if is_sell else token_b.to_human(amount)

        wETH = LEDGER_TO_WRAPPER[self.ledger_id]  # noqa: N806

        def weth_address_patcher(order: CowOrder):
            """Temporary monkey patch 🙈."""
            if order.sellToken.root == NATIVE_ETH:
                order.sellToken.root = wETH
                self.logger.debug(f"🐵 Monkey patched CowSwap order sellToken ETH -> wETH: {order}")
            if order.buyToken.root == NATIVE_ETH:
                order.buyToken.root = wETH
                self.logger.debug(f"🐵 Monkey patched CowSwap order buyToken  ETH -> wETH: {order}")

        any(map(weth_address_patcher, orders))  # pay peanuts get monkeys

        return [
            {
                "order": order,
                "symbol": lookup_symbol(order),
                "amount": from_order_to_amount(order),
                "side": get_order_side(order),
                "status": get_order_status(order),
                "price": from_order_to_rates(
                    order,
                ),
            }
            for order in orders
        ]

    async def fetch_open_orders(self, **kwargs):
        """Fetch open orders."""
        account = kwargs.get("params", {}).get("account", self.account.entity.address)

        try:
            orders: list[CowOrder] = await self.order_book_api.get_orders_by_owner(
                owner=account,
            )
        except (httpcore.ReadTimeout, httpx.ReadTimeout, UnexpectedResponseError, SSLWantReadError) as error:
            msg = "CoW Swap API is not available"
            raise ExchangeNotAvailable(msg) from error

        pre_orders = self._process_submitted_orders(orders)

        parsed_orders = [
            self._parse_order(
                **order,
                exchange_id=self.exchange_id,
            )
            for order in pre_orders
        ]
        return Orders(
            orders=parsed_orders,
        )

    async def fetch_positions(self, **kwargs):
        """Fetch positions."""
        raise NotImplementedError

    def __init__(self, ledger_id, rpc_url, key_path, logger, *args, **kwargs):
        super().__init__(ledger_id, rpc_url, key_path, logger, *args, **kwargs)
        self.order_book_api = OrderBookApi()
        self.supported_ledger = SupportedLedgers(ledger_id)
        self.chain = CowChains(LEDGER_TO_COW_CHAIN[self.supported_ledger])
        self.exchange_id = "cowswap"
        env = kwargs.get("env", "prod")
        if env not in get_args(Envs):
            msg = f"Invalid env: {env}. Supported envs: {Envs}"
            raise ValueError(msg)
        self.order_book_api = OrderBookApi(
            OrderBookAPIConfigFactory.get_config(env=env, chain_id=SupportedChainId(self.chain.value[0]))
        )

    @property
    def spender_address(self):
        """Get the spender address."""
        return SPENDER[self.supported_ledger]


class UnsupportedAssetException(Exception):
    """Exception for unsupported asset."""


def check_balance(
    token_address: Address,
    account: Address,
    amount: int,
    ledger_api: EthereumApi,
) -> int:
    """Check the balance of an erc20 token."""
    erc20_contract: Erc20 = load_contract(PublicId.from_str("eightballer/erc_20:0.1.0"))
    balance = erc20_contract.balance_of(
        ledger_api=ledger_api,
        contract_address=token_address,
        account=account,
    )["int"]
    print(f"Balance: {balance}")
    print(f"Amount: {amount}")
    print(f"Balance >= Amount: {balance >= amount}")
    return balance >= amount


@click.command()
@click.option("--ledger_id", help="Chain ID for chain to swap on", default=SupportedLedgers.BASE.value)
@click.option("--src", type=str, help="Source token address: (USDC)", default="USDC")
@click.option("--dst", type=str, help="Destination token address: (olas)", default="OLAS")
@click.option("--amount", type=float, help="Amount of tokens to swap", default=1.0)
def main(
    ledger_id,
    src,
    dst,
    amount,
):
    """Swap tokens using using cowswap.

    Args:
    ----
        ledger_id(str): Ledger ID for chain to swap on
        src(str): Source token symbol
        dst(str): Destination token symbol
        amount(float): Amount of tokens to swap in source token human readable format.

    """

    ledger = SupportedLedgers(ledger_id)

    api = EthereumApi(
        chain_id=LEDGER_TO_CHAIN_ID[ledger],
        address=LEDGER_TO_RPC[ledger],
    )
    crypto = EthereumCrypto(
        private_key_path="ethereum_private_key.txt",
    )

    logger = logging.getLogger(__name__)

    # We make sure to log to the console

    logger.setLevel("INFO")
    logger.addHandler(logging.StreamHandler())
    erc_20 = load_contract(PublicId.from_str("eightballer/erc_20:0.1.0"))

    OrderBookApi()

    buy_token = CowSwapClient.look_up_by_symbol(dst, ledger)
    sell_token = CowSwapClient.look_up_by_symbol(src, ledger)

    amount_to_sell_int = sell_token.to_machine(amount)
    if not buy_token or not sell_token:
        msg = f"Invalid token symbols: {src}, {dst}"
        raise InvalidSwapParams(msg)

    print(f"Swapping (int)      {amount_to_sell_int} {src} for {dst}")
    print(f"Spending (decimals) {amount} {src}")

    if not check_balance(
        amount=amount_to_sell_int, ledger_api=api, account=crypto.address, token_address=sell_token.address
    ):
        msg = f"Insufficient balance to fill {src}: {amount}"
        raise InsufficientBalance(msg)

    allowance = get_allowance(erc_20, api, sell_token.address, crypto.address, SPENDER[ledger])
    print(f"Current allowance: {allowance}")
    if allowance < amount:
        print(f"Allowance is sufficient: {allowance} > {amount}")
        result = increase_allowance(
            token_address=sell_token.address,
            spender=SPENDER[ledger],
            amount=amount * 1e18,
            ledger_api=api,
            crypto=crypto,
        )
        if not result:
            msg = "Failed to increase allowance"
            raise InsufficientAllowance(msg)

    if input(f"Proceed with swap of {amount} {src} for {dst}? (y/n)").lower() != "y":
        return
    click.echo(f"Performing swap of {amount} {src} for {dst}")

    print(f""""
    amount={amount_to_sell_int},
    buy_token={buy_token.address},
    sell_token={sell_token.address},
    chain={LEDGER_TO_COW_CHAIN[ledger]},
    account={crypto.entity},
    """)

    order_book_api = OrderBookApi(
        OrderBookAPIConfigFactory.get_config(
            env="prod",
            chain_id=SupportedChainId(LEDGER_TO_COW_CHAIN[ledger].value[0]),
        )
    )

    open_orders = asyncio.run(
        order_book_api.get_orders_by_owner(
            owner=crypto.entity.address,
        )
    )
    print(f"Open orders: {open_orders}")

    order_status = asyncio.run(
        order_book_api.get_order_by_uid(
            order_uid=open_orders[0].uid if open_orders else None,
        )
    )
    print(f"Order status: {order_status}")

    order = asyncio.run(
        swap_tokens(
            order_book_api=order_book_api,
            amount=amount_to_sell_int,
            buy_token=buy_token.address,
            sell_token=sell_token.address,
            chain=LEDGER_TO_COW_CHAIN[ledger],
            account=crypto.entity,
            app_data=APP_DATA,
            slippage_tolerance=SLIPPAGE_TOLERANCE,
        )
    )

    print(f"Order UID: {order.uid}")
    print(f"Order URL: {order.url}")


if __name__ == "__main__":
    main()
