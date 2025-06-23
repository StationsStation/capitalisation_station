"""Nabla Finance client for swapping tokens on the Nabla Finance DEX."""

import datetime
from dataclasses import field

import click
import requests
from web3.exceptions import TimeExhausted
from pydantic.dataclasses import dataclass
from aea.configurations.base import PublicId

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.orders.custom_types import (
    Order,
    Orders,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker
from packages.eightballer.connections.dcxt.dcxt.data.tokens import SupportedLedgers
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import (
    BaseErc20Exchange,
    signed_tx_to_dict,
    try_send_signed_transaction,
)
# from derive_client.utils.w3 import build_standard_transaction


NABLA_PORTAL_PUBLIC_ID = "dakavon/nabla_portal:0.1.0"


@dataclass
class Price:
    price: int
    publish_time: int


@dataclass
class ParsedPrice:
    id: str
    metadata: dict
    price: Price
    address: str = field(init=False)
    symbol: str = field(init=False)
    chain: SupportedLedgers = SupportedLedgers.BASE

    def __post_init__(self):
        self.address = PRICE_FEED_ID_TO_ASSET_ADDRESS[self.id]
        self.symbol = {
            k for k, v in ASSET_REGISTRY[self.chain].items() if v == self.address
        }.pop()


ASSET_REGISTRY: dict[str, dict[str, str]] = {
    SupportedLedgers.BASE: {
        "WETH": "0x4200000000000000000000000000000000000006",
        "CBBTC": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
    },
    SupportedLedgers: {
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    },
}

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
        # "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a": "",
        # "3fa4252848f9f0a1480be62745a4629d9eb1322aebab8a791e344b3b9c1adcf5": "",  # ARB token
    },
    SupportedLedgers.ARBITRUM: {
        "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",  # WETH
        "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43": "",  # cbBTC
        "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  # USDC
    },
}

NABLA_PRICE_API_URL: str = "https://antenna.nabla.fi/v1/updates/price/latest"

PORTAL_ADDRESSES: dict[str, str] = {
    SupportedLedgers.BASE: "0xd24d145f5E351de52934A7E1f8cF55b907E67fFF",
    SupportedLedgers.ARBITRUM: "0xcB94Eee869a2041F3B44da423F78134aFb6b676B",
}
ROUTER_ADDRESSES: dict[str, str] = {
    SupportedLedgers.BASE: "0x791Fee7b66ABeF59630943194aF17B029c6F487B",
    SupportedLedgers.ARBITRUM: "0x7bcFc8b8ff61456ad7C5E2be8517D01df006d18d",
}


