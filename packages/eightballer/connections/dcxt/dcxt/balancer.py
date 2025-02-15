"""Balancer exchange."""

import json
import time
import traceback
from enum import Enum
from glob import glob
from typing import cast
from decimal import Decimal
from pathlib import Path

# pylint: disable=R0914,R0902,R0912
# ruff: noqa: PLR0914,PLR0915
from datetime import datetime
from functools import cache
from collections import defaultdict

import web3
from balpy import balpy
from aea.contracts.base import Contract
from aea_ledger_ethereum import Account
from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration

from packages.eightballer.protocols.orders.custom_types import Order, Orders, OrderSide, OrderType, OrderStatus
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.connections.dcxt.dcxt.exceptions import (
    ApprovalError,
    ExchangeError,
    ConfigurationError,
    SorRetrievalException,
)
from packages.eightballer.connections.dcxt.erc_20.contract import Erc20, Erc20Token


GAS_PRICE_PREMIUM = 20
GAS_SPEED = "fastest"
GAS_PRICE = 888

TZ = datetime.now().astimezone().tzinfo

DEFAULT_ENCODING = "utf-8"


PACKAGE_DIR = Path(__file__).parent
ABI_DIR = PACKAGE_DIR / "abis"

ABI_MAPPING = {
    Path(path).stem.upper(): open(path, encoding=DEFAULT_ENCODING).read()  # noqa
    for path in glob(str(ABI_DIR / "*.json"))
}

ETH_KEYPATH = "ethereum_private_key.txt"
DEFAULT_AMOUNT_USD = 1

GAS_PRICE_PREMIUM = 20
GAS_SPEED = "fast"
GAS_PRICE = 888


class SupportedLedgers(Enum):
    """Supported ledgers."""

    ETHEREUM = "ethereum"
    GNOSIS = "gnosis"
    POLYGON_POS = "polygon_pos"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"
    MODE = "mode"


class SupportedBalancerDeployments(Enum):
    """Supported balancer deployments."""

    MAINNET = "mainnet"
    OPTIMISM = "optimism"
    BASE = "base"
    MODE = "mode"
    GNOSIS = "gnosis"
    ARBITRUM = "arbitrum"
    POLYGON = "polygon"


LEDGER_IDS_CHAIN_NAMES = {
    SupportedLedgers.OPTIMISM: SupportedBalancerDeployments.OPTIMISM,
    SupportedLedgers.ETHEREUM: SupportedBalancerDeployments.MAINNET,
    SupportedLedgers.BASE: SupportedBalancerDeployments.BASE,
    SupportedLedgers.MODE: SupportedBalancerDeployments.MODE,
    SupportedLedgers.GNOSIS: SupportedBalancerDeployments.GNOSIS,
    SupportedLedgers.ARBITRUM: SupportedBalancerDeployments.ARBITRUM,
    SupportedLedgers.POLYGON_POS: SupportedBalancerDeployments.POLYGON,
}

WHITELISTED_POOLS = {
    SupportedLedgers.ETHEREUM: [
        "0xebdd200fe52997142215f7603bc28a80becdadeb000200000000000000000694",
        "0x96646936b91d6b9d7d0c47c496afbf3d6ec7b6f8000200000000000000000019",
        "0x4e1325ff075a387e3d337f5f12638d6d72b127800001000000000000000006d7",
        "0x06df3b2bbb68adc0000000000000000000000000000000000000000000000000",
    ],
    SupportedLedgers.OPTIMISM: [
        "0x5bb3e58887264b667f915130fd04bbb56116c27800020000000000000000012a",
        "0x9da11ff60bfc5af527f58fd61679c3ac98d040d9000000000000000000000100",
    ],
    SupportedLedgers.BASE: [
        "0x5332584890d6e415a6dc910254d6430b8aab7e69000200000000000000000103",
        "0xaac1a23e7910efa801c6f1ff94648480ab0325b90002000000000000000000fc",
        "0x0c659734f1eef9c63b7ebdf78a164cdd745586db000000000000000000000046",
        "0xc771c1a5905420daec317b154eb13e4198ba97d0000000000000000000000023",
    ],
    SupportedLedgers.MODE: [
        "0xd1dbea51c7f23f61d020e2602d0d157d132faafc00020000000000000000000e",
        "0xbdee91916b38bca811f2c4c261daf1a8953262ca00000000000000000000000b",
        "0x7c86a44778c52a0aad17860924b53bf3f35dc932000200000000000000000007",
    ],
    SupportedLedgers.POLYGON_POS: [],
}


