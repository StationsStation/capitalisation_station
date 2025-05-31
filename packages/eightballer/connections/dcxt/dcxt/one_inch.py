"""Class for interacting with the 1inch API."""

import os
import sys
import asyncio
import logging
import contextlib
from typing import TYPE_CHECKING, Any, cast
from decimal import Decimal
from datetime import datetime
from functools import cache
from dataclasses import dataclass

import click
import httpx
from web3 import Web3
from web3.exceptions import TimeExhausted
from aea_ledger_ethereum import (
    Address,
    HexBytes,
    JSONLike,
    EthereumApi,
    EthereumCrypto,
    SignedTransaction,
    try_decorator,
)
from aea.configurations.base import PublicId

from packages.eightballer.connections.dcxt.utils import load_contract
from packages.eightballer.protocols.orders.custom_types import (
    Order,
    OrderSide,
    OrderType,
    OrderStatus,
)
from packages.eightballer.protocols.tickers.custom_types import Ticker
from packages.eightballer.connections.dcxt.dcxt.data.tokens import SupportedLedgers
from packages.eightballer.connections.dcxt.dcxt.defi_exchange import BaseErc20Exchange


if TYPE_CHECKING:
    from packages.eightballer.connections.dcxt.erc_20.contract import Erc20


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


class InvalidSwapParams(Exception):
    """Exception raised for invalid swap parameters."""


class InsufficientBalance(Exception):
    """Exception raised for insufficient balance."""


class InsufficientAllowance(Exception):
    """Exception raised for insufficient allowance."""


SPENDER = {"ethereum": "0x111111125421cA6dc452d289314280a0f8842A65"}

LEDGER_TO_CHAIN_ID = {
    SupportedLedgers.ETHEREUM: 1,
    SupportedLedgers.GNOSIS: 100,
    SupportedLedgers.BASE: 8453,
}