class NablaFinanceClient(BaseErc20Exchange):
    """Class for interacting with the Nabla Finance API."""

    exchange_id = "nabla"

    @property
    def spender_address(self):
        return PORTAL_ADDRESSES[self.supported_ledger]

    @property
    def router_address(self):
        return ROUTER_ADDRESSES[self.supported_ledger]

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

    async def close(self):
        """Close the client."""

    async def fetch_ticker(
        self,
        symbol: str | None = None,
        asset_a: str | None = None,
        asset_b: str | None = None,
        params: dict | None = None,
    ):
        """Fetches a ticker."""

        if all([symbol is None, asset_a is None or asset_b is None]):
            msg = "Either symbol or asset_a and asset_b must be provided"
            raise ValueError(msg)
        if symbol is None:
            symbol = f"{asset_a}/{asset_b}"
        if symbol:
            asset_a_symbol, asset_b_symbol = symbol.split("/")
            # we need to look up the token addresses for the assets.
            asset_a = self.look_up_by_symbol(
                asset_a_symbol, ledger=self.supported_ledger
            )
            asset_b = self.look_up_by_symbol(
                asset_b_symbol, ledger=self.supported_ledger
            )
        if not asset_a or not asset_b:
            msg = f"Could not find token addresses for `{asset_a}` and `{asset_b}`"
            msg += f" with symbols {asset_a_symbol} and {asset_b_symbol}"
            raise ValueError(msg)

        params = params
        ask_price = 10.0
        bid_price = 10.0
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

    def parse_order(self, order, *args, **kwargs) -> Order:
        """Parse the order."""
        return order

    async def fetch_positions(self, **kwargs) -> list:
        """Fetch positions."""
        return []

    def fetch_tickers(self, *args, **kwargs):
        """Fetch all tickers."""
        # NOTE: these are just price feeds now, not tickers as per protocol definition

        response = requests.get(NABLA_PRICE_API_URL, timeout=10)
        parsed = response.json()["parsed"]

        return [
            ParsedPrice(**data)
            for data in parsed
            if data["id"] in PRICE_FEED_ID_TO_ASSET_ADDRESS
        ]

    async def create_order(
        self,
        *args,
        asset_a: str,
        asset_b: str,
        side: str,
        amount: float,
        retries: int = 0,
        **kwargs,
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
            deadline=int(datetime.datetime.now().timestamp() + 36_000),
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

        # account = kwargs.get("params", {}).get("account", self.account.entity.address)

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
        # "print(f"Response JSON: {response_json}")"

        # Parse prices
        prices = {}
        for entry in response_json.get("parsed", []):
            feed_id = entry.get("id")
            asset_address = self.get_asset_address_by_price_feed_id(feed_id)
            price = entry.get("price", {}).get("price")
            # "print(f"feed_id: {feed_id}")
            # "print(f"price: {price}")
            if feed_id and price is not None:
                prices[asset_address] = price

        # "print(f"Price data: {prices}")

        # Parse price update data
        binary_chunks = response_json.get("binary", {}).get("data", [])
        price_update_data = "0x" + "".join(binary_chunks)
        # "print(f"Price update data: {price_update_data}")

        return {"prices": prices, "priceUpdateData": price_update_data}

    def get_asset_address_by_price_feed_id(self, price_feed_id: str) -> str:
        """Get the asset address from the price feed id."""
        if price_feed_id not in PRICE_FEED_ID_TO_ASSET_ADDRESS[self.supported_ledger]:
            msg = f"Price feed ID {price_feed_id} not found."
            raise ValueError(msg)

        return PRICE_FEED_ID_TO_ASSET_ADDRESS[self.supported_ledger][price_feed_id]


##################################
# Helper functions
##################################
def get_token_address(symbol: str, chain: SupportedLedgers) -> str:
    """Get the token address for a given symbol on a specific chain."""

    if chain not in ASSET_REGISTRY:
        msg = f"Chain {chain} is not supported."
        raise ValueError(msg)

    tokens = ASSET_REGISTRY[chain]
    address = tokens.get(symbol.upper())

    if not address:
        msg = f"Token {symbol} not found on chain {chain}."
        raise ValueError(msg)

    return address


def get_price_feed_id_by_asset_address(asset_address: str) -> str:
    """Get the price feed id from the list."""

    """
    Spaceholder for
        mapping(asset => mapping(token => priceFeedId))
    """

    return


@click.command()
@click.option(
    "--from",
    "from_token",
    type=str,
    required=True,
    help="Token to swap from",
    default="WETH",
)
@click.option(
    "--to",
    "to_token",
    type=str,
    required=True,
    help="Token to swap to",
    default="CBBTC",
)
@click.option(
    "--chain",
    "chain",
    type=click.Choice([ledger.name for ledger in SupportedLedgers]),
    default="BASE",
    help="Chain to use for the swap",
)
def main(from_token, to_token, chain):
    """CLI for swapping tokens on the Nabla Finance DEX."""

    from_token_symbol = from_token.upper()
    to_token_symbol = to_token.upper()
    chain = SupportedLedgers.BASE

    from_token_address = get_token_address(from_token_symbol, chain)
    to_token_address = get_token_address(to_token_symbol, chain)
    asset_addresses = [from_token_address, to_token_address]

    #########################################
    # Step 1: Get price feed update data
    # ""  {
    # ""      "prices": {
    # ""         _ASSET_ADDRESS: PRICE
    # ""      },
    # ""       "priceUpdateData": "0x..."
    # ""  }
    #########################################
    price_data = fetch_price_data(asset_addresses)
    token_prices = price_data["prices"]

    #########################################
    # Step 2: Receive a swap quote
    #########################################
    get_swap_quote(
        from_token_address=from_token_address,
        to_token_address=to_token_address,
        amount=int(1e18),  # Example amount in smallest unit (e.g., 1 WETH = 1e18 wei)
        token_prices=token_prices,
    )

    # # Price data is USDC denominated (8 decimals precision)
    # chain_id = LEDGER_TO_CHAIN_ID[chain]
    # token_data = read_token_list(chain_id)
    # from_token_data = token_data[from_token_address]
    # to_token_data = token_data[to_token_address]
    # from_token_decimals = from_token_data["decimals"]
    # to_token_decimals = to_token_data["decimals"]

    # token_prices[from_token_address] * from_token_decimals
    # token_prices[to_token_address] * to_token_decimals

    #########################################
    # Step 3: Execute the swap (not implemented yet)
    #########################################
    # contract

    #########################################
    # END
    #########################################


if __name__ == "__main__":
    main()