LEDGER_TO_STABLECOINS = {
    SupportedLedgers.ETHEREUM: [
        "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI,
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
    ],
    SupportedLedgers.OPTIMISM: [
        "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",  # USDT
    ],
    SupportedLedgers.BASE: [
        "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",  # USDC
        "0x50c5725949a6f0c72e6c4a641f24049a917db0cb",  # DAI
        "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca",  # usdcb
    ],
    SupportedLedgers.GNOSIS: [
        "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",  # wxdai
        "0x2a22f9c3b484c3629090feed35f17ff8f88f76f0",  # USDC.e
        "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83",  # USDC
    ],
    SupportedLedgers.POLYGON_POS: [
        "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063",
        "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",  # USDC
    ],
    SupportedLedgers.ARBITRUM: [
        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
        "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
    ],
    SupportedLedgers.MODE: [
        "0xd988097fb8612cc24eec14542bc03424c656005f",  # USDC on Mode
        "0x3f51c6c5927b88cdec4b61e2787f9bd0f5249138",
    ],
}

LEDGER_TO_NATIVE_SYMBOL = {
    SupportedLedgers.ETHEREUM: "ETH",
    SupportedLedgers.OPTIMISM: "ETH",
    SupportedLedgers.BASE: "ETH",
    SupportedLedgers.GNOSIS: "xDAI",
    SupportedLedgers.POLYGON_POS: "POL",
    SupportedLedgers.ARBITRUM: "ETH",
    SupportedLedgers.MODE: "ETH",
}

LEDGER_TO_WRAPPER = {
    SupportedLedgers.ETHEREUM: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    SupportedLedgers.OPTIMISM: "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
    SupportedLedgers.BASE: "0x4200000000000000000000000000000000000006",
    SupportedLedgers.GNOSIS: "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",
    SupportedLedgers.POLYGON_POS: "0x0000000000000000000000000000000000001010",
    SupportedLedgers.ARBITRUM: "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    SupportedLedgers.MODE: "0x4200000000000000000000000000000000000006",
}
LEDGER_TO_OLAS = {
    SupportedLedgers.ETHEREUM: "0x0001a500a6b18995b03f44bb040a5ffc28e45cb0",
    SupportedLedgers.OPTIMISM: "0xfc2e6e6bcbd49ccf3a5f029c79984372dcbfe527",
    SupportedLedgers.BASE: "0x54330d28ca3357f294334bdc454a032e7f353416",
    SupportedLedgers.GNOSIS: "0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f",
    SupportedLedgers.POLYGON_POS: "0xFEF5d947472e72Efbb2E388c730B7428406F2F95",
    SupportedLedgers.ARBITRUM: "0x064f8b858c2a603e1b106a2039f5446d32dc81c1",
    SupportedLedgers.MODE: "0xcfD1D50ce23C46D3Cf6407487B2F8934e96DC8f9",
}

LEDGER_TO_WETH = {
    SupportedLedgers.MODE: "0x4200000000000000000000000000000000000006",
    SupportedLedgers.BASE: "0x4200000000000000000000000000000000000006",
    SupportedLedgers.GNOSIS: "0x6a023ccd1ff6f2045c3309768ead9e68f978f6e1",
}


LEDGER_TO_TOKEN_LIST = {
    SupportedLedgers.ETHEREUM: set(
        [
            "0x0001a500a6b18995b03f44bb040a5ffc28e45cb0",  # olas
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.ETHEREUM]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.ETHEREUM]]
    ),
    SupportedLedgers.OPTIMISM: set(
        [
            "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
            "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.OPTIMISM]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.OPTIMISM]]
    ),
    SupportedLedgers.BASE: set(
        [
            "0x54330d28ca3357f294334bdc454a032e7f353416",  # OLAS
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.BASE]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.BASE]]
    ),
    SupportedLedgers.GNOSIS: set(
        [
            "0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f",  # olas
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.GNOSIS]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.GNOSIS]]
        + [LEDGER_TO_WETH[SupportedLedgers.GNOSIS]]
    ),
    SupportedLedgers.POLYGON_POS: set(
        [
            "0xFEF5d947472e72Efbb2E388c730B7428406F2F95",  # olas
            "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",  # weth
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.POLYGON_POS]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.POLYGON_POS]]
    ),
    SupportedLedgers.ARBITRUM: set(
        [
            "0x064f8b858c2a603e1b106a2039f5446d32dc81c1",  # olas
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.ARBITRUM]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.ARBITRUM]]
    ),
    SupportedLedgers.MODE: set(
        [
            "0xcfd1d50ce23c46d3cf6407487b2f8934e96dc8f9",  # mode
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.MODE]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.MODE]]
    ),
}


