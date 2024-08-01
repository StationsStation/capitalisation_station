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

from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration
from aea.contracts.base import Contract
from aea_ledger_ethereum import Account
from balpy import balpy

from packages.eightballer.connections.dcxt.dcxt.exceptions import ConfigurationError, SorRetrievalException
from packages.eightballer.contracts.erc_20.contract import Erc20, Erc20Token
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.protocols.tickers.custom_types import Ticker

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

WHITELISTED_POOLS = ['0xebdd200fe52997142215f7603bc28a80becdadeb000200000000000000000694']

WHITE_LISTED_TOKENS = [OLAS_ADDRESS, USDC_ADDRESS]

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
        self.bal = balpy.balpy(
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
        self.erc20_contract = Contract.from_config(configuration)
        self.logger = kwargs.get("logger")

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
        tickers = []
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

        for token_address in WHITE_LISTED_TOKENS:
            if token_address == USDC_ADDRESS:
                continue

            token = self.tokens[token_address]
            Erc20(self.erc20_contract)

            bid_price = self.get_price(
                amount=DEFAULT_AMOUNT_USD, output_token_address=token_address, input_token_address=USDC_ADDRESS
            )
            sell_amount = bid_price * DEFAULT_AMOUNT_USD
            ask_price = 1 / self.get_price(
                amount=sell_amount, output_token_address=USDC_ADDRESS, input_token_address=token_address
            )
            ticker = Ticker(
                symbol=f'{token.symbol}/USDC',
                high=ask_price,
                low=bid_price,
                ask=ask_price,
                bid=bid_price,
            )
            tickers.append(ticker)
        return tickers

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

    async def fetch_positions(self, positions_message: PositionsMessage, dialogue: PositionsDialogue, **kwargs):
        """
        Fetches a ticker.

        :return: The ticker.
        """
        del kwargs
        return dialogue.reply(
            performative=PositionsMessage.Performative.ERROR,
            target_message=positions_message,
            error_code=PositionsMessage.ErrorCode.API_ERROR,
            error_msg="Spot exchange does not support positions!",
        )

    async def create_order(self, *args, **kwargs):
        """
        Create an order.

        :return: The order.
        """
        del args, kwargs
        raise NotImplementedError

    async def cancel_order(self, *args, **kwargs):
        """
        Cancel an order.

        :return: The order.
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

    async def get_orders(self, *args, **kwargs):
        """
        Get an order.

        :return: The order.
        """
        del args, kwargs
        raise NotImplementedError

    async def get_all_markets(self, *args, **kwargs):
        """
        Get all markets.

        :return: The markets.
        """
        del args, kwargs
        raise NotImplementedError

    async def get_all_balances(self, *args, **kwargs):
        """
        Get all balances.

        :return: The balances.
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
