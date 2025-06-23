"""Nabla Finance client for swapping tokens on the Nabla Finance DEX."""

import json
import datetime
from pathlib import Path

import requests
from pydantic import BaseModel
from web3.exceptions import TimeExhausted
from aea.configurations.base import PublicId

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.orders.custom_types import (
    Order,
    Orders,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.connections.dcxt.dcxt.data.tokens import SupportedLedgers
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import (
    BaseErc20Exchange,
    signed_tx_to_dict,
    try_send_signed_transaction,
)


class Pool(BaseModel):
    ADDRESS: str
    NAME: str
    SYMBOL: str
    DECIMALS: int
    ASSET: str
    ASSET_ADDRESS: str


class MainCryptoHub(BaseModel):
    ROUTER: str
    POOLS: dict[str, Pool]
    BACKSTOP_POOL: Pool


class NablaLedgerConfig(BaseModel):
    PORTAL: str
    PYTH_ADAPTER_V2: str
    ORACLE: str
    MAIN_CRYPTO_HUB: MainCryptoHub
    NABLA_DRIP: str
    STAKING: str | None = None  # missing on ARBITRUM


class NablaConfig(BaseModel):
    BASE: NablaLedgerConfig
    ARBITRUM: NablaLedgerConfig

    @classmethod
    def load(cls):
        path = Path(__file__).parent / "data" / "nabla" / "config.json"
        return cls(**json.loads(path.read_text()))

    def __getitem__(self, key: str) -> NablaLedgerConfig:
        try:
            return getattr(self, key)
        except AttributeError as e:
            raise KeyError(key) from e


NABLA_CONFIG = NablaConfig.load()

NABLA_PORTAL_PUBLIC_ID = "dakavon/nabla_portal:0.1.0"

LEDGER_ASSET_ADDRESS_TO_PRICE_FEED_ID: dict[SupportedLedgers, dict[str, str]] = {
    SupportedLedgers.BASE: {
        "0x4200000000000000000000000000000000000006": "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",
        "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf": "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
        "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913": "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a",
    },
    SupportedLedgers.ARBITRUM: {
        "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",
        "0xaf88d065e77c8cC2239327C5EDb3A432268e5831": "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a",
    },
}

PRICE_FEED_ID_TO_ASSET_ADDRESS: dict[str, str] = {
    SupportedLedgers.BASE: {
        "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace": "0x4200000000000000000000000000000000000006",  # WETH
        "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
        "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    },
    SupportedLedgers.ARBITRUM: {
        "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",  # WETH
        "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43": "",  # cbBTC
        "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  # USDC
    },
}

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

    async def close(self):
        """Close the client."""

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
        price_data = self.fetch_price_data([asset_a, asset_b])
        token_a = self.get_token(asset_a)
        token_b = self.get_token(asset_b)
        token_prices = price_data["prices"]

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

        return bid_price, ask_price

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
            msg = (
                f"Could not find token addresses for `{asset_a}` and `{asset_b}` "
                f"with symbols {a_sym} and {b_sym}"
            )
            raise ValueError(msg)

        # get live ask/bid for X units of asset A
        amount = params.get("amount", 0.5) if params is not None else 0.5
        bid, ask = await self.get_ask_bid(
            amount=amount, asset_a=asset_a.address, asset_b=asset_b.address
        )

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

    def fetch_tickers(self, *args, **kwargs):
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
    ):
        """Create an order."""
        price_data = self.fetch_price_data([asset_a, asset_b])
        token_a = self.get_token(asset_a)
        token_b = self.get_token(asset_b)

        token_prices = price_data["prices"]
        price_update_data = price_data["priceUpdateData"]

        decimals = token_a.decimals if side == "sell" else token_b.decimals
        from_token_address = asset_a if side == "sell" else asset_b
        to_token_address = asset_b if side == "sell" else asset_a
        amt = int(amount * 10**decimals)

        output_token_amount = await self.get_swap_quote(
            from_token_address=from_token_address,
            to_token_address=to_token_address,
            amount=amt,
            token_prices=token_prices,
        )
        nabla_portal_contract = load_contract(PublicId.from_str(NABLA_PORTAL_PUBLIC_ID))

        swap_fn = nabla_portal_contract.swap_exact_tokens_for_tokens(
            ledger_api=self.web3,
            contract_address=self.spender_address,
            amount_in=amt,
            amount_out_min=output_token_amount,
            token_path=[from_token_address, to_token_address],
            router_path=[self.router_address],
            deadline=int(datetime.datetime.now(tz=datetime.UTC).timestamp() + 36_000),
            to=self.account.address,
            price_update_data=[price_update_data],
        )

        swap_tx = swap_fn.build_transaction(
            {
                "from": self.account.address,
                "nonce": self.web3.api.eth.get_transaction_count(self.account.address),
                "gas": 750_000,
                "gasPrice": int(self.web3.api.eth.gas_price * 1.1),
            }
        )
        self.logger.debug("Built swap transaction", extra={"tx": swap_tx})
        signed_tx = signed_tx_to_dict(self.account.entity.sign_transaction(swap_tx))
        self.logger.info(f"Signed transaction: {signed_tx}")
        tx_hash = try_send_signed_transaction(self.web3, signed_tx, raise_on_try=True)
        self.logger.info(f"Transaction hash: {tx_hash}")

        try:
            receipt = self.web3.api.eth.wait_for_transaction_receipt(
                tx_hash, timeout=60, poll_latency=1
            )
            if receipt.get("status") == 1:
                self.logger.info(
                    "Transaction succeeded",
                    extra={
                        "tx_hash": tx_hash,
                        "blockNumber": receipt.get("blockNumber"),
                    },
                )
            else:
                self.logger.info(
                    "Transaction failed on-chain", extra={"receipt": receipt}
                )
        except TimeExhausted:
            self.logger.exception(f"Timeout waiting for transaction receipt: {tx_hash}")
            receipt = None

        return receipt

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
        swap_amount_out = nabla_portal_contract.quote_swap_exact_tokens_for_tokens(
            ledger_api=self.web3,
            contract_address=self.spender_address,
            amount_in=amount,
            token_path=[from_token_address, to_token_address],
            router_path=[self.router_address],
            token_prices=token_prices,
        )
        return swap_amount_out["amountOut_"]

    def fetch_price_data(self, asset_addresses) -> dict:
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

        params = [
            (
                "ids[]",
                LEDGER_ASSET_ADDRESS_TO_PRICE_FEED_ID[self.supported_ledger][
                    asset_address
                ],
            )
            for asset_address in asset_addresses
        ]
        response = requests.get(NABLA_PRICE_API_URL, params=params, timeout=10)
        if response.status_code != 200:
            msg = (
                f"Failed to fetch price data: {response.status_code} - {response.text}"
            )
            raise ValueError(msg)

        response_json = response.json()

        # Parse prices
        prices = {}
        for entry in response_json.get("parsed", []):
            feed_id = entry.get("id")
            asset_address = self.get_asset_address_by_price_feed_id(feed_id)
            price = entry.get("price", {}).get("price")
            if feed_id and price is not None:
                prices[asset_address] = price

        # Parse price update data
        binary_chunks = response_json.get("binary", {}).get("data", [])
        price_update_data = "0x" + "".join(binary_chunks)

        return {"prices": prices, "priceUpdateData": price_update_data}

    def get_asset_address_by_price_feed_id(self, price_feed_id: str) -> str:
        """Get the asset address from the price feed id."""
        if price_feed_id not in PRICE_FEED_ID_TO_ASSET_ADDRESS[self.supported_ledger]:
            msg = f"Price feed ID {price_feed_id} not found."
            raise ValueError(msg)

        return PRICE_FEED_ID_TO_ASSET_ADDRESS[self.supported_ledger][price_feed_id]
