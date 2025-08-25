"""Interface for asset_bridging protocol."""

from typing import TYPE_CHECKING
from logging import Logger
from functools import partial

from pydantic import BaseModel, ConfigDict
from derive_client.data_types import (
    ChainID,
    Currency,
    TxStatus,
    BridgeTxResult,
    DeriveTxResult,
    DeriveTxStatus,
    PreparedBridgeTx,
)
from derive_client.clients.async_client import AsyncClient

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
    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient


# ruff: noqa: PLR0914  # Too many local variables
# ruff: noqa: PLR0911  # Too many return statements

BRIDGE_DEPOSIT = "Depositing %(amount)s %(token)s from %(eoa)s on %(chain)s to funding wallet %(wallet)s on DERIVE."
BRIDGE_WITHDRAWAL = "Withdrawing %(amount)s %(token)s from %(wallet)s on DERIVE to funding wallet %(eoa)s on %(chain)s."

TRANSFER_TO_FUNDING = "Transferring %(amount)s %(token)s from subaccount %(subaccount)s to funding wallet %(wallet)s."
TRANSFER_TO_SUBACC = "Transferring %(amount)s %(token)s from funding wallet %(wallet)s to subaccount %(subaccount)s."


ErrorCode = AssetBridgingMessage.ErrorInfo.Code


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


async def _deposit_to_derive(request: BridgeRequest, client: AsyncClient, logger):
    amount = request.amount
    currency = Currency[request.source_token]
    source_chain = ChainID[request.source_ledger_id.upper()]

    kwargs = {
        "amount": amount,
        "token": currency.name,
        "eoa": client.account.address,
        "chain": source_chain.name,
        "wallet": client.wallet,
    }
    logger.info(BRIDGE_DEPOSIT, kwargs)

    # 1. Prepare bridge transaction
    prepared_tx: PreparedBridgeTx = await client.prepare_deposit_to_derive(
        human_amount=amount, currency=currency, chain_id=source_chain
    )

    # 2. Submit bridge transaction
    bridge_tx_result: BridgeTxResult = await client.submit_bridge_tx(prepared_tx=prepared_tx)

    # 3. Poll bridge transaction result
    bridge_tx_result = await client.poll_bridge_progress(tx_result=bridge_tx_result)

    # If we didn't raise above, TxStatus is considered final and FAILED
    if bridge_tx_result.status is not TxStatus.SUCCESS:
        msg = f"Bridge did not succeed: {bridge_tx_result}"
        raise BridgeFailed(msg)

    # 4. Transfer from funding account to subaccount
    kwargs = {"amount": amount, "token": currency.name, "wallet": client.wallet, "subaccount": client.subaccount_id}
    logger.info(TRANSFER_TO_SUBACC, kwargs)
    derive_tx_result: DeriveTxResult = client.transfer_from_funding_to_subaccount(
        amount=amount,
        asset_name=request.source_token,
        subaccount_id=client.subaccount_id,
    )
    if derive_tx_result.status is not DeriveTxStatus.SETTLED:
        msg = f"Funding -> subaccount transfer failed: {derive_tx_result}"
        raise DeriveTransferFailed(msg)

    return create_bridge_result(request=request, bridge_tx_result=bridge_tx_result, derive_tx_result=derive_tx_result)


async def _withdraw_from_derive(request: BridgeRequest, client: AsyncClient, logger: Logger):
    amount = request.amount
    currency = Currency[request.source_token]
    target_chain = ChainID[request.target_ledger_id.upper()]

    kwargs = {"amount": amount, "token": currency.name, "subaccount": client.subaccount_id, "wallet": client.wallet}
    logger.info(TRANSFER_TO_FUNDING, kwargs)

    # 1. Transfer from subaccount to funding account
    derive_tx_result: DeriveTxResult = client.transfer_from_subaccount_to_funding(
        amount=amount,
        asset_name=request.source_token,
        subaccount_id=client.subaccount_id,
    )

    if derive_tx_result.status is not DeriveTxStatus.SETTLED:
        msg = f"Subaccount -> funding transfer failed: {derive_tx_result}"
        raise DeriveTransferFailed(msg)

    kwargs = {
        "amount": amount,
        "token": currency.name,
        "wallet": client.wallet,
        "eoa": client.account.address,
        "chain": target_chain.name,
    }
    logger.info(BRIDGE_WITHDRAWAL, kwargs)

    # 2. Prepare bridge transaction
    prepared_tx: PreparedBridgeTx = await client.prepare_withdrawal_from_derive(
        human_amount=amount,
        currency=currency,
        chain_id=target_chain,
    )

    # 3. Submit bridge transaction
    bridge_tx_result: BridgeTxResult = await client.submit_bridge_tx(prepared_tx=prepared_tx)

    # 3. Poll bridge transaction result
    bridge_tx_result = await client.poll_bridge_progress(tx_result=bridge_tx_result)

    # If we didn't raise above, TxStatus is considered final and FAILED
    if bridge_tx_result.status is not TxStatus.SUCCESS:
        msg = f"Bridge did not succeed: {bridge_tx_result}"
        raise BridgeFailed(msg)

    return create_bridge_result(request=request, bridge_tx_result=bridge_tx_result, derive_tx_result=derive_tx_result)


def create_bridge_result(
    request: BridgeRequest,
    bridge_tx_result: BridgeTxResult,
    derive_tx_result: DeriveTxResult,
) -> BridgeResult:
    """Convert BridgeTxResult + DeriveTxResult into BridgeResult."""

    info = ExtraInfo(
        derive_status=derive_tx_result.status.value,
        transaction_id=derive_tx_result.transaction_id,
        derive_tx_hash=derive_tx_result.tx_hash or "",
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
        client: AsyncClient = exchange.client

        await client.connect_ws()
        await client.login_client()

        if request.receiver is not None:
            err_msg = (
                "Providing a custom receiver isn't supported for the Derive.\n"
                "We automatically use:\n"
                f"  • Your EOA ({client.signer.address}) when withdrawing FROM Derive.\n"
                f"  • The Derive contract wallet ({client.wallet}) when depositing TO Derive."
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
