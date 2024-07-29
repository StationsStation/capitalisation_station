"""
Balancer exchange.
"""
import json
from glob import glob
from pathlib import Path

from aea_ledger_ethereum import Account
from balpy import balpy

from packages.eightballer.connections.dcxt.dcxt.exceptions import ConfigurationError, SorRetrievalException
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue
from packages.eightballer.protocols.positions.message import PositionsMessage

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

BASE_ASSET_ID = '0x6b175474e89094c44da98b954eedeac495271d0f'


class BalancerClient:
    """
    Balancer exchange.
    """

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
                    asset_id=BASE_ASSET_ID,
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

        params = self.pool_ids

        self.bal.getOnchainData(params)
        # We setup a mulkticall to ensure we have the name of all of the pools.
        self.bal.mc.reset()
        for token_address in self.bal.decimals:
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
            contract = self.bal.erc20GetContract(token_address)
            self.bal.mc.addCall(
                token_address,
                contract.abi,
                'symbol',
                args=[],
            )
        symbol_data = self.bal.mc.execute()

        for address, name, symbol in zip(self.bal.decimals, name_data[0], symbol_data[0]):
            print(address, name[0], symbol[0])
        del args, kwargs

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
