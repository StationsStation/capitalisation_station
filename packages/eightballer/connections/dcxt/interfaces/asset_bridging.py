"""Interface for asset_bridging protocol."""

from __future__ import annotations

import json
import time
import asyncio
from typing import TYPE_CHECKING
from functools import partial

from pydantic import BaseModel, ConfigDict
from derive_client.config import (
    LYRA_OFT_WITHDRAW_WRAPPER,
    LYRA_OFT_WITHDRAW_WRAPPER_ABI_PATH,
    LayerZeroChainIDv2,
)
from derive_client._bridge.w3 import get_contract, get_erc20_contract, wait_for_tx_finality  # noqa: PLC2701
from derive_client.data_types import (
    D,
    ChainID,
    Currency,
    TxStatus,
    BridgeTxResult,
    PreparedBridgeTx,
)
from derive_client.config.networks import DeriveTokenAddress
from derive_client.utils.prod_addresses import get_prod_derive_addresses
from derive_client.data_types.generated_models import (
    TxStatus as DeriveTxStatus,
    PrivateDepositResultSchema,
    PrivateWithdrawResultSchema,
    PublicGetTransactionResultSchema,
)

from packages.zarathustra.protocols.asset_bridging.message import (
    AssetBridgingMessage,
)
from packages.zarathustra.protocols.asset_bridging.dialogues import (
    AssetBridgingDialogue,
    BaseAssetBridgingDialogues,
)
from packages.zarathustra.protocols.asset_bridging.custom_types import (
    BridgeResult,
    BridgeRequest,
)
from packages.eightballer.connections.dcxt.interfaces.interface_base import (
    BaseInterface,
)


if TYPE_CHECKING:
    from decimal import Decimal
    from logging import Logger

    from derive_client import AsyncHTTPClient

    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient


# ruff: noqa: PLR0914  # Too many local variables
# ruff: noqa: PLR0911  # Too many return statements
# ruff: noqa: SLF001   # Private member accessed

# Minimum 300 for signature expiry, a little extra for buffer
DERIVE_TX_SETTLEMENT_TIMEOUT_SEC = 310
DERIVE_TX_POLL_INTERVAL = 10

BRIDGE_DEPOSIT = "Depositing %(amount)s %(token)s from %(eoa)s on %(chain)s to funding wallet %(wallet)s on DERIVE."
BRIDGE_WITHDRAWAL = "Withdrawing %(amount)s %(token)s from %(wallet)s on DERIVE to funding wallet %(eoa)s on %(chain)s."

TRANSFER_TO_FUNDING = "Transferring %(amount)s %(token)s from subaccount %(subaccount)s to funding wallet %(wallet)s."
TRANSFER_TO_SUBACC = "Transferring %(amount)s %(token)s from funding wallet %(wallet)s to subaccount %(subaccount)s."


ErrorCode = AssetBridgingMessage.ErrorInfo.Code

DERIVE_PROD_ADDRESSES = get_prod_derive_addresses()


class BridgeFailed(Exception):
    """Raised when a bridge transaction fails or does not reach SUCCESS."""


class DeriveTransferFailed(Exception):
    """Raised when transfer to subaccount/funding does not settle."""


class ExtraInfo(BaseModel):
    """ExtraInfo."""

    model_config = ConfigDict(validate_assignment=True, extra="allow")
    derive_status: str = ""
    transaction_id: str = ""
    derive_tx_hash: str = ""
    bridge_type: str = ""


async def get_lightaccount_currency_balance(
    client,
    currency: Currency,
    target_chain: ChainID | None = None,
) -> Decimal:
    """Get LightAccount Currency Balance."""

    source_chain = ChainID.DERIVE
    derive_w3 = client.bridge._derive_bridge.derive_w3
    if currency == Currency.DRV:
        token_address = DeriveTokenAddress.DERIVE.value
    else:
        token_address = DERIVE_PROD_ADDRESSES.chains[source_chain][currency].MintableToken

    contract = get_erc20_contract(w3=derive_w3, token_address=token_address)
    balance = await contract.functions.balanceOf(client._auth.wallet).call()

    if currency == Currency.DRV:
        # pay in LZ tokens (DRV).
        # Actual final amount will be less than balance, due to fee deduction
        token_fee = await get_drv_fee_in_token(
            client,
            amount=balance,
            token_address=token_address,
            target_chain=target_chain,
        )
    else:
        # pay in native token (ETH) for gas
        token_fee = 0

    balance -= token_fee

    decimals = await contract.functions.decimals().call()
    amount = balance / (10**decimals)

    return D(amount)