@dataclass
class OneInchSwapParams:
    """This class is used to define the swap parameters for the 1inch API."""

    src: str
    dst: str
    amount: str
    slippage: int
    from_: str
    disable_estimate: bool
    allow_partial_fill: bool
    fee: int = 0.0  # percentate fee ie. 0.001 = 0.001%
    referrer_address: str = "0x1c83bb5a464277bDCa5d8fB9c354Aae642D18914"

    def to_json(self):
        """Convert the swap parameters to JSON."""
        return {
            "src": self.src,
            "dst": self.dst,
            "amount": self.amount,
            "slippage": self.slippage,
            "from": self.from_,
            "disableEstimate": self.disable_estimate,
            "allowPartialFill": self.allow_partial_fill,
            "fee": self.fee,
            "referrerAddress": self.referrer_address,
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


class OneInchSwapApi:
    """This class is used to swap tokens using the 1inch API."""

    api: EthereumApi
    crypto: EthereumCrypto
    chain_id: int
    api_key: str
    logger: Any

    def __init__(
        self,
        api: EthereumApi,
        account: EthereumCrypto,
        chain_id: int,
        api_key: str,
        logger,
    ):
        self.api = api
        self.account = account
        self.chain_id = chain_id
        self.api_key = api_key
        self.logger = logger
        self.logger.warning("JUHU connected to 1inch API")

    def api_request_url(
        self,
        method_name,
        query_params,
    ):
        """Build the API request URL."""
        self.logger("Building API request URL for method: %s with params: %s", method_name, query_params)
        return (
            f"https://api.1inch.dev/swap/v6.0/{self.chain_id}{method_name}?"
            + f"{'&'.join([f'{key}={value}' for key, value in query_params.items()])}"
        )

    def sign_swap_txn(self, swap_transaction):
        """Sign the swap transaction."""
        self.logger.info(f"Signing swap transaction: {swap_transaction}")
        return signed_tx_to_dict(self.account.entity.sign_transaction(swap_transaction))

    async def build_tx_for_swap(self, swap_params, retries=5, cooldown=1):
        """Build the transaction for the swap."""
        self.logger.info(f"Building transaction for swap: {swap_params}")
        url = self.api_request_url("/swap", swap_params.to_json())
        try:
            response = await httpx.get(url, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=5)  # noqa
            swap_transaction = response.json()
        except httpx.DecodingError:
            if "The limit of requests per second has been exceeded" in response.text:
                self.logger.exception(
                    f"Rate limit exceeded for 1inch API remaining: {retries} cooldown: {cooldown}",
                )
                if retries == 0:
                    raise
                await asyncio.sleep(cooldown)
                return await self.build_tx_for_swap(swap_params, retries - 1, cooldown * 2)
        if "error" in swap_transaction:
            if "Not enough" in swap_transaction["description"]:
                raise InsufficientBalance(swap_transaction["description"])
            if "insufficient liquidity" in swap_transaction["description"]:
                if retries == 0:
                    raise InvalidSwapParams(swap_transaction["description"])
                await asyncio.sleep(cooldown)
                self.logger.exception(
                    f"Rate limit exceeded for 1inch API remaining: {retries} cooldown: {cooldown}",
                )
                return await self.build_tx_for_swap(swap_params, retries - 1, cooldown * 2)
            raise InvalidSwapParams(swap_transaction["description"])
        return swap_transaction["tx"]

    async def swap_tokens(self, swap_params, retries=5, nonce=None):
        """Swap tokens using the 1inch API."""
        self.logger.info(f"Starting Swap: {swap_params}")
        swap_transaction = await self.build_tx_for_swap(swap_params)
        swap_transaction["from"] = self.account.address
        swap_transaction["to"] = Web3.to_checksum_address(swap_transaction["to"])
        swap_transaction["value"] = int(swap_transaction["value"])
        swap_transaction["gasPrice"] = int(int(swap_transaction["gasPrice"]) * 1.05)
        swap_transaction["chainId"] = self.chain_id
        cur_nonce = self.api._try_get_transaction_count(self.account.address, raise_on_try=True)  # noqa
        if nonce and nonce != cur_nonce:
            self.logger.error(f"Nonce mismatch: {nonce} != {cur_nonce}")
            return False, None
        swap_transaction["nonce"] = cur_nonce
        self.logger.info(f"Signing transaction: {swap_transaction}")
        signed_txn = self.sign_swap_txn(swap_transaction)
        self.logger.info(f"Signed transaction: {signed_txn}")
        txn_hash = try_send_signed_transaction(self.api, signed_txn, raise_on_try=True)
        self.logger.info(f"Transaction hash: {txn_hash}")
        result = False

        try:
            result = self.api.api.eth.wait_for_transaction_receipt(txn_hash, timeout=60, poll_latency=1)
        except TimeExhausted:
            self.logger.exception(f"Transaction timed out: {txn_hash}")
            retries -= 1
            if retries == 0:
                return False, txn_hash
            await asyncio.sleep(2)
            return await self.swap_tokens(swap_params, retries=retries, nonce=cur_nonce)

        if not result:
            return False, txn_hash
        if result.get("status") == 0:
            return False, txn_hash
        return True, txn_hash

    async def get_quote(self, swap_params, retries=10, cooldown=2):
        """Get a quote for the swap."""
        try:
            url = self.api_request_url("/quote", swap_params.to_json())
            response = await httpx.get(url, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=5)  # noqa
            quote = response.json()
            self.logger(f"Got quote: {quote}")
        except httpx.DecodingError:
            self.logger.exception(
                f"Rate limit exceeded for 1inch API remaining: {retries} cooldown: {cooldown}",
            )
            if retries == 0:
                raise
            await asyncio.sleep(cooldown)
            return await self.get_quote(swap_params, retries - 1, cooldown * 2)
        if "error" in quote:
            self.logger.exception(
                f"Rate limit exceeded for 1inch API remaining: {retries} cooldown: {cooldown}",
            )
            if retries == 0:
                raise InvalidSwapParams(quote["description"])
            await asyncio.sleep(cooldown)
            return await self.get_quote(swap_params, retries - 1, cooldown * 2)
        return quote

    async def close(self):
        """Close the connection."""
        self.logger("Closing connection to 1inch API")


class OneInchApiClient(BaseErc20Exchange):
    """Class for interacting with the 1inch API."""

    def parse_order(self, api_call: dict[str, Any], exchange_id) -> Order:
        """Create an order from an api call."""
        order = api_call
        order.exchange_id = exchange_id
        self.logger.warning(f"Parsed order: {order}")
        return order

    async def fetch_open_orders(self, address: str) -> dict[str, Any]:
        """Fetch the open orders for the given address."""

    async def fetch_positions(self, *arg, **kwargs) -> dict[str, Any]:
        """Fetch the positions for the given address."""

    async def fetch_tickers(self, *args, **kwargs) -> dict[str, Any]:
        """Fetch the tickers."""

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

        # look up the token addresses by key.
        input_token = self.get_token_by_name(asset_a)
        output_token = self.get_token_by_name(asset_b)

        if not input_token or not output_token:
            msg = f"Invalid token symbol provided: {asset_a} or {asset_b}"
            raise ValueError(msg)
        symbol = f"{input_token.symbol}/{output_token.symbol}"

        # We now calculate the price of the token.
        params["is_sell"] = True
        bid_price, amount = await self.get_price(input_token, output_token, **params)
        params["amount"] = amount
        inverse_ask_p, amount = await self.get_price(output_token, input_token, **params)

        ask_price = 1 / inverse_ask_p

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

    async def create_order(
        self,
        side: OrderSide,
        asset_a: str,
        asset_b: str,
        amount: Decimal,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        """Create an order."""
        del args
        side = OrderSide.BUY if side == "buy" else OrderSide.SELL
        if side == OrderSide.BUY:
            src = asset_b
            dst = asset_a

        else:
            src = asset_a
            dst = asset_b

        input_token = self.get_token(src)
        output_token = self.get_token(dst)

        if side == OrderSide.BUY:
            _amount = int((amount * 10**input_token.decimals) * kwargs.get("price"))
        else:
            _amount = int(amount * 10**output_token.decimals)

        swap_params = OneInchSwapParams(
            src=src,
            dst=dst,
            amount=str(_amount),
            from_=self.account.address,
            disable_estimate=False,
            allow_partial_fill=False,
            slippage=str(1),
        )

        res, txn_hash = await self.one_inch_api.swap_tokens(swap_params)

        return Order(
            id=txn_hash,
            symbol=f"{input_token.symbol}/{output_token.symbol}",
            side=side,
            asset_a=asset_a,
            asset_b=asset_b,
            amount=amount,
            price=kwargs.get("price"),
            status=OrderStatus.FILLED if res else OrderStatus.FAILED,
            type=OrderType.MARKET,
            timestamp=datetime.now(tz=datetime.timetz().tzinfo).timestamp(),
        )

    @cache  # noqa
    def get_token_by_name(self, name):
        """Get the token by name."""
        address = self.names_to_addresses.get(name)
        if address:
            return self.get_token(address)
        return None

    def __init__(self, ledger_id, rpc_url, key_path, logger, *args, **kwargs):
        self.one_inch_api = OneInchSwapApi(
            EthereumApi(
                address=rpc_url,
            ),
            EthereumCrypto(key_path),
            LEDGER_TO_CHAIN_ID[SupportedLedgers(ledger_id)],
            kwargs.get("api_key"),
            logger=logger,
        )
        super().__init__(ledger_id, rpc_url, key_path, logger, *args, **kwargs)

    async def get_price(
        self,
        input_token,
        output_token,
        amount,
    ):
        """Get the price of the token."""
        amount = int(amount * 10**input_token.decimals)
        swap_params = OneInchSwapParams(
            src=input_token.address,
            dst=output_token.address,
            amount=str(amount),
            from_=self.account.address,
            disable_estimate=False,
            allow_partial_fill=False,
            slippage=str(1),
        )
        quote = await self.one_inch_api.get_quote(swap_params)
        out_amt = int(quote["dstAmount"])
        in_amt_human = amount / 10**input_token.decimals
        out_amt_human = out_amt / 10**output_token.decimals
        ratio = in_amt_human / out_amt_human
        return 1 / ratio, out_amt_human


def get_erc_details(contract, api, address, crypto):
    """Get the ERC details."""
    decimals = contract.decimals(api, address)["int"]
    balance = contract.balance_of(api, address, crypto.address)["int"]
    symbol = contract.symbol(api, address)["str"]
    return decimals, balance, symbol


def get_allowance(
    contract,
    api,
    src,
    owner,
    spender,
):
    """Get the allowance."""
    return contract.allowance(api, src, owner, spender)["int"]


def increase_allowance(
    token_address: Address,
    spender: Address,
    amount: int,
    ledger_api: EthereumApi,
    crypto: EthereumCrypto,
) -> None:
    """Increase the allowance."""
    erc20_contract: Erc20 = load_contract(PublicId.from_str("eightballer/erc_20:0.1.0"))
    func = erc20_contract.approve(
        ledger_api=ledger_api,
        contract_address=token_address,
        to=spender,
        value=int(amount * 1e6),  # infinite allowance
    )
    txn = func.build_transaction(
        {
            "from": crypto.address,
            "nonce": ledger_api.api.eth.get_transaction_count(crypto.address),
            "gas": 100000,
            "gasPrice": ledger_api.api.eth.gas_price,
        }
    )

    return sign_and_send_txn(txn, crypto, ledger_api)


def sign_and_send_txn(txn, crypto, ledger_api):
    """Sign and send transaction."""

    def _sign_swap_txn(swap_transaction):
        """Sign the swap transaction."""
        return signed_tx_to_dict(crypto.entity.sign_transaction(swap_transaction))

    signed_txn = _sign_swap_txn(txn)
    txn_hash = try_send_signed_transaction(ledger_api, signed_txn)
    result = False
    with contextlib.suppress(Exception):
        result = ledger_api.api.eth.wait_for_transaction_receipt(txn_hash, timeout=600)
    if result.get("status") == 0:
        return False, txn_hash
    return True, txn_hash


def perform_swap(
    one_inch_api: OneInchSwapApi,
    swap_params: OneInchSwapParams,
    amount: int,
    spent_erc_20_decimals: int,
    bought_erc_20_decimals: int,
):
    """Perform the swap."""

    price_quote = asyncio.run(
        one_inch_api.get_quote(swap_params, retries=0),
    )
    in_amt_human = amount / 10**spent_erc_20_decimals
    out_amt_human = int(price_quote["dstAmount"]) / 10**bought_erc_20_decimals

    ratio = in_amt_human / out_amt_human
    1 / ratio

    if input("Proceed with swap? (y/n): ").lower() != "y":
        sys.exit(0)

    result, _txn = asyncio.run(one_inch_api.swap_tokens(swap_params))

    if result:
        pass
    else:
        pass


@click.command()
@click.option("--chain_id", type=int, help="Chain ID for chain to swap on", default=1)
@click.option("--api_key", type=str, help="API key for 1inch API", default=None)
@click.option(
    "--src",
    type=str,
    help="Source token address: (usdc)",
    default="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
)
@click.option(
    "--dst",
    type=str,
    help="Destination token address: (lbtc)",
    default="0x8236a87084f8b84306f72007f36f2618a5634494",
)
@click.option("--amount", type=int, help="Amount of tokens to swap", default="10000000")
def main(chain_id, src, dst, amount, api_key):  # noqa
    """Swap tokens using the 1inch API.

    Args:
    ----
        chain_id (int): Chain ID for chain to swap on.
        api_key (str): API key for 1inch API.

    """

    api = EthereumApi(
        address="https://eth.drpc.org",
        chain_id=str(chain_id),
    )
    crypto = EthereumCrypto(
        private_key_path="ethereum_private_key.txt",
    )

    swap_params = OneInchSwapParams(
        src=src,
        dst=dst,
        amount=amount,
        from_=crypto.address,
        slippage=1,
        disable_estimate=False,
        allow_partial_fill=False,
    )

    logger = logging.getLogger(__name__)

    # We make sure to log to the console

    logger.setLevel("INFO")
    logger.addHandler(logging.StreamHandler())
    erc_20 = load_contract(PublicId.from_str("eightballer/erc_20:0.1.0"))
    one_inch_api_key = os.getenv("ONE_INCH_API_KEY")
    if not one_inch_api_key:
        msg = "ONE_INCH_API_KEY environment variable not set"
        raise UserWarning(msg)

    one_inch_api = OneInchSwapApi(api, crypto, chain_id, api_key=one_inch_api_key, logger=logger)

    spent_erc_20_decimals, spent_erc_20_balance, spent_erc_20_symbol = get_erc_details(erc_20, api, src, crypto)
    bought_erc_20_decimals, _bought_erc_20_balance, bought_erc_20_symbol = get_erc_details(erc_20, api, dst, crypto)

    if spent_erc_20_balance < amount:
        msg = "Insufficient balance in source token"
        raise InsufficientBalance(msg)

    ledger_id = {
        1: SupportedLedgers.ETHEREUM,
        100: SupportedLedgers.GNOSIS,
        8453: SupportedLedgers.BASE,
    }[chain_id]
    allowance = get_allowance(erc_20, api, src, crypto.address, SPENDER[ledger_id.value])
    if allowance < amount:
        result = increase_allowance(
            token_address=src,
            spender=SPENDER[str(chain_id)],
            amount=amount,
            ledger_api=api,
            crypto=crypto,
        )
        if not result:
            msg = "Failed to increase allowance"
            raise InsufficientAllowance(msg)

    click.echo(f"Performing swap of {amount} {src} for {dst}")
    click.echo(f"Spent:  {spent_erc_20_symbol}  : {amount / 10**spent_erc_20_decimals}")
    click.echo(f"Bought: {bought_erc_20_symbol} : {amount / 10**bought_erc_20_decimals}")

    perform_swap(one_inch_api, swap_params, amount, spent_erc_20_decimals, bought_erc_20_decimals)


if __name__ == "__main__":
    main()
