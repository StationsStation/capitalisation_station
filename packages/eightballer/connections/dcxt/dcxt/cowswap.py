"""CowSwap client for swapping tokens on the CowSwap DEX."""

import asyncio
import logging
import datetime
import warnings
from functools import lru_cache

import rich_click as click
from rich import print
from web3 import Account
from aea_ledger_ethereum import Address, EthereumApi, EthereumCrypto
from cowdao_cowpy.cow.swap import Order as CowOrder, swap_tokens, get_order_quote
from aea.configurations.base import PublicId
from cowdao_cowpy.common.chains import Chain as CowChains
from cowdao_cowpy.common.config import SupportedChainId
from cowdao_cowpy.order_book.api import OrderBookApi
from cowdao_cowpy.common.constants import ZERO_APP_DATA, CowContractAddress
from cowdao_cowpy.common.api.errors import UnexpectedResponseError
from cowdao_cowpy.order_book.config import OrderBookAPIConfigFactory
from cowdao_cowpy.order_book.generated.model import (
    TokenAmount,
    OrderQuoteSide1,
    OrderQuoteRequest,
    OrderQuoteSideKindSell,
)

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus
from packages.eightballer.connections.dcxt.dcxt.one_inch import (
    InvalidSwapParams,
    InsufficientBalance,
    InsufficientAllowance,
    get_allowance,
    increase_allowance,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.connections.dcxt.dcxt.exceptions import RpcError
from packages.eightballer.connections.dcxt.erc_20.contract import Erc20, Erc20Token
from packages.eightballer.connections.dcxt.dcxt.data.tokens import SupportedLedgers
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import BaseErc20Exchange, read_token_list


MAX_ORDER_ATTEMPTS = 3
SLIPPAGE_TOLERANCE = 0.0005
# 1bps fee applied to all trades
APP_DATA = ZERO_APP_DATA
SPENDER = {
    SupportedLedgers.ETHEREUM: CowContractAddress.VAULT_RELAYER.value,
    SupportedLedgers.GNOSIS: CowContractAddress.VAULT_RELAYER.value,
    SupportedLedgers.BASE: CowContractAddress.VAULT_RELAYER.value,
    SupportedLedgers.ARBITRUM: CowContractAddress.VAULT_RELAYER.value,
}
LEDGER_TO_CHAIN_ID = {
    SupportedLedgers.ETHEREUM: CowChains.MAINNET.value[0].value,
    SupportedLedgers.GNOSIS: CowChains.GNOSIS.value[0].value,
    SupportedLedgers.BASE: CowChains.BASE.value[0].value,
    SupportedLedgers.ARBITRUM: CowChains.ARBITRUM_ONE.value[0].value,
}

LEDGER_TO_COW_CHAIN = {
    SupportedLedgers.ETHEREUM: CowChains.MAINNET,
    SupportedLedgers.GNOSIS: CowChains.GNOSIS,
    SupportedLedgers.BASE: CowChains.BASE,
    SupportedLedgers.ARBITRUM: CowChains.ARBITRUM_ONE,
}

LEDGER_TO_RPC = {
    SupportedLedgers.ETHEREUM: "https://eth.drpc.org",
    SupportedLedgers.GNOSIS: "https://gnosis.drpc.org",
    SupportedLedgers.BASE: "https://base.drpc.org",
    SupportedLedgers.ARBITRUM: "https://arbitrum.drpc.org",
}

warnings.filterwarnings("ignore", category=UserWarning)


async def get_quote(
    buy_token: Erc20Token,
    sell_token: Erc20Token,
    sell_amount_int: int,
    chain: CowChains,
    account: Account,
    order_book_api: OrderBookApi,
):
    """Get a quote for a token swap."""
    chain_id = SupportedChainId(chain.value[0])
    order_book_api = OrderBookApi(OrderBookAPIConfigFactory.get_config(env="prod", chain_id=chain_id))

    order_quote_request = OrderQuoteRequest(
        sellToken=sell_token.address,
        buyToken=buy_token.address,
        from_=account.address,  # type: ignore # pyright doesn't recognize `populate_by_name=True`.
    )
    order_side = OrderQuoteSide1(
        kind=OrderQuoteSideKindSell.sell,
        sellAmountBeforeFee=TokenAmount(str(sell_amount_int)),
    )

    return await get_order_quote(order_quote_request, order_side, order_book_api)


class CowSwapClient(BaseErc20Exchange):
    """Class for interacting with the 1inch API."""

    def _parse_order(
        self,
        order: CowOrder,
        exchange_id: str,
        symbol: str,
        price: float,
        amount: float,
        side: OrderSide,
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
            type=OrderType.MARKET,
            status=OrderStatus.OPEN,
        )
        self.logger.info(f"Parsed Order: {order}")
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
                account=self.account.entity,
                order_book_api=self.order_book_api,
            )
        except UnexpectedResponseError as error:
            self.logger.exception(f"Failed to get quote: {error}")
            raise RpcError from error

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

    async def fetch_open_orders(self, **kwargs):
        """Fetch open orders."""
        raise NotImplementedError

    async def fetch_positions(self, **kwargs):
        """Fetch positions."""
        raise NotImplementedError

    def __init__(self, ledger_id, rpc_url, key_path, logger, *args, **kwargs):
        super().__init__(ledger_id, rpc_url, key_path, logger, *args, **kwargs)
        self.order_book_api = OrderBookApi()
        self.supported_ledger = SupportedLedgers(ledger_id)
        self.chain = CowChains(LEDGER_TO_COW_CHAIN[self.supported_ledger])
        self.exchange_id = "cowswap"

    @classmethod
    @lru_cache(
        maxsize=128,
    )
    def look_up_by_symbol(cls, symbol: str, ledger: SupportedLedgers) -> Erc20Token:
        """Look up a token by symbol."""
        token_list = read_token_list(LEDGER_TO_CHAIN_ID[ledger])
        for token, data in token_list.items():
            if data["symbol"] == symbol:
                return Erc20Token(
                    address=token,
                    symbol=data["symbol"],
                    decimals=data["decimals"],
                    name=data["name"],
                )
        return None


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

    order = asyncio.run(
        swap_tokens(
            amount=amount_to_sell_int,
            buy_token=buy_token.address,
            sell_token=sell_token.address,
            chain=LEDGER_TO_COW_CHAIN[ledger],
            account=crypto.entity,
            app_data=ZERO_APP_DATA,
            slippage_tolerance=SLIPPAGE_TOLERANCE,
        )
    )

    print(f"Order UID: {order.uid}")
    print(f"Order URL: {order.url}")


if __name__ == "__main__":
    main()
