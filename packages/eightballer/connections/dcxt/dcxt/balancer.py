"""
Balancer exchange.
"""
import json
import traceback

# pylint: disable=R0914,R0902,R0912
from datetime import datetime
from decimal import Decimal
from glob import glob
from pathlib import Path
from typing import cast

import web3
from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration
from aea.contracts.base import Contract
from aea_ledger_ethereum import Account
from balpy import balpy

from packages.eightballer.connections.dcxt.dcxt.exceptions import ConfigurationError, SorRetrievalException
from packages.eightballer.connections.dcxt.erc_20.contract import Erc20Token
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.protocols.orders.custom_types import Order, Orders
from packages.eightballer.protocols.tickers.custom_types import Ticker, Tickers

GAS_PRICE_PREMIUM = 20
GAS_SPEED = "fast"
GAS_PRICE = 888


DEFAULT_ENCODING = "utf-8"


PACKAGE_DIR = Path(__file__).parent
ABI_DIR = PACKAGE_DIR / "abis"

ABI_MAPPING = {
    Path(path)
    .stem.upper(): open(path, encoding=DEFAULT_ENCODING)  # pylint: disable=R1732
    .read()  # pylint: disable=R1732
    for path in glob(str(ABI_DIR / "*.json"))
}

ETH_KEYPATH = 'ethereum_private_key.txt'

OLAS_ADDRESS = '0x0001a500a6b18995b03f44bb040a5ffc28e45cb0'
USDC_ADDRESS = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
WETH_ADDRESS = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'

# Manuall retrieved from https://balancer.fi/pools/ethereum/v2/
WHITELISTED_POOLS = [
    '0xebdd200fe52997142215f7603bc28a80becdadeb000200000000000000000694',
    '0x96646936b91d6b9d7d0c47c496afbf3d6ec7b6f8000200000000000000000019',
]

WHITE_LISTED_TOKENS = [OLAS_ADDRESS, USDC_ADDRESS, WETH_ADDRESS]

DEFAULT_AMOUNT_USD = 1


