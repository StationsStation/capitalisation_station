"""Base exchange to be used to for erc20 exchanges."""

import contextlib
from typing import Any, cast
from functools import cache, lru_cache

import requests
from web3 import Web3
from multicaller import multicaller
from aea_ledger_ethereum import (
    HexBytes,
    JSONLike,
    EthereumApi,
    EthereumCrypto,
    SignedTransaction,
    try_decorator,
)
from aea.configurations.base import PublicId

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.connections.dcxt.dcxt.exceptions import RpcError, BadSymbol
from packages.eightballer.connections.dcxt.erc_20.contract import Erc20, Erc20Token
from packages.eightballer.connections.dcxt.dcxt.data.tokens import (
    LEDGER_TO_TOKEN_LIST,
    LEDGER_TO_NATIVE_SYMBOL,
    SupportedLedgers,
    read_token_list,
)


LEDGER_TO_CHAIN_ID = {
    SupportedLedgers.ETHEREUM: 1,
    SupportedLedgers.GNOSIS: 100,
    SupportedLedgers.BASE: 8453,
    SupportedLedgers.ARBITRUM: 42161,
    SupportedLedgers.POLYGON: 137,
}


class SignedTransactionTranslator:
    """Translator for SignedTransaction."""

    @staticmethod
    def to_dict(signed_transaction: SignedTransaction) -> dict[str, str | int]:
        """Write SignedTransaction to dict."""
        signed_transaction_dict: dict[str, str | int] = {
            "raw_transaction": cast(str, signed_transaction.raw_transaction.hex()),
            "hash": cast(str, signed_transaction.hash.hex()),
            "r": cast(int, signed_transaction.r),
            "s": cast(int, signed_transaction.s),
            "v": cast(int, signed_transaction.v),
        }
        return signed_transaction_dict

    @staticmethod
    def from_dict(signed_transaction_dict: JSONLike) -> SignedTransaction:
        """Get SignedTransaction from dict."""
        if not isinstance(signed_transaction_dict, dict) and len(signed_transaction_dict) == 5:
            msg = f"Invalid for conversion. Found object: {signed_transaction_dict}."
            raise ValueError(  # pragma: nocover
                msg
            )
        return SignedTransaction(
            raw_transaction=HexBytes(cast(str, signed_transaction_dict["raw_transaction"])),
            hash=HexBytes(cast(str, signed_transaction_dict["hash"])),
            r=cast(int, signed_transaction_dict["r"]),
            s=cast(int, signed_transaction_dict["s"]),
            v=cast(int, signed_transaction_dict["v"]),
        )


def signed_tx_to_dict(signed_transaction: Any) -> dict[str, str | int]:
    """Write SignedTransaction to dict."""
    signed_transaction_dict: dict[str, str | int] = {
        "raw_transaction": cast(str, signed_transaction.raw_transaction.hex()),
        "hash": cast(str, signed_transaction.hash.hex()),
        "r": cast(int, signed_transaction.r),
        "s": cast(int, signed_transaction.s),
        "v": cast(int, signed_transaction.v),
    }
    return signed_transaction_dict


@try_decorator("Unable to send transaction: {}", logger_method="warning")
def try_send_signed_transaction(ethereum_api: EthereumApi, tx_signed: JSONLike, **_kwargs: Any) -> str | None:
    """Try send a raw signed transaction."""
    signed_transaction = SignedTransactionTranslator.from_dict(tx_signed)
    hex_value = ethereum_api.api.eth.send_raw_transaction(  # pylint: disable=no-member
        signed_transaction.raw_transaction
    )
    tx_digest = hex_value.hex()
    if not tx_digest.startswith("0x"):
        tx_digest = "0x" + tx_digest
    return tx_digest


def sign_and_send_txn(txn, crypto, ledger_api):
    """Sign and send transaction."""

    def _sign_swap_txn(swap_transaction):
        """Sign the swap transaction."""
        return signed_tx_to_dict(crypto.entity.sign_transaction(swap_transaction))

    signed_txn = _sign_swap_txn(txn)
    txn_hash = try_send_signed_transaction(ledger_api, signed_txn)
    with contextlib.suppress(Exception):
        result = ledger_api.api.eth.wait_for_transaction_receipt(txn_hash, timeout=600)
        if result.get("status") == 0:
            return False, txn_hash
    return True, txn_hash


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
            _chainId=LEDGER_TO_CHAIN_ID[self.ledger_id],
            _web3=self.web3.api,
            _maxRetries=10,
            _verbose=False,
            _allowFailure=True,
        )
        self.logger = logger

        self.erc20_contract: Erc20 = load_contract(PublicId.from_str("eightballer/erc_20:0.1.0"))
        self.raw_token_data = read_token_list(LEDGER_TO_CHAIN_ID[self.ledger_id])
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

        try:
            balance_data = self.mc.execute()
            native = self.web3.api.eth.get_balance(address_to_check)
        except requests.exceptions.HTTPError as err:
            self.logger.exception(f"Error fetching balance: {err}")
            msg = "Error fetching balance"
            raise RpcError(msg) from err

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

    @classmethod
    @lru_cache(
        maxsize=128,
    )
    def look_up_by_symbol(cls, symbol: str, ledger: SupportedLedgers) -> Erc20Token:
        """Look up a token by symbol."""
        token_list = read_token_list(LEDGER_TO_CHAIN_ID[ledger])
        for token, data in token_list.items():
            if data["symbol"] == symbol:
                return Erc20Token(
                    address=token,
                    symbol=data["symbol"],
                    decimals=data["decimals"],
                    name=data["name"],
                )
        return None

    def set_approval(self, asset_id, amount, is_eoa):
        """Set approval for an asset."""
        self.logger.info(f"Setting approval for {asset_id} on {self.exchange_id}")
        token = self.look_up_by_symbol(asset_id, ledger=self.supported_ledger)
        if not token:
            msg = f"Token {asset_id} not found for exchange {self.exchange_id} on ledger {self.ledger_id}"
            raise BadSymbol(msg)

        if is_eoa:
            current_approval = self.erc20_contract.allowance(
                self.web3,
                token.address,
                self.account.address,
                self.spender_address,
            )["int"]
            if current_approval >= amount:
                self.logger.info(f"Approval already set for {token.symbol} on {self.exchange_id}")
                return
            self.logger.info(f"Setting approval for {token.symbol} on {self.exchange_id}")
            func = self.erc20_contract.approve(
                ledger_api=self.web3,
                contract_address=token.address,
                to=self.spender_address,
                value=amount,
            )
            # we call it to verify it will succeed
            func.call(
                {"from": self.account.address},
            )
            txn_data = func.build_transaction(
                {
                    "from": self.account.address,
                    "gas": 1000000,
                    "gasPrice": self.web3.api.eth.gas_price * 5,
                    "nonce": self.web3.api.eth.get_transaction_count(self.account.address),
                }
            )
            result, txn_hash = sign_and_send_txn(
                txn_data,
                self.account,
                self.web3,
            )
            if not result:
                msg = f"Transaction failed: {txn_hash}"
                raise RpcError(msg)
            self.logger.info(f"Transaction sent: {txn_hash} with result: {result}")

    @property
    def spender_address(self):
        """Get the spender address."""
        msg = "Spender address not implemented"
        raise NotImplementedError(msg)  # pragma: no cover
