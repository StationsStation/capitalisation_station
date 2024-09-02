"""
Balancer exchange.
"""

import json
import traceback
from enum import Enum
from glob import glob
from typing import cast
from decimal import Decimal
from pathlib import Path

# pylint: disable=R0914,R0902,R0912
from datetime import datetime

import web3
from balpy import balpy
from aea.contracts.base import Contract
from aea_ledger_ethereum import Account
from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration

from packages.eightballer.protocols.orders.custom_types import Order, Orders
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.connections.dcxt.dcxt.exceptions import (
    ApprovalError,
    ExchangeError,
    ConfigurationError,
    SorRetrievalException,
)
from packages.eightballer.connections.dcxt.erc_20.contract import Erc20Token


GAS_PRICE_PREMIUM = 20
GAS_SPEED = "fast"
GAS_PRICE = 888


DEFAULT_ENCODING = "utf-8"


PACKAGE_DIR = Path(__file__).parent
ABI_DIR = PACKAGE_DIR / "abis"

ABI_MAPPING = {
    Path(path).stem.upper(): open(path, encoding=DEFAULT_ENCODING).read()  # pylint: disable=R1732  # pylint: disable=R1732
    for path in glob(str(ABI_DIR / "*.json"))
}

ETH_KEYPATH = "ethereum_private_key.txt"
DEFAULT_AMOUNT_USD = 1


class SupportedLedgers(Enum):
    """
    Supported ledgers.
    """

    ETHEREUM = "ethereum"
    OPTIMISM = "optimism"


class SupportedBalancerDeployments(Enum):
    """
    Supported balancer deployments.
    """

    MAINNET = "mainnet"
    OPTIMISM = "optimism"


LEDGER_IDS_CHAIN_NAMES = {
    SupportedLedgers.OPTIMISM: SupportedBalancerDeployments.OPTIMISM,
    SupportedLedgers.ETHEREUM: SupportedBalancerDeployments.MAINNET,
}

WHITELISTED_POOLS = {
    SupportedLedgers.ETHEREUM: [
        "0xebdd200fe52997142215f7603bc28a80becdadeb000200000000000000000694",
        "0x96646936b91d6b9d7d0c47c496afbf3d6ec7b6f8000200000000000000000019",
    ],
    SupportedLedgers.OPTIMISM: [
        "0x5bb3e58887264b667f915130fd04bbb56116c27800020000000000000000012a",
        "0x9da11ff60bfc5af527f58fd61679c3ac98d040d9000000000000000000000100",
    ],
}


LEDGER_TO_TOKEN_LIST = {
    SupportedLedgers.ETHEREUM: [
        "0x0001a500a6b18995b03f44bb040a5ffc28e45cb0",
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    ],
    SupportedLedgers.OPTIMISM: [
        "0x4200000000000000000000000000000000000006",
        "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
    ],
}

LEDGER_TO_STABLECOINS = {
    SupportedLedgers.ETHEREUM: ["0x6b175474e89094c44da98b954eedeac495271d0f"],
    SupportedLedgers.OPTIMISM: ["0xda10009cbd5d07dd0cecc66161fc93d7c9000da1"],
}