class BalancerClient:
    """
    Balancer exchange.
    """

    tokens: dict[str:Erc20Token] = {}

    def __init__(self, *args, **kwargs):  # pylint: disable=super-init-not-called
        del args
        custom_kwargs = kwargs.get("kwargs", {})
        self.chain_name = custom_kwargs.get("chain_id")
        if not self.chain_name:
            raise ConfigurationError("Chain name not provided to BalancerClient")

        self.rpc_url = custom_kwargs.get("rpc_url")
        if not self.rpc_url:
            raise ConfigurationError("RPC URL not provided to BalancerClient")

        self.etherscan_api_key = custom_kwargs.get("etherscan_api_key")
        if not self.etherscan_api_key:
            raise ConfigurationError("Etherscan API key not provided to BalancerClient")

        self.account = Account.from_key(  # pylint: disable=E1120
            private_key=kwargs.get('auth').get("private_key").strip()
        )  # pylint: disable=E1120
        self.bal: balpy.balpy = balpy.balpy(
            self.chain_name,
            manualEnv={
                "privateKey": self.account._private_key,
                "customRPC": self.rpc_url,
                "etherscanApiKey": self.etherscan_api_key,
            },
        )

        self.gas_price = kwargs.get("gas_price", None)
        self.gas_price_premium = kwargs.get("gas_price_premium", GAS_PRICE_PREMIUM)

        contract_dir = Path(__file__).parent.parent.parent.parent / 'contracts' / 'erc_20'

        configuration = cast(
            ContractConfig,
            load_component_configuration(
                ComponentType.CONTRACT, Path(__file__).parent.parent.parent.parent / 'contracts' / 'erc_20'
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
                    'id': pool_id,
                    'symbol': 'OLAS/USDC',
                    'base': 'OLAS',
                    'quote': 'USDC',
                    'spot': True,
                }
                for pool_id in self.pool_ids
            ]
            return Markets(
                markets=[Market(**market) for market in markets],
            )
        except SorRetrievalException as exc:
            raise SorRetrievalException(
                f'Error fetching markets from chainId {self.chain_name} Balancer: {exc}'
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
                    asset_id=USDC_ADDRESS,
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
        # We read in the pool IDs from a file for now.
        with open(Path(__file__).parent / 'data' / 'balancer' / "mainnet.json", "r", encoding=DEFAULT_ENCODING) as file:
            json_data = json.loads(file.read())['pools']
        if 'Element' in json_data:
            del json_data['Element']
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
                if pool_id.lower() in WHITELISTED_POOLS:
                    if pool_type not in pools_of_interest:
                        pools_of_interest[pool_type] = [pool_id]
                    else:
                        pools_of_interest[pool_type].append(pool_id)

        if not pools_of_interest:
            raise SorRetrievalException("No pools of interest found!")
        self.bal.getOnchainData(pools_of_interest)
        # We setup a mulkticall to ensure we have the name of all of the pools.

        self.bal.mc.reset()
        for token_address in self.bal.decimals:
            if token_address not in WHITE_LISTED_TOKENS:
                continue

            contract = self.bal.erc20GetContract(token_address)
            self.bal.mc.addCall(
                token_address,
                contract.abi,
                'name',
                args=[],
            )
        name_data = self.bal.mc.execute()

        # We now get the symbols
        self.bal.mc.reset()
        for token_address in self.bal.decimals:
            if token_address not in WHITE_LISTED_TOKENS:
                continue
            contract = self.bal.erc20GetContract(token_address)
            self.bal.mc.addCall(
                token_address,
                contract.abi,
                'symbol',
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
        for token_address in WHITE_LISTED_TOKENS:
            if token_address == USDC_ADDRESS:
                continue

            token = self.tokens[token_address]

            # TODO Ensure we handle Decimals in the behaviours.  # pylint: disable=W0511
            ask_price = 1 / float(
                self.get_price(
                    amount=DEFAULT_AMOUNT_USD, output_token_address=token_address, input_token_address=USDC_ADDRESS
                )
            )
            buy_amount = DEFAULT_AMOUNT_USD / ask_price

            bid_price = 1 / float(
                1
                / self.get_price(
                    amount=buy_amount, output_token_address=USDC_ADDRESS, input_token_address=token_address
                )
            )
            symbol = f'{token.symbol}/USDC'
            symbol = f'{token.address}/{USDC_ADDRESS}'
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
            "network": self.chain_name,
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
        if not sor_result['batchSwap']['limits']:
            raise SorRetrievalException(
                f"No limits found for swap. Implies incorrect configuration of swap params: {params}"
            )
        amount_out = float(sor_result['batchSwap']['limits'][-1])
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

    async def create_order(self, retries=1, *args, **kwargs) -> Order:
        """
        Create an order.

        :return: The order.
        """
        print(f"Creating order with args: {args} and kwargs: {kwargs}")

        symbol = kwargs.get("symbol", None)
        if not symbol:
            raise ValueError("Symbol not provided to create order")

        input_token_address, output_token_address = symbol.split('/')
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
            raise SorRetrievalException(f"Error querying SOR: {exc}")

        swap = sor_result["batchSwap"]
        self.logger.info(
            f"Recommended swap: for {human_amount} {input_token_address} -> {output_token_address}\n {json.dumps(swap, indent=4)}"
        )
        tokens = swap["assets"]
        limits = swap["limits"]
        if not tokens or not limits:
            self.log("Problem with SOR retrieval!!")
            if retries > 0:
                self.log(f"Retrying transaction. {retries} retries left")
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

        swap['funds']['sender'] = safe_address
        swap['funds']['recipient'] = safe_address

        # approved = self.bal.erc20GetAllowanceStandard(
        #     tokenAddress=input_token_address,
        #     allowedAddress=vault.address,
        # )

        approved = 99999999999999999999999

        # We approve the token if we have not already done so.

        if approved < machine_amount:
            self.logger.info(f"Approving {machine_amount} {input_token_address} for {vault.address}")
            contract = self.bal.erc20GetContract(input_token_address)
            data = contract.encodeABI('approve', [vault.address, machine_amount])

        else:
            try:
                mc_args = self.bal.balFormatBatchSwapData(swap)
                vault = self.bal.balLoadContract("Vault")
                function_name = 'batchSwap'
                data = vault.encodeABI(function_name, mc_args)
            except web3.exceptions.ContractLogicError as exc:
                self.logger.error(exc)
                self.logger.error(f"Error calling batchSwapFn: {traceback.format_exc()}")
                if 'BAL#508' in str(exc):
                    raise ValueError("SWAP_DEADLINE: Swap transaction not mined within the specified deadline")
                if 'execution reverted: ERC20: transfer amount exceeds allowance' in str(exc):
                    raise ValueError("ERC20: transfer amount exceeds allowance")
                raise SorRetrievalException(f"Error calling batchSwapFn: {exc}")

        return Order(
            exchange_id="balancer",
            symbol=symbol,
            data={
                "data": data,
                'vault_address': vault.address,
                'chain_id': self.bal.web3.eth.chain_id,
            },
        )

    def _handle_eoa_txn(self, swap, symbol, input_token_address, machine_amount, **kwargs) -> Order:
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
            data = contract.encodeABI('approve', [vault.address, machine_amount])

        else:
            try:
                mc_args = self.bal.balFormatBatchSwapData(swap)
                vault = self.bal.balLoadContract("Vault")
                function_name = 'batchSwap'
                data = vault.encodeABI(function_name, mc_args)
                batchSwapFn = vault.get_function_by_name(fn_name=function_name)
                # Assuming this does not revert, we have our call data for the order.
                batchSwapFn(*mc_args).call()
            except web3.exceptions.ContractLogicError as exc:
                self.logger.error(exc)
                self.logger.error(f"Error calling batchSwapFn: {traceback.format_exc()}")
                if 'BAL#508' in str(exc):
                    raise ValueError("SWAP_DEADLINE: Swap transaction not mined within the specified deadline")
                if 'execution reverted: ERC20: transfer amount exceeds allowance' in str(exc):
                    raise ValueError("ERC20: transfer amount exceeds allowance")
                raise SorRetrievalException(f"Error calling batchSwapFn: {exc}")

        return Order(
            exchange_id="balancer",
            symbol=symbol,
            data={
                "data": data,
                'vault_address': vault.address,
                'chain_id': self.bal.web3.eth.chain_id,
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
        for token_address in WHITE_LISTED_TOKENS:
            if token_address not in self.tokens:
                continue
            contract = self.bal.erc20GetContract(token_address)
            mc.addCall(
                token_address,
                contract.abi,
                'balanceOf',
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
                for token_address, balance in zip(WHITE_LISTED_TOKENS, balance_data[0])
            ]
        )
        return balances