async def get_drv_fee_in_token(
    client,
    amount: int,
    token_address: str,
    target_chain: ChainID,
) -> int:
    """Get LayerZero fee in token. Used bridging DRV from Derive to external."""

    derive_w3 = client.bridge._derive_bridge.derive_w3
    abi = json.loads(LYRA_OFT_WITHDRAW_WRAPPER_ABI_PATH.read_text())
    withdraw_wrapper = get_contract(w3=derive_w3, address=LYRA_OFT_WITHDRAW_WRAPPER, abi=abi)
    destEID = LayerZeroChainIDv2[target_chain.name]  # noqa: N806

    return await withdraw_wrapper.functions.getFeeInToken(
        token=token_address,
        amount=amount,
        destEID=destEID,
    ).call()


async def wait_for_settlement(
    client: AsyncHTTPClient,
    result: PrivateDepositResultSchema | PrivateWithdrawResultSchema,
    timeout_sec: int = DERIVE_TX_SETTLEMENT_TIMEOUT_SEC,
    poll_interval_sec: float = DERIVE_TX_POLL_INTERVAL,
) -> PublicGetTransactionResultSchema:
    """Wait for transaction settlement on Derive chain.

    Args:
    ----
        client: Derive async HTTP client
        result: Initial deposit/withdraw result with transaction_id
        timeout_sec: Maximum time to wait for settlement
        poll_interval_sec: Time between status checks

    Returns:
    -------
        Final transaction result

    Raises:
    ------
        TimeoutError: If transaction doesn't reach final state within timeout
        RuntimeError: If transaction reaches error state (reverted/ignored/timed_out)

    """

    start_time = time.monotonic()

    while True:
        tx_result = await client.transactions.get(transaction_id=result.transaction_id)

        # Success case
        if tx_result.status == DeriveTxStatus.settled:
            return tx_result

        # Error cases
        if tx_result.status in {DeriveTxStatus.reverted, DeriveTxStatus.ignored, DeriveTxStatus.timed_out}:
            msg = f"Transaction failed with status {tx_result.status}: {tx_result.error_log}"
            raise RuntimeError(msg)

        # Still processing (requested/pending) - check timeout
        if time.monotonic() - start_time > timeout_sec:
            msg = f"Transaction {result.transaction_id} did not settle within {timeout_sec}s"
            raise TimeoutError(msg)

        await asyncio.sleep(poll_interval_sec)


async def _deposit_to_derive(request: BridgeRequest, client: AsyncHTTPClient, logger):
    amount = D(request.amount)
    currency = Currency[request.source_token]
    source_chain = ChainID[request.source_ledger_id.upper()]
    ChainID[request.target_ledger_id.upper()]

    kwargs = {
        "amount": amount,
        "token": currency.name,
        "eoa": client._auth.account.address,
        "chain": source_chain.name,
        "wallet": client._auth.wallet,
    }
    logger.info(BRIDGE_DEPOSIT, kwargs)

    # 1. Prepare bridge transaction
    prepared_tx: PreparedBridgeTx = await client.bridge.prepare_deposit_tx(
        amount=amount,
        currency=currency,
        chain_id=source_chain,
    )

    # 2. Submit bridge transaction
    bridge_tx_result: BridgeTxResult = await client.bridge.submit_tx(prepared_tx=prepared_tx)

    # 3. Poll bridge transaction result
    bridge_tx_result = await client.bridge.poll_tx_progress(tx_result=bridge_tx_result)

    # If we didn't raise above, TxStatus is considered final and FAILED
    if bridge_tx_result.status is not TxStatus.SUCCESS:
        msg = f"Bridge did not succeed: {bridge_tx_result}"
        raise BridgeFailed(msg)

    # 4. Transfer from funding account to subaccount
    # We always try to move the entire available amount for the currency
    amount = await get_lightaccount_currency_balance(client=client, currency=currency)
    kwargs = {
        "amount": amount,
        "token": currency.name,
        "wallet": client._auth.wallet,
        "subaccount": client._subaccount_id,
    }
    logger.info(TRANSFER_TO_SUBACC, kwargs)

    signature_expiry_sec = int(time.time()) + DERIVE_TX_SETTLEMENT_TIMEOUT_SEC

    deposit_result: PrivateDepositResultSchema = await client.collateral.deposit_to_subaccount(
        amount=amount,
        asset_name=request.source_token,
        signature_expiry_sec=signature_expiry_sec,
    )

    # Wait for settlement
    derive_tx_result: PublicGetTransactionResultSchema = await wait_for_settlement(client=client, result=deposit_result)

    if derive_tx_result.status is not DeriveTxStatus.settled:
        msg = f"Funding -> subaccount transfer failed: {deposit_result}"
        logger.error(msg)
        raise DeriveTransferFailed(msg)

    # Wait for finality
    w3 = client.bridge._derive_bridge.w3s[source_chain]
    tx_receipt = await wait_for_tx_finality(
        w3=w3,
        tx_hash=derive_tx_result.transaction_hash,
        logger=logger,
        poll_interval=DERIVE_TX_POLL_INTERVAL,
    )
    if tx_receipt.status != TxStatus.SUCCESS:
        msg = f"Derive deposit_to_subaccount failed waiting for finality: {tx_receipt}"
        raise DeriveTransferFailed(msg)

    return create_bridge_result(
        request=request,
        bridge_tx_result=bridge_tx_result,
        derive_tx_result=derive_tx_result,
        transaction_id=deposit_result.transaction_id,
    )