TOKEN_LIST_PATH = Path(__file__).parent / "data" / "token_list.json"


def read_token_list(chain_id: int):
    """Read the token list."""
    with open(TOKEN_LIST_PATH, encoding=DEFAULT_ENCODING) as file:
        token_list = json.loads(file.read())["tokens"]

    tokens = filter(lambda t: t["chainId"] == chain_id, token_list)
    return {t["address"]: t for t in tokens}


class BalancerClient:
    """Balancer exchange."""

    tokens: dict[str:Erc20Token] = {}

    def __init__(self, key_path: str, ledger_id: str, rpc_url: str, etherscan_api_key: str, **kwargs):  # pylint: disable=super-init-not-called
        if SupportedLedgers(ledger_id) not in LEDGER_IDS_CHAIN_NAMES:
            msg = f"Incorrect chain name `{ledger_id}` provided to BalancerClient"
            raise ConfigurationError(msg)

        self.ledger_id = SupportedLedgers(ledger_id)
        self.balancer_deployment = LEDGER_IDS_CHAIN_NAMES[self.ledger_id]

        self.rpc_url = rpc_url

        self.etherscan_api_key = etherscan_api_key

        with open(key_path, encoding=DEFAULT_ENCODING) as file:
            key = file.read().strip()
        self.account = Account.from_key(private_key=key)
        self.bal: balpy.balpy = balpy.balpy(
            LEDGER_IDS_CHAIN_NAMES[self.ledger_id].value,
            manualEnv={
                "privateKey": self.account._private_key,  # noqa
                "customRPC": self.rpc_url,
                "etherscanApiKey": self.etherscan_api_key,
            },
        )

        self.gas_price = kwargs.get("gas_price", None)
        self.gas_price_premium = kwargs.get("gas_price_premium", GAS_PRICE_PREMIUM)

        contract_dir = Path(__file__).parent.parent.parent.parent / "contracts" / "erc_20"
        configuration = cast(
            ContractConfig,
            load_component_configuration(
                ComponentType.CONTRACT, Path(__file__).parent.parent.parent.parent / "contracts" / "erc_20"
            ),
        )
        configuration.directory = contract_dir
        # Not a nice way to do this, but connections cannot have contracts as a dependency.
        self.erc20_contract: Erc20 = Contract.from_config(configuration)
        self.logger = kwargs.get("logger")
        self.tickers = {}
        self.raw_token_data = read_token_list(self.bal.web3.eth.chain_id)
        self.tokens = {}

    async def fetch_markets(
        self,
        params: dict,
    ) -> Markets:
        """Fetches the markets.

        Args:
        ----
            params: The parameters.

        Returns:
        -------
            The markets.

        """

        del params
        try:
            markets = [
                {
                    "id": pool_id,
                    "symbol": "OLAS/USDC",
                    "base": "OLAS",
                    "quote": "USDC",
                    "spot": True,
                }
                for pool_id in self.pool_ids
            ]
            return Markets(
                markets=[Market(**market) for market in markets],
            )
        except SorRetrievalException as exc:
            msg = f"Error fetching markets from chainId {self.chain_name} Balancer: {exc}"
            raise SorRetrievalException(msg) from exc

    @property
    def pool_ids(self) -> dict:
        """Get the pool IDs.

        :return(dict): The pool IDs.
        """
        # We read in the pool IDs from a file for now. we get this file from https://github.com/balancer/frontend-v2/blob/8563b8d33b6bff266148bd48d7ebc89f921374f4/src/lib/config/mainnet/pools.ts#L296
        with open(
            Path(__file__).parent / "data" / "balancer" / f"{self.balancer_deployment.value}.json",
            encoding=DEFAULT_ENCODING,
        ) as file:
            json_data = json.loads(file.read())["pools"]
        if "Element" in json_data:
            del json_data["Element"]
        return json_data

    async def build_tokens(self):
        """Build the token data."""
        params = (
            self.pool_ids
        )  # however as we are not able to collect for *all* ppols, we just select a few to get the data for.

        # We use olas USDC as the base pair for now.

        pools_of_interest = {}
        for pool_type in params:
            for pool_id in params[pool_type]:
                if pool_id.lower() in WHITELISTED_POOLS[self.ledger_id]:
                    if pool_type not in pools_of_interest:
                        pools_of_interest[pool_type] = [pool_id]
                    else:
                        pools_of_interest[pool_type].append(pool_id)

        if not pools_of_interest:
            msg = "No pools of interest found!"
            raise SorRetrievalException(msg)
        self.bal.getOnchainData(pools_of_interest)

        self.bal.mc.reset()

        for token_address in self.bal.decimals:
            contract = self.bal.erc20GetContract(token_address)
            self.bal.mc.addCall(
                token_address,
                contract.abi,
                "name",
                args=[],
            )
        name_data = self.bal.mc.execute()
        # We now get the symbols
        self.bal.mc.reset()
        for token_address in self.bal.decimals:
            contract = self.bal.erc20GetContract(token_address)
            self.bal.mc.addCall(
                token_address,
                contract.abi,
                "symbol",
                args=[],
            )
        symbol_data = self.bal.mc.execute()

        # We create an array of ticker data.
        for address, name, symbol in zip(self.bal.decimals, name_data[0], symbol_data[0], strict=False):
            if not name or not symbol:
                continue
            if address not in self.tokens:
                self.tokens[address] = Erc20Token(
                    address=address,
                    symbol=symbol[0],
                    name=name[0],
                    decimals=self.bal.decimals[address],
                )
            # We now get get the price for the swap
            # We now make an erc20 representation of the token.

    async def fetch_tickers(self, *args, **kwargs) -> Tickers:
        """Fetches the tickers.

        Args:
        ----
            args: The arguments.
            kwargs: The keyword arguments.

        :return(Tickers): The tickers.

        """
        del args, kwargs

        # We temporarily assume that the tickers are the same as the markets, and use the pool IDs to get the tickers.
        prices = self.bal.graph.getCurrentPrices(
            chain=self.balancer_deployment.value,
        )
        prices = {price["address"]: price["price"] for price in prices}
        for token_address in LEDGER_TO_TOKEN_LIST[self.ledger_id]:
            token = self.get_token(token_address)
            symbol = f"{token.symbol}/USD"
            usd_price = prices[token.address.lower()]
            timestamp = datetime.now(tz=datetime.now().astimezone().tzinfo)
            ticker = Ticker(
                symbol=symbol,
                asset_a=token.symbol,
                asset_b="USD",
                high=usd_price,
                low=usd_price,
                ask=usd_price,
                bid=usd_price,
                timestamp=int(timestamp.timestamp()),
                datetime=timestamp.isoformat(),
            )
            self.tickers[symbol] = ticker
        return Tickers(tickers=list(self.tickers.values()))

    def get_params_for_swap(self, input_token_address, output_token_address, input_amount, is_buy=False):
        """Given the data, we get the params for the swap from the balancer exchange."""
        gas_price = self.bal.web3.eth.gas_price * GAS_PRICE_PREMIUM
        return {
            "network": self.balancer_deployment.value,
            "slippageTolerancePercent": "0.1",  # 1%
            "sor": {
                "sellToken": input_token_address,
                "buyToken": output_token_address,  # // token out
                "orderKind": "buy" if is_buy else "sell",
                "amount": input_amount,
                "gasPrice": gas_price,
            },
            "batchSwap": {
                "funds": {
                    "sender": self.account.address,  # // your address
                    "recipient": self.account.address,  # // your address
                    "fromInternalBalance": False,  # // to/from internal balance
                    "toInternalBalance": False,  # // set to "false" unless you know what you're doing
                },
                # // unix timestamp after which the trade will revert if it hasn't executed yet
                "deadline": datetime.now(tz=TZ).timestamp() + 600,
            },
        }

    def get_price(
        self, input_token_address: str, output_token_address: str, amount: float, is_sell: bool = False
    ) -> float:
        """Get the price of the token."""

        self.logger.debug(
            f"Getting price for {input_token_address} -> {output_token_address} for {amount} is_sell: {is_sell}"
        )
        params = self.get_params_for_swap(
            input_token_address=input_token_address,
            output_token_address=output_token_address,
            input_amount=amount,
            is_buy=not is_sell,
        )
        # we query the smart router
        try:
            sor_result = self.bal.balSorQuery(params)
        except Exception as exc:  # pylint: disable=W0718
            self.logger.exception(exc)
            self.logger.exception(f"Error querying SOR: {traceback.format_exc()}")

        if not sor_result.get("returnAmount", None):
            msg = f"No limits found for swap. Implies incorrect configuration of swap params: {params}"
            raise SorRetrievalException(msg)
        amount_out = float(sor_result["returnAmount"])
        return Decimal(amount_out) / Decimal(amount)

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
            asset_a, asset_b = symbol.split("/")
        if not asset_a or not asset_b:
            msg = "Asset A and Asset B must be provided"
            raise ValueError(msg)

        input_token = self.get_token(asset_a)
        output_token = self.get_token(asset_b)
        symbol = f"{input_token.symbol}/{output_token.symbol}"

        # We now calculate the price of the token.
        params["is_sell"] = True
        bid_price = self.get_price(input_token.address, output_token.address, **params)
        params["amount"] = bid_price * Decimal(params["amount"])
        ask_price = 1 / self.get_price(output_token.address, input_token.address, **params)
        timestamp = datetime.now(tz=datetime.now().astimezone().tzinfo)
        self.logger.debug(f"Got ticker for {symbol} with ask: {ask_price} and bid: {bid_price}")
        return Ticker(
            symbol=symbol,
            asset_a=asset_a,
            asset_b=asset_b,
            high=ask_price,
            low=bid_price,
            ask=ask_price,
            bid=bid_price,
            timestamp=int(timestamp.timestamp()),
            datetime=timestamp.isoformat(),
        )

    async def fetch_positions(self, **kwargs) -> list:
        """Fetches the positions, notice as this is a balancer exchange, we do not have positions.
        We therefore return an empty list.

        Args:
        ----
            kwargs: The keyword arguments.

        :return(List): The

        """
        del kwargs
        return []

    async def create_order(
        self,
        *args,
        retries=1,
        **kwargs,
    ) -> Order:
        """Create an order.

        Args:
        ----
            args: The arguments.
            retries: The number of retries.
            kwargs: The keyword arguments.

        :return(Order): The order.

        """

        symbol = kwargs.get("symbol", None)
        if not symbol:
            msg = "Symbol not provided to create order"
            raise ValueError(msg)

        asset_a, asset_b = kwargs.get("asset_a"), kwargs.get("asset_b")
        human_amount = kwargs.get("amount", None)
        if not human_amount:
            msg = "Size not provided to create order"
            raise ValueError(msg)
        asset_a_token = self.get_token(asset_a)

        is_buy = kwargs.get("side") == "buy"
        if is_buy:
            input_token_address = asset_b
            output_token_address = asset_a
            amount = human_amount * kwargs.get("price") if kwargs.get("price") else human_amount
            machine_amount = asset_a_token.to_machine(amount)
            self.logger.debug(f"Creating buy order for {human_amount} {asset_a} -> {asset_b}")
        else:
            input_token_address = asset_a
            output_token_address = asset_b
            machine_amount = asset_a_token.to_machine(human_amount)
            amount = human_amount

        params = self.get_params_for_swap(
            input_token_address=input_token_address,
            output_token_address=output_token_address,
            input_amount=amount,
            is_buy=False,
        )
        try:
            sor_result = self.bal.balSorQuery(params)
        except Exception as exc:  # pylint: disable=W0703
            self.logger.exception(exc)
            self.logger.exception(f"Error querying SOR: {traceback.format_exc()}")
            msg = f"Error querying SOR: {exc}"
            raise SorRetrievalException(msg) from exc

        # We now parse the result;

        if not sor_result["swaps"]:
            self.logger("Problem with SOR retrieval!!")
            if retries > 0:
                self.logger(f"Retrying transaction. {retries} retries left")
                return self.create_order(*args, **kwargs, retries=retries - 1)
            msg = f"Error querying SOR: {sor_result}"
            raise SorRetrievalException(msg)

        msg = (
            f"Recommended swap: for {human_amount} {asset_a} -> {asset_b} is: " + f"{json.dumps(sor_result, indent=4)}"
        )
        self.logger.debug(msg)
        batch_swap = self.bal.balSorResponseToBatchSwapFormat(params, sor_result).get("batchSwap", None)

        if not batch_swap:
            msg = f"Error parsing SOR response: {sor_result}"
            raise SorRetrievalException(msg)

        # we now do the txn if its not a multi sig.
        extra_data = kwargs.get("data", None)
        safe_contract_address = None
        if extra_data:
            safe_contract_address = extra_data.get("safe_contract_address", None)
        if not safe_contract_address:
            self.logger.info("Handling EOA txn")
            fnc = self._handle_eoa_txn
        else:
            self.logger.info(f"Handling safe txn request in dcxt for {safe_contract_address!r}")
            fnc = self._handle_safe_txn
        return fnc(
            batch_swap,
            symbol,
            input_token_address,
            machine_amount=machine_amount,
            safe_address=safe_contract_address,
            price=kwargs.get("price"),
            amount=kwargs.get("amount"),
            side=kwargs.get("side"),
        )

    def _handle_safe_txn(
        self, swap, symbol, input_token_address, machine_amount, safe_address, side=None, **kwargs
    ) -> Order:
        """Handle the EOA transaction."""
        del kwargs

        vault = self.bal.balLoadContract("Vault")

        swap["funds"]["sender"] = safe_address
        swap["funds"]["recipient"] = safe_address

        erc_contract = self.bal.erc20GetContract(input_token_address)
        approved = erc_contract.functions.allowance(owner=safe_address, spender=vault.address).call()

        # We approve the token if we have not already done so.

        if approved < machine_amount * 1e17:
            self.logger.info(f"Approving {machine_amount} {input_token_address} for {vault.address}")
            data = erc_contract.encodeABI("approve", [vault.address, int(machine_amount * 1e18)])
            vault_address = erc_contract.address

        else:
            try:
                mc_args = self.bal.balFormatBatchSwapData(swap)
                vault = self.bal.balLoadContract("Vault")
                function_name = "batchSwap"
                data = vault.encodeABI(function_name, mc_args)
                vault_address = vault.address
            except web3.exceptions.ContractLogicError as exc:
                self.logger.exception(exc)
                self.logger.exception(f"Error calling batchSwapFn: {traceback.format_exc()}")
                if "BAL#508" in str(exc):
                    msg = "SWAP_DEADLINE: Swap transaction not mined within the specified deadline"
                    raise ExchangeError(msg) from exc
                if "execution reverted: ERC20: transfer amount exceeds allowance" in str(exc):
                    msg = "ERC20: transfer amount exceeds allowance"
                    raise ApprovalError(msg) from exc
                msg = f"Error calling batchSwapFn: {exc}"
                raise SorRetrievalException(msg) from exc

        self.logger.info(f"Creating order for {symbol} with data: {data} to {vault_address}")
        return Order(
            exchange_id="balancer",
            symbol=symbol,
            status=OrderStatus.NEW,
            side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
            type=OrderType.MARKET,
            ledger_id=self.ledger_id.value,
            info=json.dumps(
                {
                    "data": data,
                    "vault_address": vault_address,
                    "chain_id": self.bal.web3.eth.chain_id,
                }
            ),
        )

    def _do_eoa_approval(self, input_token_address, machine_amount, vault, contract) -> None:
        """Do the EOA approval."""
        del input_token_address
        func = contract.functions.approve(vault.address, int(machine_amount * 1e240))
        return self._do_txn(func)

    def _do_txn(self, func):
        base_fee = self.bal.web3.eth.fee_history(1, "latest")["baseFeePerGas"][-1]  # Get the current base fee
        priority_fee = self.bal.web3.to_wei(
            GAS_PRICE_PREMIUM, "gwei"
        )  # Set a reasonable priority fee (at least 1 gwei)

        kwargs = {
            "from": self.account.address,
            "nonce": self.bal.web3.eth.get_transaction_count(self.account.address),
            "gas": func.estimate_gas(),  # Estimated gas limit
        }
        if self.ledger_id == SupportedLedgers.GNOSIS:
            kwargs["maxFeePerGas"] = base_fee + priority_fee
            kwargs["maxPriorityFeePerGas"] = priority_fee
        tx_1 = func.build_transaction(kwargs)
        signed_tx = self.account.sign_transaction(tx_1)
        tx_hash_1 = self.bal.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # we wait for the transaction to be mined
        self.logger.info("Waiting for transaction to be mined")
        # we wait for the next block to be sure that the transaction nonce is correct
        current_block = self.bal.web3.eth.block_number
        while current_block == self.bal.web3.eth.block_number:
            time.sleep(0.1)
        self.logger.info("Waiting for transaction to be mined")
        receipt = self.bal.web3.eth.wait_for_transaction_receipt(tx_hash_1)
        self.logger.info("Transaction mined")
        self.logger.debug(f"Receipt: {receipt}")
        was_successful = receipt["status"]
        if not was_successful:
            msg = f"Transaction failed: {receipt}"
            raise ValueError(msg)
        return tx_hash_1.hex()

    def _handle_eoa_txn(  # pylint: disable=unused-argument
        self, swap, symbol, input_token_address, machine_amount, execute=True, **kwargs
    ) -> Order:  # pylint: disable=unused-argument
        """Handle the EOA transaction."""

        vault = self.bal.balLoadContract("Vault")

        # We do a call on the erc_20 not on the balancer contract as the balancer contract checks the spenders account.

        approved = self.bal.erc20GetAllowanceStandard(
            tokenAddress=input_token_address,
            allowedAddress=vault.address,
        )

        # We approve the token if we have not already done so.

        tx_hash = None
        if approved < machine_amount:
            self.logger.info(f"Approving {machine_amount} {input_token_address} for {vault.address}")
            contract = self.bal.erc20GetContract(input_token_address)
            data = contract.encodeABI("approve", [vault.address, machine_amount * 3])
            vault_address = contract.address

            if execute:
                # We recall the function to get the updated allowance.
                self._do_eoa_approval(input_token_address, machine_amount, vault, contract)
                return self._handle_eoa_txn(
                    swap, symbol, input_token_address, machine_amount, execute=execute, **kwargs
                )
        else:
            try:
                mc_args = self.bal.balFormatBatchSwapData(swap)
                vault = self.bal.balLoadContract("Vault")
                function_name = "batchSwap"
                data = vault.encodeABI(function_name, mc_args)
                fn = vault.get_function_by_name(fn_name=function_name)
                # Assuming this does not revert, we have our call data for the order.
                fn(*mc_args).call()
                vault_address = vault.address
                if execute:
                    self.logger.info(f"Creating order for {symbol} with data: {data} to {vault_address}")

                    tx_hash = self._do_txn(fn(*mc_args))
                    self.logger.info(f"Transaction hash: {tx_hash!r} to {self.rpc_url}")
            except ValueError as exc:
                if "EffectivePriorityFeePerGas" in str(exc):
                    self.logger.info("Transaction reverted due to insufficient gas price")
                    self.logger.exception(exc)
                if kwargs.get("attempts", 0) < 3:
                    kwargs["attempts"] = 1 + kwargs.get("attempts", 0)
                    self.logger.info(f"Retrying transaction. {kwargs['attempts']} retries left")
                    return self._handle_eoa_txn(
                        swap, symbol, input_token_address, machine_amount, execute=execute, **kwargs
                    )
                raise

            except web3.exceptions.ContractLogicError as exc:
                self.logger.exception(exc)
                self.logger.exception(f"Error calling batchSwapFn: {traceback.format_exc()}")
                if "BAL#508" in str(exc):
                    msg = "SWAP_DEADLINE: Swap transaction not mined within the specified deadline"
                    raise ExchangeError(msg) from exc
                if "execution reverted: ERC20: transfer amount exceeds allowance" in str(exc):
                    msg = f"ERC20: transfer amount exceeds allowance: {exc}"
                    raise ApprovalError(msg) from exc
                msg = f"Error calling batchSwapFn: {exc}"
                raise SorRetrievalException(msg) from exc

        return Order(
            id=tx_hash,
            exchange_id="balancer",
            ledger_id=self.ledger_id.value,
            symbol=symbol,
            price=kwargs.get("price"),
            amount=kwargs.get("amount"),
            status=OrderStatus.NEW if not execute else OrderStatus.FILLED,
            type=OrderType.LIMIT,
            side=OrderSide.BUY if kwargs.get("side") == "buy" else OrderSide.SELL,
            info=json.dumps(
                {
                    "data": data,
                    "vault_address": vault_address,
                    "chain_id": self.bal.web3.eth.chain_id,
                }
            ),
        )

    def parse_order(self, order, *args, **kwargs) -> Order:
        """Parse the order.

        :return(Order): The order.
        """
        del args, kwargs
        return order

    async def cancel_order(self, *args, **kwargs):
        """Cancel an order.

        NOTE: This method is not implemented as we dont have orders in balancer.

        in the future, we would look to get pending orders in
        the mempool and replace with a 0 transfer of the same hash

        Args:
        ----
            args: The arguments.
            kwargs: The keyword arguments.

        """
        del args, kwargs
        raise NotImplementedError

    async def get_order(self, *args, **kwargs):
        """Get an order."""
        del args, kwargs
        raise NotImplementedError

    async def fetch_open_orders(self, **kwargs):
        """Get an order."""
        vault = self.bal.balLoadContract("Vault")
        params = kwargs.get("params", {})

        def parse_transaction(events, _):
            def net_out_swaps(swap_events):
                # This dictionary will hold net amounts for each token address
                token_balances = defaultdict(lambda: {"spent": 0, "received": 0})

                # Loop over each swap event and net out the amounts
                for event in swap_events:
                    # Extract the details from each swap event
                    token_in = event["args"]["tokenIn"]
                    token_out = event["args"]["tokenOut"]
                    amount_in = event["args"]["amountIn"]
                    amount_out = event["args"]["amountOut"]

                    # Update the 'spent' (tokenIn) and 'received' (tokenOut) amounts
                    token_balances[token_in]["spent"] += amount_in
                    token_balances[token_out]["received"] += amount_out

                # Calculate the net balances for each token
                net_balances = {}
                for token, balances in token_balances.items():
                    net_bal = balances["received"] - balances["spent"]
                    if net_bal != 0:
                        net_balances[token] = net_bal

                return net_balances

            net_balances = net_out_swaps(events)
            for address, raw_balance in net_balances.items():
                token = self.get_token(address)
                balance = token.to_human(raw_balance)
                net_balances[address] = balance
            return net_balances

        all_events = []
        # We have to batch up the events as the filter can only return 10k events at a time
        start = 21076969
        interval = 2000
        end = self.bal.web3.eth.block_number
        account = params.get("account")
        for i in range(0, end - start, interval):
            start += i
            to = start + interval
            if to > end:
                to = end - 1
            if start >= end:
                break
            events = vault.events.Swap.create_filter(fromBlock=start, toBlock=to, address=account).get_all_entries()
            all_events.extend(events)

        # We create a bundle of events for each transaction
        event_bundles = defaultdict(list)
        for event in events:
            tx_hash = event["transactionHash"].hex()
            event_bundles[tx_hash].append(event)

        # We now parse all the individual transactions
        trades = {}

        transaction_data = {}
        for tx_hash, events in event_bundles.items():
            trades[tx_hash] = parse_transaction(events, tx_hash)
            transaction_data[tx_hash] = self.bal.web3.eth.get_transaction(tx_hash)

        {k: v for k, v in transaction_data.items() if v["from"] == account}

        return Orders(orders=[])

    async def get_all_markets(self, *args, **kwargs):
        """Get all markets."""
        del args, kwargs
        raise NotImplementedError

    async def subscribe(self, *args, **kwargs):
        """Subscribe to the order book."""
        del args, kwargs
        raise NotImplementedError

    async def close(self):
        """Close the connection."""

    async def fetch_balance(self, *args, **kwargs) -> Balances:
        """Fetch the balance.

        :return(Balances): The balance.
        """
        del args

        mc = self.bal.mc
        mc.reset()
        use_external_address = kwargs.get("address", None)
        address_to_check = use_external_address or self.account.address
        self.logger.debug(
            f"Checking balance for {address_to_check} with for tokens {LEDGER_TO_TOKEN_LIST[self.ledger_id]}"
        )
        for token_address in LEDGER_TO_TOKEN_LIST[self.ledger_id]:
            contract = self.bal.erc20GetContract(token_address)
            mc.addCall(
                token_address,
                contract.abi,
                "balanceOf",
                args=[address_to_check],
            )
        balance_data = mc.execute()
        native = self.bal.web3.eth.get_balance(address_to_check)

        return Balances(
            balances=[
                self._from_decimals_amt_to_token(token_address, balance[0])
                for token_address, balance in zip(LEDGER_TO_TOKEN_LIST[self.ledger_id], balance_data[0], strict=False)
            ]
            + [
                Balance(
                    asset_id=LEDGER_TO_NATIVE_SYMBOL[self.ledger_id],
                    free=self.bal.web3.from_wei(native, "ether"),
                    total=self.bal.web3.from_wei(native, "ether"),
                    is_native=True,
                    used=0,
                )
            ]
        )

    @cache  # noqa
    def get_token(self, address):
        """Get the token from the address."""
        # We check if the token is already in the raw token data.
        if address in self.tokens:
            return self.tokens[address]
        if address in self.raw_token_data:
            token_data = self.raw_token_data[address]
            token = Erc20Token(
                address=address,
                symbol=token_data["symbol"],
                name=token_data["name"],
                decimals=token_data["decimals"],
            )
            self.tokens[address] = token
            return self.get_token(address)
        # We retrieve the token from the balancer contract.
        contract = self.bal.erc20GetContract(address)
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        self.tokens[address] = Erc20Token(
            address=address,
            name=name,
            symbol=symbol,
            decimals=decimals,
        )
        return self.get_token(address)

    def _from_decimals_amt_to_token(self, address, balance):
        """Convert the balance to a token balance."""
        token = self.get_token(address)
        return Balance(
            asset_id=token.symbol,
            contract_address=token.address,
            free=token.to_human(balance),
            used=0,
            total=token.to_human(balance),
            is_native=False,
        )
