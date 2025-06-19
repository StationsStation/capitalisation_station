"""Nabla Finance client for swapping tokens on the Nabla Finance DEX."""

from dataclasses import field

import click
import requests
from aea_ledger_ethereum import EthereumApi
from pydantic.dataclasses import dataclass

# from packages.dakavon.contracts.nabla_portal import PUBLIC_ID as NABLA_PORTAL_PUBLIC_ID
from packages.eightballer.connections.dcxt.utils import load_contract
from aea.configurations.base import PublicId

# Add the base directory to the Python path (if needed)
# root_dir = Path(__file__) resolve() parents[5]
# sys path append(base_dir)
from packages.eightballer.protocols.orders.custom_types import (
    Order,
)
from packages.eightballer.connections.dcxt.dcxt.data.tokens import SupportedLedgers
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import (
    BaseErc20Exchange,
)

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


ASSET_REGISTRY = {
    SupportedLedgers.BASE: {
        "WETH": "0x4200000000000000000000000000000000000006",
        "CBBTC": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
    },
    # SupportedLedgers.ARBITRUM
}

ASSET_ADDRESS_TO_PRICE_FEED_ID = {
    "0x4200000000000000000000000000000000000006": "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",
    "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf": "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
}
PRICE_FEED_ID_TO_ASSET_ADDRESS = {
    "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace": "0x4200000000000000000000000000000000000006",  # WETH
    "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
    # "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a": "",
    # "3fa4252848f9f0a1480be62745a4629d9eb1322aebab8a791e344b3b9c1adcf5": "",  # ARB token
}
NABLA_PRICE_API_URL = "https://antenna.nabla.fi/v1/updates/price/latest"

PORTAL_ADDRESSES = {
    SupportedLedgers.BASE: "0xd24d145f5E351de52934A7E1f8cF55b907E67fFF",
    SupportedLedgers.ARBITRUM: "0xcB94Eee869a2041F3B44da423F78134aFb6b676B",
}

BASE_ROUTER_ADDRESS = "0x791Fee7b66ABeF59630943194aF17B029c6F487B"
ROUTER_ADDRESSES = {
    SupportedLedgers.BASE: "0x791Fee7b66ABeF59630943194aF17B029c6F487B",
}


class NablaFinanceClient(BaseErc20Exchange):
    """Class for interacting with the Nabla Finance API."""

    exchange_id = "nabla"

    @property
    def spender_address(self):
        return PORTAL_ADDRESSES[self.supported_ledger]

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
        if symbol:
            asset_a_symbol, asset_b_symbol = symbol.split("/")
            # we need to look up the token addresses for the assets.
            asset_a = get_token_address(asset_a_symbol, SupportedLedgers.BASE)
            asset_b = get_token_address(asset_b_symbol, SupportedLedgers.BASE)
        if not asset_a or not asset_b:
            msg = f"Could not find token addresses for `{asset_a}` and `{asset_b}`"
            msg += f" with symbols {asset_a_symbol} and {asset_b_symbol}"
            raise ValueError(msg)

        params = params

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

    async def create_order(self, *args, retries=0, **kwargs):
        """Create an order."""

    async def fetch_open_orders(self, **kwargs):
        """Fetch open orders."""


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

    return ASSET_ADDRESS_TO_PRICE_FEED_ID[asset_address]


def get_asset_address_by_price_feed_id(price_feed_id: str) -> str:
    """Get the asset address from the price feed id."""
    if price_feed_id not in PRICE_FEED_ID_TO_ASSET_ADDRESS:
        msg = f"Price feed ID {price_feed_id} not found."
        raise ValueError(msg)

    return PRICE_FEED_ID_TO_ASSET_ADDRESS[price_feed_id]


def fetch_price_data(asset_addresses) -> dict:
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
        ("ids[]", get_price_feed_id_by_asset_address(asset_address))
        for asset_address in asset_addresses
    ]
    response = requests.get(NABLA_PRICE_API_URL, params=params, timeout=10)

    if response.status_code != 200:
        msg = f"Failed to fetch price data: {response.status_code} - {response.text}"
        raise ValueError(msg)

    response_json = response.json()
    # "print(f"Response JSON: {response_json}")"

    # Parse prices
    prices = {}
    for entry in response_json.get("parsed", []):
        feed_id = entry.get("id")
        asset_address = get_asset_address_by_price_feed_id(feed_id)
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


def get_swap_quote(
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

    api = EthereumApi(address="https://base.drpc.org", chain_id=str(8453))

    nabla_portal_contract = load_contract(PublicId.from_str(NABLA_PORTAL_PUBLIC_ID))

    swap_amount_out = nabla_portal_contract.quote_swap_exact_tokens_for_tokens(
        ledger_api=api,
        contract_address=self.spender_address,
        amount_in=amount,
        token_path=[from_token_address, to_token_address],
        router_path=[BASE_ROUTER_ADDRESS],
        token_prices=[
            token_prices.get(from_token_address),
            token_prices.get(to_token_address),
        ],
    )

    return swap_amount_out.get("amountOut_", 0)


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

    breakpoint()

    #########################################
    # Step 3: Execute the swap (not implemented yet)
    #########################################
    # contract

    #########################################
    # END
    #########################################


if __name__ == "__main__":
    main()