async def _withdraw_from_derive(request: BridgeRequest, client: AsyncHTTPClient, logger: Logger):
    amount = D(request.amount)
    currency = Currency[request.source_token]
    target_chain = ChainID[request.target_ledger_id.upper()]

    kwargs = {
        "amount": amount,
        "token": currency.name,
        "subaccount": client._subaccount_id,
        "wallet": client._auth.wallet,
    }
    logger.info(TRANSFER_TO_FUNDING, kwargs)

    # 1. Transfer from subaccount to funding account
    signature_expiry_sec = int(time.time()) + DERIVE_TX_SETTLEMENT_TIMEOUT_SEC
    withdraw_result: PrivateWithdrawResultSchema = await client.collateral.withdraw_from_subaccount(
        amount=amount,
        asset_name=request.source_token,
        signature_expiry_sec=signature_expiry_sec,
    )

    logger.info(f"Withdraw result: {withdraw_result}")

    # Wait for settlement
    derive_tx_result: PublicGetTransactionResultSchema = await wait_for_settlement(
        client=client, result=withdraw_result
    )

    if derive_tx_result.status is not DeriveTxStatus.settled:
        msg = f"Subaccount -> funding transfer failed: {derive_tx_result}"
        logger.error(msg)
        raise DeriveTransferFailed(msg)

    logger.info("Subaccount -> funding transfer settled.")

    # Wait for finality
    derive_w3 = client.bridge._derive_bridge.derive_w3
    tx_receipt = await wait_for_tx_finality(
        w3=derive_w3,
        tx_hash=derive_tx_result.transaction_hash,
        logger=logger,
        poll_interval=DERIVE_TX_POLL_INTERVAL,
    )
    if tx_receipt.status != TxStatus.SUCCESS:
        msg = f"Derive withdraw_from_subaccount failed waiting for finality: {tx_receipt}"
        raise DeriveTransferFailed(msg)

    kwargs = {
        "amount": amount,
        "token": currency.name,
        "wallet": client._auth.wallet,
        "eoa": client._auth.account.address,
        "chain": target_chain.name,
    }
    logger.info(BRIDGE_WITHDRAWAL, kwargs)

    # 2. Prepare bridge transaction
    # We always try to move the entire available amount for the currency
    # NOTE: we subtract LZ token fee in case of DRV
    amount = await get_lightaccount_currency_balance(client=client, currency=currency, target_chain=target_chain)

    prepared_tx: PreparedBridgeTx = await client.bridge.prepare_withdrawal_tx(
        amount=amount,
        currency=currency,
        chain_id=target_chain,
    )

    # 3. Submit bridge transaction
    bridge_tx_result: BridgeTxResult = await client.bridge.submit_tx(prepared_tx=prepared_tx)

    # 3. Poll bridge transaction result
    bridge_tx_result = await client.bridge.poll_tx_progress(tx_result=bridge_tx_result)

    # If we didn't raise above, TxStatus is considered final and FAILED
    if bridge_tx_result.status is not TxStatus.SUCCESS:
        msg = f"Bridge did not succeed: {bridge_tx_result}"
        raise BridgeFailed(msg)

    return create_bridge_result(
        request=request,
        bridge_tx_result=bridge_tx_result,
        derive_tx_result=derive_tx_result,
        transaction_id=withdraw_result.transaction_id,
    )


