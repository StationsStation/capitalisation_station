"""Nabla Finance client for swapping tokens on the Nabla Finance DEX."""

import json
import datetime
from typing import Any, Literal
from pathlib import Path
from functools import lru_cache

import requests
from pydantic import BaseModel
from web3.exceptions import TimeExhausted
from aea.configurations.base import PublicId

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.orders.custom_types import (
    Order,
    Orders,
    OrderSide,
    OrderType,
    OrderStatus,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.connections.dcxt.dcxt.exceptions import UnsupportedAsset
from packages.eightballer.connections.dcxt.dcxt.data.tokens import SupportedLedgers
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import (
    BaseErc20Exchange,
    signed_tx_to_dict,
    try_send_signed_transaction,
)


# ruff: noqa: ARG002

ZERO_PRICE_FEED = "0000000000000000000000000000000000000000000000000000000000000000"
MULTICALL3_ADDRESS = "0xcA11bde05977b3631167028862bE2a173976CA11"


class Pool(BaseModel):
    """Pool."""

    ADDRESS: str
    NAME: str
    SYMBOL: str
    DECIMALS: int
    ASSET: str
    ASSET_ADDRESS: str


class MainCryptoHub(BaseModel):
    """MainCryptoHub."""

    ROUTER: str
    POOLS: dict[str, Pool]
    BACKSTOP_POOL: Pool


class NablaLedgerConfig(BaseModel):
    """NablaLedgerConfig."""

    PORTAL: str
    PYTH_ADAPTER_V2: str
    ORACLE: str
    MAIN_CRYPTO_HUB: MainCryptoHub
    NABLA_DRIP: str
    STAKING: str | None = None  # missing on ARBITRUM
    NABLA_QUOTE: str | None = None


class NablaConfig(BaseModel):
    """NablaConfig."""

    BASE: NablaLedgerConfig
    ARBITRUM: NablaLedgerConfig

    @classmethod
    def load(cls):
        """Load the configuration."""
        path = Path(__file__).parent / "data" / "nabla" / "config.json"
        return cls(**json.loads(path.read_text()))

    def __getitem__(self, key: str) -> NablaLedgerConfig:
        """Dynamic lookup by key."""
        try:
            return getattr(self, key)
        except AttributeError as e:
            raise KeyError(key) from e


class Price(BaseModel):
    """Price."""

    price: int
    publish_time: int


class ParsedEntry(BaseModel):
    """ParsedEntry."""

    id: str
    metadata: dict[str, Any]
    price: Price


class BinaryData(BaseModel):
    """BinaryData."""

    data: list[str]
    encoding: Literal["hex"]


class PriceFeedResponse(BaseModel):
    """PriceFeedResponse."""

    binary: BinaryData
    parsed: list[ParsedEntry]
    feed_to_address: dict[str, str]

    @property
    def prices(self) -> dict[str, int]:
        """Returns a mapping from price-feed ID to price value."""
        return {entry.id: entry.price.price for entry in self.parsed}

    @property
    def token_prices(self) -> dict[str, int]:
        """Returns a mapping from token address to price value."""
        return {self.feed_to_address[fid]: price for fid, price in self.prices.items() if fid in self.feed_to_address}

    @property
    def price_update_data(self) -> str:
        """Returns the concatenated hex string with '0x' prefix."""
        return "0x" + "".join(self.binary.data)


NABLA_CONFIG = NablaConfig.load()
NABLA_PORTAL_PUBLIC_ID = "dakavon/nabla_portal:0.1.0"
NABLA_QUOTE_PUBLIC_ID = "dakavon/nabla_quote:0.1.0"
MULTICALL3_PUBLIC_ID = "dakavon/multicall3:0.1.0"
NABLA_DIRECT_PRICE_ORACLE_ID = "zarathustra/direct_price_oracle:0.1.0"
NABLA_PRICE_API_URL: str = "https://antenna.nabla.fi/v1/updates/price/latest"


class NablaFinanceClient(BaseErc20Exchange):
    """Class for interacting with the Nabla Finance API."""

    exchange_id = "nabla"

    @property
    def spender_address(self):
        """Spender address."""
        return self.config.PORTAL

    @property
    def router_address(self):
        """Router address."""
        return self.config.MAIN_CRYPTO_HUB.ROUTER

    @property
    def nabla_quote_address(self):
        """Nabla quote address."""
        return self.config.NABLA_QUOTE

    def __init__(self, ledger_id, rpc_url, key_path, logger, *args, **kwargs):
        super().__init__(
            *args,
            ledger_id=ledger_id,
            rpc_url=rpc_url,
            key_path=key_path,
            logger=logger,
            **kwargs,
        )
        self.supported_ledger = SupportedLedgers(ledger_id)
        self.config = NABLA_CONFIG[self.supported_ledger.name]
        self.direct_price_oracle = load_contract(PublicId.from_str(NABLA_DIRECT_PRICE_ORACLE_ID))
        self.nabla_price_feed_ids = {}  # Cache for asset (string) to price feed ID (bytes32)

    async def close(self):
        """Close the client."""

    @lru_cache(maxsize=128)  # noqa: B019
    def get_price_feed_id(self, asset_address: str) -> str:
        """Get price feed id."""
        asset = self.direct_price_oracle.address_to_asset(
            ledger_api=self.web3,
            contract_address=self.config.ORACLE,
            var_0=asset_address,
        )["str"]

        price_feed_id = self.direct_price_oracle.asset_to_price_feed_id(
            ledger_api=self.web3,
            contract_address=self.config.ORACLE,
            var_0=asset,
        )["str"]

        if price_feed_id == ZERO_PRICE_FEED:
            msg = f"No price feed found for asset {asset_address} ({asset})"
            self.logger.error(msg)
            raise UnsupportedAsset(msg)

        self.nabla_price_feed_ids[asset_address] = price_feed_id

        return self.nabla_price_feed_ids[asset_address]

    async def get_ask_bid(
        self,
        amount: float,
        asset_a: str,
        asset_b: str,
    ) -> tuple[float, float]:
        """Quote a swap both ways and return (ask_price, bid_price).

        ask_price = amount of B you get per 1 A (sell A → B)
        bid_price = amount of A you get per 1 B (sell B → A)
        """
        # fetch price data once
        price_feed_response = self.fetch_price_data([asset_a, asset_b])
        token_a = self.get_token(asset_a)
        token_b = self.get_token(asset_b)
        token_prices = price_feed_response.token_prices

        # helper to call get_swap_quote
        async def quote(from_addr: str, to_addr: str, amt_units: int) -> int:
            return await self.get_swap_quote(
                from_token_address=from_addr,
                to_token_address=to_addr,
                amount=amt_units,
                token_prices=token_prices,
            )

        # 1) quote(A → B) is the bid price (B per A)
        units_a = int(amount * 10**token_a.decimals)
        out_b_units = await quote(asset_a, asset_b, units_a)
        out_b = out_b_units / 10**token_b.decimals
        bid_price = out_b / amount  # B per A

        self.logger.info(
            "Bid quote %s→%s: %.6f %s → %.6f %s; bid = %.6f %s/%s",
            token_a.symbol,
            token_b.symbol,
            amount,
            token_a.symbol,
            out_b,
            token_b.symbol,
            bid_price,
            token_b.symbol,
            token_a.symbol,
        )

        # 2) quote(B → A) inverted is the ask price (B per A)
        units_b = int(out_b * 10**token_b.decimals)
        out_a_units = await quote(asset_b, asset_a, units_b)
        out_a = out_a_units / 10**token_a.decimals
        ask_price = out_b / out_a  # B per A

        self.logger.info(
            "Ask quote %s→%s: %.6f %s → %.6f %s; ask = %.6f %s/%s",
            token_b.symbol,
            token_a.symbol,
            out_b,
            token_b.symbol,
            out_a,
            token_a.symbol,
            ask_price,
            token_b.symbol,
            token_a.symbol,
        )

        return ask_price, bid_price

    async def get_nabla_quote(
        self,
        amount: float,
        asset_a: str,
        asset_b: str,
    ) -> tuple[float, float]:
        """Fetches a swap quote from NablaQuote contract and returns (ask_price, bid_price).

        NablaQuote contract interface:
            quote(
                uint256 _amountIn,
                address[] calldata _tokenPath,
                address[] calldata _routerPath,
                uint256[] calldata _tokenPrices
            ) external view returns (uint256 bidAmountOut_, uint256 askAmountOut_)

        Returns
        -------
            ask_price = amount of B you get per 1 A (buy A ← B)
            bid_price = amount of B you get per 1 A (sell A → B)

        """
        # fetch price data
        price_feed_response = self.fetch_price_data([asset_a, asset_b])
        token_a = self.get_token(asset_a)
        token_b = self.get_token(asset_b)
        token_prices = price_feed_response.token_prices

        # load the NablaQuote contract
        nabla_quote_contract = load_contract(PublicId.from_str(NABLA_QUOTE_PUBLIC_ID))
        params = {
            "amount_in": int(amount * 10**token_a.decimals),
            "token_path": [token_a.address, token_b.address],
            "router_path": [self.router_address],
            "token_prices": [
                token_prices[token_a.address],
                token_prices[token_b.address],
            ],
        }

        # call the quote function on the NablaQuote contract
        nabla_quote = nabla_quote_contract.quote(
            ledger_api=self.web3,
            contract_address=self.nabla_quote_address,
            **params,
        )

        # 1) BID price: Quote (sell A → B), i.e. market buy price for B using A
        amount_out_token_b_units = nabla_quote["bidAmountOut_"]
        amount_out_token_b = amount_out_token_b_units / 10**token_b.decimals
        bid_price = amount_out_token_b / amount  # B per A ($B/$A)

        self.logger.debug(
            "### BID quote $%s → $%s: %.6f $%s → %.6f $%s; bid_price = %.6f $%s/$%s",
            token_a.symbol,
            token_b.symbol,
            amount,
            token_a.symbol,
            amount_out_token_b,
            token_b.symbol,
            bid_price,
            token_b.symbol,
            token_a.symbol,
        )

        # ASK price: Quote (buy A ← B), i.e. market sell price for B using A
        amount_out_token_a_units = nabla_quote["askAmountOut_"]
        amount_out_token_a = amount_out_token_a_units / 10**token_a.decimals
        ask_price = amount_out_token_b / amount_out_token_a  # B per A ($B/$A)

        self.logger.debug(
            "### ASK quote $%s → $%s: %.6f $%s → %.6f $%s; ask_price = %.6f $%s/$%s",
            token_b.symbol,
            token_a.symbol,
            amount_out_token_b,
            token_b.symbol,
            amount_out_token_a,
            token_a.symbol,
            ask_price,
            token_b.symbol,
            token_a.symbol,
        )

        return ask_price, bid_price

    async def convert_amount(
        self,
        from_amount: int,
        from_price: float,
        to_price: float,
        from_token_decimals: int,
        to_token_decimals: int,
    ) -> int:
        """Price conversion from one token to another.

        Args:
        ----
            from_amount (int): Amount of the from token.
            from_price (float): Price of the from token in USD.
            to_price (float): Price of the to token in USD.
            from_token_decimals (int): Decimals of the from token.
            to_token_decimals (int): Decimals of the to token.

        Returns:
        -------
            int: Equivalent amount in the to token.

        """
        return from_amount * (from_price / to_price) / (10 ** (from_token_decimals - to_token_decimals))

    async def get_orderbook(self, asset_a: str, asset_b: str, amounts: list[float]) -> list[tuple[float, float]]:  # noqa: PLR0914
        """Get the orderbook for a given token pair.

        Args:
        ----
            from_token_address (str): Address of the token to swap from.
            to_token_address (str): Address of the token to swap to.
            amounts (list[float]): List of amounts to get quotes for.

        Returns:
        -------
            list[tuple[float, float]]: List of tuples containing (ask_price, bid_price) for each amount.

        """
        # fetch price data
        price_feed_response = self.fetch_price_data([asset_a, asset_b])
        token_a = self.get_token(asset_a)
        token_b = self.get_token(asset_b)
        token_prices = price_feed_response.token_prices

        # load the Multicall3 contract
        multicall3_contract = load_contract(PublicId.from_str(MULTICALL3_PUBLIC_ID))
        # load the NablaQuote contract
        nabla_quote_contract = load_contract(PublicId.from_str(NABLA_QUOTE_PUBLIC_ID))

        # Prepare the calls for the Multicall3 contract
        bid_amounts = []
        ask_amounts = []
        call3s = []
        quotes = []

        for amount in amounts:
            # Prepare amounts in token units
            bid_amount_in = int(amount * 10**token_a.decimals)
            ask_amount_in = int(
                await self.convert_amount(
                    from_amount=bid_amount_in,
                    from_price=token_prices[token_a.address],
                    to_price=token_prices[token_b.address],
                    from_token_decimals=token_a.decimals,
                    to_token_decimals=token_b.decimals,
                )
            )

            # Save bid/ask amounts in decimals
            bid_amounts.append(amount)
            ask_amounts.append(ask_amount_in / 10**token_b.decimals)

            params = {
                "bid_amount_in": bid_amount_in,
                "ask_amount_in": ask_amount_in,
                "token_path": [token_a.address, token_b.address],
                "router_path": [self.router_address],
                "token_prices": [
                    token_prices[token_a.address],
                    token_prices[token_b.address],
                ],
            }

            nabla_quote_calldata = nabla_quote_contract.quote_with_reference_price_calldata(
                ledger_api=self.web3,
                contract_address=self.nabla_quote_address,
                **params,
            )

            quote_call3_struct = {
                "target": self.nabla_quote_address,
                "allowFailure": True,
                "callData": nabla_quote_calldata,
            }

            call3s.append(quote_call3_struct)

        # Call the Multicall3 contract to aggregate the quotes
        multicall3_quotes_calldata = multicall3_contract.aggregate3(
            ledger_api=self.web3, contract_address=MULTICALL3_ADDRESS, calls=call3s
        )
        multicall3_quotes_returned = multicall3_quotes_calldata.call()

        # Decode the multicall3 returned data
        for i, (success, returned_data) in enumerate(multicall3_quotes_returned):
            if not success:
                self.logger.error(f"Multicall3 call {i} for amount {bid_amounts[i]} failed.")
                quotes.append((None, None))
                continue

            if len(returned_data) < 64:
                self.logger.error(f"Multicall3 call {i} for amount {bid_amounts[i]} returned unexpected data length.")
                quotes.append((None, None))
                continue

            # Decode bid and ask as uint256
            amount_out_token_b_units = int.from_bytes(returned_data[:32], byteorder="big")
            amount_out_token_a_units = int.from_bytes(returned_data[32:64], byteorder="big")

            # Convert to decimals
            amount_out_token_b = amount_out_token_b_units / 10**token_b.decimals
            amount_out_token_a = amount_out_token_a_units / 10**token_a.decimals

            # BID price: Quote (sell A → B), i.e. market buy price for B using A, i.e. B per A ($B/$A)
            bid_price = amount_out_token_b / bid_amounts[i] if bid_amounts[i] != 0.0 else 0.0

            self.logger.info(
                "### BID quote $%s → $%s: %.6f $%s → %.6f $%s; bid_price = %.6f $%s/$%s",
                token_a.symbol,
                token_b.symbol,
                bid_amounts[i],
                token_a.symbol,
                amount_out_token_b,
                token_b.symbol,
                bid_price,
                token_b.symbol,
                token_a.symbol,
            )

            # ASK price: Quote (buy A ← B), i.e. market sell price for B using A, i.e. B per A ($B/$A)

            ask_price = ask_amounts[i] / amount_out_token_a if amount_out_token_a != 0.0 else 0.0

            self.logger.info(
                "### ASK quote $%s → $%s: %.6f $%s → %.6f $%s; ask_price = %.6f $%s/$%s",
                token_b.symbol,
                token_a.symbol,
                ask_amounts[i],
                token_b.symbol,
                amount_out_token_a,
                token_a.symbol,
                ask_price,
                token_b.symbol,
                token_a.symbol,
            )

            quotes.append(
                (
                    ask_price if ask_price != 0.0 else None,
                    bid_price if bid_price != 0.0 else None,
                )
            )

        return quotes or [(None, None)] * len(amounts)

    async def fetch_ticker(
        self,
        symbol: str | None = None,
        asset_a: str | None = None,
        asset_b: str | None = None,
        params: dict | None = None,
    ) -> Ticker:
        """Fetches a ticker with live ask/bid from on-chain quotes."""

        if all([symbol is None, asset_a is None or asset_b is None]):
            msg = "Either symbol or asset_a and asset_b must be provided"
            raise ValueError(msg)

        if symbol is None:
            symbol = f"{asset_a}/{asset_b}"

        a_sym, b_sym = symbol.split("/")
        asset_a = self.look_up_by_symbol(a_sym, ledger=self.supported_ledger)
        asset_b = self.look_up_by_symbol(b_sym, ledger=self.supported_ledger)

        if not asset_a or not asset_b:
            msg = f"Could not find token addresses for `{asset_a}` and `{asset_b}` " f"with symbols {a_sym} and {b_sym}"
            raise ValueError(msg)

        # get live ask/bid for X units of asset A from NablaQuote contract
        amount = params.get("amount", 0.5) if params is not None else 0.5

        orderbook = await self.get_orderbook(asset_a=asset_a.address, asset_b=asset_b.address, amounts=[amount])
        ask, bid = orderbook[0] if orderbook else (0.0, 0.0)

        ts = datetime.datetime.now(tz=datetime.UTC)
        return Ticker(
            symbol=symbol,
            asset_a=asset_a.address,
            asset_b=asset_b.address,
            high=ask,
            low=bid,
            ask=ask,
            bid=bid,
            timestamp=int(ts.timestamp()),
            datetime=ts.isoformat(),
        )

    def parse_order(self, order, *args, **kwargs) -> Order:
        """Parse the order."""
        return order

    async def fetch_positions(self, **kwargs) -> list:
        """Fetch positions."""
        return []

    async def fetch_tickers(self, *args, **kwargs):
        """Fetch all tickers."""

        return Tickers(tickers=[])

    async def create_order(
        self,
        *,
        asset_a: str,
        asset_b: str,
        side: str,
        amount: float,
        retries: int = 0,
        symbol: str | None = None,
        price: float | None = None,
        type: str = "market",
        data: dict[str, Any] | None = None,
        **kwargs,
    ):
        """Create an order."""

        price_feed_response = self.fetch_price_data([asset_a, asset_b])
        token_a = self.get_token(asset_a)
        token_b = self.get_token(asset_b)

        decimals = token_a.decimals if side == "sell" else token_b.decimals
        from_token_address = asset_a if side == "sell" else asset_b
        to_token_address = asset_b if side == "sell" else asset_a
        amt = int(amount * 10**decimals)

        if side == "buy":
            amt *= price

        output_token_amount = await self.get_swap_quote(
            from_token_address=from_token_address,
            to_token_address=to_token_address,
            amount=amt,
            token_prices=price_feed_response.token_prices,
        )
        nabla_portal_contract = load_contract(PublicId.from_str(NABLA_PORTAL_PUBLIC_ID))

        swap_fn = nabla_portal_contract.swap_exact_tokens_for_tokens(
            ledger_api=self.web3,
            contract_address=self.spender_address,
            amount_in=int(amt),
            amount_out_min=int(output_token_amount),
            token_path=[from_token_address, to_token_address],
            router_path=[self.router_address],
            deadline=int(datetime.datetime.now(tz=datetime.UTC).timestamp() + 36_000),
            to=self.account.address,
            price_update_data=[price_feed_response.price_update_data],
        )

        swap_tx = swap_fn.build_transaction(
            {
                "from": self.account.address,
                "nonce": self.web3.api.eth.get_transaction_count(self.account.address),
                "gas": 850_000,
                "gasPrice": int(self.web3.api.eth.gas_price * 1.1),
            }
        )
        self.logger.info("Built swap transaction", extra={"tx": swap_tx})
        signed_tx = signed_tx_to_dict(self.account.entity.sign_transaction(swap_tx))
        tx_hash = try_send_signed_transaction(self.web3, signed_tx, raise_on_try=True)

        try:
            receipt = self.web3.api.eth.wait_for_transaction_receipt(tx_hash, timeout=60, poll_latency=1)
            if receipt.get("status") == 1:
                self.logger.info(
                    "Transaction succeeded",
                    extra={
                        "tx_hash": tx_hash,
                        "blockNumber": receipt.get("blockNumber"),
                    },
                )
                status = OrderStatus.FILLED
            else:
                self.logger.info("Transaction failed on-chain", extra={"receipt": receipt})
                status = OrderStatus.FAILED
        except TimeExhausted:
            self.logger.exception(f"Timeout waiting for transaction receipt: {tx_hash}")
            receipt = None

        return Order(
            exchange_id=self.exchange_id.lower(),
            ledger_id=self.supported_ledger.name.lower(),
            symbol=symbol,
            price=price,
            side=OrderSide[side.upper()],
            id=tx_hash,
            type=OrderType[type.upper()],
            status=status,
            amount=amount if side == OrderSide.SELL.name.lower() else amount / price,
        )

    async def fetch_open_orders(self, **kwargs):
        """Fetch open orders."""

        parsed_orders = []
        return Orders(
            orders=parsed_orders,
        )

    async def get_swap_quote(
        self,
        from_token_address: str,
        to_token_address: str,
        amount: int,
        token_prices: dict[str, int],
    ) -> int:
        """Get a swap quote from the Nabla Finance AMM.

            function quoteSwapExactTokensForTokens(
                uint256 _amountIn,
                address[] _tokenPath,
                address[] _routerPath,
                uint256[] _tokenPrices
            ) external view returns (uint256 amountOut_)


        Args:
        ----
            from_token_address (str): Address of the token to swap from.
            to_token_address (str): Address of the token to swap to.
            amount (int): Amount of the from token in smallest unit (e.g., wei).
            token_prices (Dict[str, int]): Mapping of token addresses to their prices

        Returns:
        -------
            int: Amount of the to token that will be received in the swap.

        """

        nabla_portal_contract = load_contract(PublicId.from_str(NABLA_PORTAL_PUBLIC_ID))
        token_prices = [
            token_prices[from_token_address],
            token_prices[to_token_address],
        ]
        params = {
            "amount_in": int(amount),
            "token_path": [from_token_address, to_token_address],
            "router_path": [self.router_address],
            "token_prices": token_prices,
        }
        swap_amount_out = nabla_portal_contract.quote_swap_exact_tokens_for_tokens(
            ledger_api=self.web3,
            contract_address=self.spender_address,
            **params,
        )
        return swap_amount_out["amountOut_"]

    def fetch_price_data(self, asset_addresses) -> PriceFeedResponse:
        """Fetch price data from the Nabla Finance API.

        Args:
        ----
            asset_addresses (List[str]): List of asset addresses to fetch prices for.

        Returns:
        -------
            Dict: {
                "prices": Dict[str, int],  # Mapping from price feed ID to price
                "priceUpdateData": str     # Hex string with 0x prefix
            }

        """

        price_feeds = {addr: self.get_price_feed_id(addr) for addr in asset_addresses}
        feed_to_address = {feed_id.hex(): addr for addr, feed_id in price_feeds.items()}

        params = [("ids[]", id_) for id_ in price_feeds.values()]
        response = requests.get(NABLA_PRICE_API_URL, data=params, timeout=10)

        if response.status_code != 200:
            msg = f"Failed to fetch price data: {response.status_code} - {response.text}"
            raise ValueError(msg)

        payload = {**response.json(), "feed_to_address": feed_to_address}
        return PriceFeedResponse.parse_obj(payload)