class BalancerClient:
    """
    Balancer exchange.
    """

    tokens: dict[str:Erc20Token] = {}

    def __init__(self, key_path: str, ledger_id: str, rpc_url: str, etherscan_api_key: str, **kwargs):  # pylint: disable=super-init-not-called
        if SupportedLedgers(ledger_id) not in LEDGER_IDS_CHAIN_NAMES:
            raise ConfigurationError("Chain name not provided to BalancerClient")

        self.ledger_id = SupportedLedgers(ledger_id)
        self.balancer_deployment = LEDGER_IDS_CHAIN_NAMES[self.ledger_id]

        self.rpc_url = rpc_url

        self.etherscan_api_key = etherscan_api_key

        with open(key_path, "r", encoding=DEFAULT_ENCODING) as file:
            key = file.read().strip()
        self.account = Account.from_key(private_key=key)
        self.bal: balpy.balpy = balpy.balpy(
            LEDGER_IDS_CHAIN_NAMES[self.ledger_id].value,
            manualEnv={
                "privateKey": self.account._private_key,
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
        self.erc20_contract = Contract.from_config(configuration)
        self.logger = kwargs.get("logger")
        self.tickers = {}

    async def fetch_markets(
        self,
        params: dict,
    ):
        """
        Fetches the markets.

        :return: The markets.
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
            raise SorRetrievalException(
                f"Error fetching markets from chainId {self.chain_name} Balancer: {exc}"
            ) from exc

    async def fetch_balances(self, *args, **kwargs):
        """
        Fetches the balances.

        :return: The balances.
        """
        del args, kwargs
        balances = Balances(
            balances=[
                Balance(
                    asset_id=LEDGER_TO_STABLECOINS[self.ledger_id][0],
                    free=0,
                    used=0,
                    total=0,
                )
            ]
        )
        return balances

    @property
    def pool_ids(self):
        """
        Get the pool IDs.

        :return: The pool IDs.
        """
        # We read in the pool IDs from a file for now. we get this file from https://github.com/balancer/frontend-v2/blob/8563b8d33b6bff266148bd48d7ebc89f921374f4/src/lib/config/mainnet/pools.ts#L296
        with open(
            Path(__file__).parent / "data" / "balancer" / f"{self.balancer_deployment.value}.json",
            "r",
            encoding=DEFAULT_ENCODING,
        ) as file:
            json_data = json.loads(file.read())["pools"]
        if "Element" in json_data:
            del json_data["Element"]
        return json_data

    async def fetch_tickers(self, *args, **kwargs):
        """
        Fetches the tickers.

        :return: The tickers.
        """

        # We temporarily assume that the tickers are the same as the markets, and use the pool IDs to get the tickers.

        await self.fetch_markets(*args, **kwargs)

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
            raise SorRetrievalException("No pools of interest found!")
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
        for address, name, symbol in zip(self.bal.decimals, name_data[0], symbol_data[0]):
            print(address, name[0], symbol[0])
            if address not in self.tokens:
                self.tokens[address] = Erc20Token(
                    address=address,
                    symbol=symbol[0],
                    name=name[0],
                    decimals=18,
                )
            # We now get get the price for the swap
            # We now make an erc20 representation of the token.

        self.tickers = {}
        for token_address in LEDGER_TO_TOKEN_LIST[self.ledger_id]:
            if token_address in LEDGER_TO_STABLECOINS[self.ledger_id]:
                continue

            stable_address = LEDGER_TO_STABLECOINS[self.ledger_id][0]
            token = self.tokens[token_address]

            # TODO Ensure we handle Decimals in the behaviours.  # pylint: disable=W0511
            ask_price = 1 / float(
                self.get_price(
                    amount=DEFAULT_AMOUNT_USD, output_token_address=token_address, input_token_address=stable_address
                )
            )
            buy_amount = DEFAULT_AMOUNT_USD / ask_price

            bid_price = 1 / float(
                1
                / self.get_price(
                    amount=buy_amount, output_token_address=stable_address, input_token_address=token_address
                )
            )
            symbol = f"{token.address}/{stable_address}"
            ticker = Ticker(
                symbol=symbol,
                high=ask_price,
                low=bid_price,
                ask=ask_price,
                bid=bid_price,
            )
            self.tickers[symbol] = ticker
        return Tickers(tickers=list(ticker for ticker in self.tickers.values()))

    def get_params_for_swap(self, input_token_address, output_token_address, input_amount, is_buy=False):
        """
        Given the data, we get the params for the swap from the balancer exchange.
        """
        gas_price = self.bal.web3.eth.gas_price * GAS_PRICE_PREMIUM
        params = {
            "network": self.balancer_deployment.value,
            "slippageTolerancePercent": "1.0",  # 1%
            "sor": {
                "sellToken": input_token_address,
                "buyToken": output_token_address,  # // token out
                "orderKind": "buy" if is_buy else "sell",
                "amount": input_amount,
                "gasPrice": gas_price,
            },
            "batchSwap": {
                "funds": {
                    "sender": self.account.address,  #      // your address
                    "recipient": self.account.address,  #   // your address
                    "fromInternalBalance": False,  # // to/from internal balance
                    "toInternalBalance": False,  # // set to "false" unless you know what you're doing
                },
                # // unix timestamp after which the trade will revert if it hasn't executed yet
                "deadline": datetime.now().timestamp() + 60,
            },
        }

        return params

    def get_price(self, input_token_address: str, output_token_address: str, amount: float) -> float:
        """
        Get the price of the token.
        """

        params = self.get_params_for_swap(
            input_token_address=input_token_address,
            output_token_address=output_token_address,
            input_amount=amount,
        )
        # we query the smart router
        try:
            sor_result = self.bal.balSorQuery(params)
        except Exception as exc:  # pylint: disable=W0718
            self.logger.error(exc)
            self.logger.error(f"Error querying SOR: {traceback.format_exc()}")
        if not sor_result["batchSwap"]["limits"]:
            raise SorRetrievalException(
                f"No limits found for swap. Implies incorrect configuration of swap params: {params}"
            )
        amount_out = float(sor_result["batchSwap"]["limits"][-1])
        output_amount = -amount_out
        rate = Decimal(output_amount) / Decimal(amount)
        return rate

    async def fetch_ticker(self, *args, **kwargs):
        """
        Fetches a ticker.

        :return: The ticker.
        """
        del args, kwargs
        raise NotImplementedError

    async def fetch_positions(self, **kwargs):
        """
        Fetches the positions, notice as this is a balancer exchange, we do not have positions.
        We therefore return an empty list.

        :return: The
        """
        del kwargs
        return []

    async def create_order(
        self,
        *args,
        retries=1,
        **kwargs,
    ) -> Order:
        """
        Create an order.

        :return: The order.
        """
        print(f"Creating order with args: {args} and kwargs: {kwargs}")

        symbol = kwargs.get("symbol", None)
        if not symbol:
            raise ValueError("Symbol not provided to create order")

        input_token_address, output_token_address = symbol.split("/")
        human_amount = kwargs.get("amount", None)
        if not human_amount:
            raise ValueError("Size not provided to create order")
        machine_amount = self.tokens[input_token_address].to_machine(human_amount)
        amount = human_amount

        params = self.get_params_for_swap(
            input_token_address=input_token_address,
            output_token_address=output_token_address,
            input_amount=amount,
            is_buy=True,
        )
        try:
            sor_result = self.bal.balSorQuery(params)
        except Exception as exc:  # pylint: disable=W0703
            self.logger.error(exc)
            self.logger.error(f"Error querying SOR: {traceback.format_exc()}")
            raise SorRetrievalException(f"Error querying SOR: {exc}") from exc

        swap = sor_result["batchSwap"]
        self.logger.info(
            f"Recommended swap: for {human_amount} {input_token_address} -> {output_token_address}\n"
            + f"{json.dumps(swap, indent=4)}"
        )
        tokens = swap["assets"]
        limits = swap["limits"]
        if not tokens or not limits:
            self.logger("Problem with SOR retrieval!!")
            if retries > 0:
                self.logger(f"Retrying transaction. {retries} retries left")
                return self.create_order(*args, **kwargs, retries=retries - 1)
            raise SorRetrievalException(f"No tokens {tokens} or limits: {limits} provided in swap")

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
        return fnc(swap, symbol, input_token_address, machine_amount, safe_address=safe_contract_address)

    def _handle_safe_txn(self, swap, symbol, input_token_address, machine_amount, safe_address) -> Order:
        """
        Handle the EOA transaction.
        """

        vault = self.bal.balLoadContract("Vault")

        swap["funds"]["sender"] = safe_address
        swap["funds"]["recipient"] = safe_address

        # Note this is a place holder for the approval amount assuming we have approved the token.
        approved = 99999999999999999999999

        # We approve the token if we have not already done so.

        if approved < machine_amount:
            self.logger.info(f"Approving {machine_amount} {input_token_address} for {vault.address}")
            contract = self.bal.erc20GetContract(input_token_address)
            data = contract.encodeABI("approve", [vault.address, machine_amount])

        else:
            try:
                mc_args = self.bal.balFormatBatchSwapData(swap)
                vault = self.bal.balLoadContract("Vault")
                function_name = "batchSwap"
                data = vault.encodeABI(function_name, mc_args)
            except web3.exceptions.ContractLogicError as exc:
                self.logger.error(exc)
                self.logger.error(f"Error calling batchSwapFn: {traceback.format_exc()}")
                if "BAL#508" in str(exc):
                    raise ExchangeError(
                        "SWAP_DEADLINE: Swap transaction not mined within the specified deadline"
                    ) from exc
                if "execution reverted: ERC20: transfer amount exceeds allowance" in str(exc):
                    raise ApprovalError("ERC20: transfer amount exceeds allowance") from exc
                raise SorRetrievalException(f"Error calling batchSwapFn: {exc}") from exc

        return Order(
            exchange_id="balancer",
            symbol=symbol,
            data={
                "data": data,
                "vault_address": vault.address,
                "chain_id": self.bal.web3.eth.chain_id,
            },
        )

    def _handle_eoa_txn(  # pylint: disable=unused-argument
        self, swap, symbol, input_token_address, machine_amount, **kwargs
    ) -> Order:  # pylint: disable=unused-argument
        """
        Handle the EOA transaction.
        """

        vault = self.bal.balLoadContract("Vault")

        approved = self.bal.erc20GetAllowanceStandard(
            tokenAddress=input_token_address,
            allowedAddress=vault.address,
        )

        # We approve the token if we have not already done so.

        if approved < machine_amount:
            self.logger.info(f"Approving {machine_amount} {input_token_address} for {vault.address}")
            contract = self.bal.erc20GetContract(input_token_address)
            data = contract.encodeABI("approve", [vault.address, machine_amount])

        else:
            try:
                mc_args = self.bal.balFormatBatchSwapData(swap)
                vault = self.bal.balLoadContract("Vault")
                function_name = "batchSwap"
                data = vault.encodeABI(function_name, mc_args)
                fn = vault.get_function_by_name(fn_name=function_name)
                # Assuming this does not revert, we have our call data for the order.
                fn(*mc_args).call()
            except web3.exceptions.ContractLogicError as exc:
                self.logger.error(exc)
                self.logger.error(f"Error calling batchSwapFn: {traceback.format_exc()}")
                if "BAL#508" in str(exc):
                    raise ExchangeError(
                        "SWAP_DEADLINE: Swap transaction not mined within the specified deadline"
                    ) from exc
                if "execution reverted: ERC20: transfer amount exceeds allowance" in str(exc):
                    raise ApprovalError(f"ERC20: transfer amount exceeds allowance: {exc}") from exc
                raise SorRetrievalException(f"Error calling batchSwapFn: {exc}") from exc

        return Order(
            exchange_id="balancer",
            symbol=symbol,
            data={
                "data": data,
                "vault_address": vault.address,
                "chain_id": self.bal.web3.eth.chain_id,
            },
        )

    def parse_order(self, order, *args, **kwargs):
        """
        Parse the order.

        :return: The order.
        """
        del args, kwargs
        return order

    async def cancel_order(self, *args, **kwargs):
        """
        Cancel an order.

        :return: The order tx hash

        NOTE: This method is not implemented as we dont have orders in balancer.

        in the future, we would look to get pending orders in
        the mempool and replace with a 0 transfer of the same hash.

        """
        del args, kwargs
        raise NotImplementedError

    async def get_order(self, *args, **kwargs):
        """
        Get an order.

        :return: The order.
        """
        del args, kwargs
        raise NotImplementedError

    async def fetch_open_orders(self, *args, **kwargs):
        """
        Get an order.

        :return: The orders as an array.

        NOTE: This method is not implemented as we dont have orders in balancer.

        However, further work would be to implement this method to get the orders from the balancer exchange.

        This would get the pending order from the mempool, and the filled orders from the chain.

        """
        del args, kwargs
        return Orders(orders=[])

    async def get_all_markets(self, *args, **kwargs):
        """
        Get all markets.

        :return: The markets.
        """
        del args, kwargs
        raise NotImplementedError

    async def subscribe(self, *args, **kwargs):
        """
        Subscribe to the order book.

        :return: The order book.
        """
        del args, kwargs
        raise NotImplementedError

    async def close(self):
        """
        Close the connection.

        :return: None
        """
        return None

    async def fetch_balance(self, *args, **kwargs):
        """
        Fetch the balance.

        :return: The balance.
        """
        del args, kwargs

        mc = self.bal.mc
        # We iterate over all the whitelisted tokens and get the balances.
        mc.reset()
        for token_address in LEDGER_TO_TOKEN_LIST[self.ledger_id]:
            if token_address not in self.tokens:
                continue
            contract = self.bal.erc20GetContract(token_address)
            mc.addCall(
                token_address,
                contract.abi,
                "balanceOf",
                args=[self.account.address],
            )
        balance_data = mc.execute()
        balances = Balances(
            balances=[
                Balance(
                    asset_id=token_address,
                    free=balance[0],
                    used=0,
                    total=balance[0],
                )
                for token_address, balance in zip(LEDGER_TO_TOKEN_LIST[self.ledger_id], balance_data[0])
            ]
        )
        return balances