def create_bridge_result(
    request: BridgeRequest,
    bridge_tx_result: BridgeTxResult,
    derive_tx_result: PublicGetTransactionResultSchema,
    transaction_id: str,
) -> BridgeResult:
    """Convert BridgeTxResult + DeriveTxResult into BridgeResult."""

    info = ExtraInfo(
        derive_status=derive_tx_result.status,
        transaction_id=transaction_id,
        derive_tx_hash=derive_tx_result.transaction_hash,
        **{k: str(v) for k, v in derive_tx_result.error_log.items()},
    )

    info.bridge_type = bridge_tx_result.bridge_type.name

    match bridge_tx_result.status:
        case TxStatus.SUCCESS:
            status = BridgeResult.Status.STATUS_SUCCESS
        case TxStatus.FAILED:
            status = BridgeResult.Status.STATUS_FAILED
        case TxStatus.PENDING:  # should not be possible
            status = BridgeResult.Status.STATUS_PENDING

    return BridgeResult(
        request=request,
        source_tx_hash=bridge_tx_result.source_tx.tx_hash,
        target_tx_hash=bridge_tx_result.target_tx.tx_hash if bridge_tx_result.target_tx else None,
        target_from_block=bridge_tx_result.target_from_block,
        status=status,
        extra_info=info.model_dump(),
    )


class AssetBridgingInterface(BaseInterface):
    """Interface for the asset bridging protocol."""

    protocol_id = AssetBridgingMessage.protocol_id
    dialogue_class = AssetBridgingDialogue
    dialogues_class = BaseAssetBridgingDialogues

    async def request_bridge(
        self, message: AssetBridgingMessage, dialogue: AssetBridgingDialogue, connection
    ) -> AssetBridgingMessage | None:
        """Handle incoming asset bridge request."""

        reply_err = partial(self._error_reply, dialogue=dialogue, target_message=message)

        if message.performative != AssetBridgingMessage.Performative.REQUEST_BRIDGE:
            return reply_err(
                code=ErrorCode.CODE_INVALID_PERFORMATIVE,
                err_msg="Expecting REQUEST_BRIDGE performative",
            )

        request: BridgeRequest = message.request

        if request.bridge != ChainID.DERIVE.name.lower():
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=f"Bridge '{request.bridge}' not supported",
            )
        if "derive" not in {request.source_ledger_id, request.target_ledger_id}:
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=f"Can only bridge FROM or TO Derive at this time: {request}",
            )
        if request.target_token and request.target_token != request.source_token:
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=f"Socket superbridge requires source_token == target_token, got {request}",
            )

        ledger_id = exchange_id = request.bridge
        exchange: DeriveClient = connection.exchanges[ledger_id][exchange_id]
        client: AsyncHTTPClient = exchange.client

        await client.connect()

        if request.receiver is not None:
            err_msg = (
                "Providing a custom receiver isn't supported for the Derive.\n"
                "We automatically use:\n"
                f"  • Your EOA ({client._auth.account.address}) when withdrawing FROM Derive.\n"
                f"  • The Derive contract wallet ({client._auth.wallet}) when depositing TO Derive."
            )
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=err_msg,
            )

        is_deposit = request.target_ledger_id == "derive"

        try:
            if is_deposit:
                result: BridgeResult = await _deposit_to_derive(request, client, connection.logger)
            else:
                result: BridgeResult = await _withdraw_from_derive(request, client, connection.logger)
        except Exception as e:  # noqa: BLE001
            err_msg = f"Error during {'deposit' if is_deposit else 'withdrawal'}: {type(e).__name__}: {e}"
            return reply_err(
                code=ErrorCode.CODE_OTHER_EXCEPTION,
                err_msg=err_msg,
            )

        return dialogue.reply(
            performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
            target_message=message,
            result=result,
        )

    async def request_status(
        self,
        _message: AssetBridgingMessage,
        _dialogue: AssetBridgingDialogue,
        _connection,
    ) -> AssetBridgingMessage | None:
        """Handle incoming asset bridge status update request."""

        msg = (
            "request_status is not supported anymore: bridging always completes or fails "
            "within request_bridge. No incremental status polling is implemented."
        )
        raise NotImplementedError(msg)

    def _error_reply(
        self,
        dialogue: AssetBridgingDialogue,
        target_message: AssetBridgingMessage,
        code: ErrorCode,
        err_msg: str,
    ) -> AssetBridgingMessage:
        return dialogue.reply(
            performative=AssetBridgingMessage.Performative.ERROR,
            target_message=target_message,
            info=AssetBridgingMessage.ErrorInfo(
                code=code,
                message=err_msg,
            ),
        )
