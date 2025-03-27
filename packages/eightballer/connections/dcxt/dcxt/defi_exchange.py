"""Base exchange to be used to for erc20 exchanges."""

from functools import cache

from web3 import Web3
from multicaller import multicaller
from aea_ledger_ethereum import EthereumApi, EthereumCrypto
from aea.configurations.base import PublicId

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.connections.dcxt.erc_20.contract import Erc20Token
from packages.eightballer.connections.dcxt.dcxt.data.tokens import (
    LEDGER_TO_TOKEN_LIST,
    LEDGER_TO_NATIVE_SYMBOL,
    SupportedLedgers,
    read_token_list,
)


LEDGER_TO_CHAIN_ID = {"ethereum": 1, "gnosis": 100, "base": 8453}


class BaseErc20Exchange:
    """Base exchange to be used to for erc20 exchanges."""

    tokens: dict[str, Erc20Token] = {}

    def __init__(self, ledger_id, rpc_url, key_path, logger, *args, **kwargs):
        """Initialize the exchange."""
        del args, kwargs
        self.web3 = EthereumApi(
            address=rpc_url,
        )
        self.account = EthereumCrypto(private_key_path=key_path)
        self.ledger_id = SupportedLedgers(ledger_id)

        self.mc = multicaller.multicaller(
            _chainId=LEDGER_TO_CHAIN_ID[ledger_id],
            _web3=self.web3.api,
            _maxRetries=5,
            _verbose=False,
            _allowFailure=True,
        )
        self.logger = logger

        self.erc20_contract = load_contract(PublicId.from_str("eightballer/erc_20:0.1.0"))
        self.raw_token_data = read_token_list(LEDGER_TO_CHAIN_ID[ledger_id])
        self.names_to_addresses = {v["symbol"]: k for k, v in self.raw_token_data.items()}
        self.tokens = {}

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

    @cache  # noqa
    def get_token(self, address):
        """Get the token from the address."""
        # We check if the token is already in the raw token data.
        address = Web3.to_checksum_address(address)
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

        name = self.erc20_contract.name(
            self.web3,
            address,
        )["str"]
        symbol = self.erc20_contract.symbol(
            self.web3,
            address,
        )["str"]
        decimals = self.erc20_contract.decimals(
            self.web3,
            address,
        )["int"]
        self.tokens[address] = Erc20Token(
            address=address,
            name=name,
            symbol=symbol,
            decimals=decimals,
        )
        return self.get_token(address)

    async def fetch_balance(self, *args, **kwargs) -> Balances:
        """Fetch the balance.

        :return(Balances): The balance.
        """
        del args

        self.mc.reset()
        use_external_address = kwargs.get("address", None)
        address_to_check = use_external_address or self.account.address
        self.logger.debug(
            f"Checking balance for {address_to_check} with for tokens {LEDGER_TO_TOKEN_LIST[self.ledger_id]}"
        )
        abi = self.erc20_contract.get_instance(self.web3).abi

        for token_address in LEDGER_TO_TOKEN_LIST[self.ledger_id]:
            self.mc.addCall(
                token_address,
                abi,
                "balanceOf",
                args=[address_to_check],
            )
        balance_data = self.mc.execute()
        native = self.web3.api.eth.get_balance(address_to_check)

        return Balances(
            balances=[
                self._from_decimals_amt_to_token(token_address, balance[0])
                for token_address, balance in zip(LEDGER_TO_TOKEN_LIST[self.ledger_id], balance_data[0], strict=False)
            ]
            + [
                Balance(
                    asset_id=LEDGER_TO_NATIVE_SYMBOL[self.ledger_id],
                    free=Web3.from_wei(native, "ether"),
                    total=Web3.from_wei(native, "ether"),
                    is_native=True,
                    used=0,
                )
            ]
        )
