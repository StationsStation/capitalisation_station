"""Interface for asset_bridging protocol."""

from typing import TYPE_CHECKING
from functools import partial

from derive_client.utils import get_w3_connection, wait_for_tx_receipt
from derive_client.data_types import ChainID, Currency, TxStatus, BridgeTxResult, DeriveTxResult, DeriveTxStatus

from packages.zarathustra.protocols.asset_bridging.message import (
    ErrorInfo,
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
    from derive_client.clients.async_client import AsyncClient

    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient


ErrorCode = ErrorInfo.CODE


DERIVE_TX_TO_BRIDGE_STATUS: dict[DeriveTxStatus, BridgeResult.Status] = {
    DeriveTxStatus.REQUESTED: BridgeResult.Status.STATUS_PENDING,
    DeriveTxStatus.PENDING: BridgeResult.Status.STATUS_PENDING,
    DeriveTxStatus.SETTLED: BridgeResult.Status.STATUS_SUCCESS,
    DeriveTxStatus.REVERTED: BridgeResult.Status.STATUS_FAILED,
    DeriveTxStatus.IGNORED: BridgeResult.Status.STATUS_ERROR,
    DeriveTxStatus.TIMED_OUT: BridgeResult.Status.STATUS_ERROR,
}


class AssetBridgingInterface(BaseInterface):
    """Interface for the asset bridging protocol."""

    protocol_id = AssetBridgingMessage.protocol_id
    dialogue_class = AssetBridgingDialogue
    dialogues_class = BaseAssetBridgingDialogues

    async def request_bridge(  # noqa: PLR0911
        self, message: AssetBridgingMessage, dialogue: AssetBridgingDialogue, connection
    ) -> AssetBridgingMessage | None:
        """Handle incoming asset bridge request."""

        reply_err = partial(self._error_reply, dialogue=dialogue, target_message=message)

        if message.performative != AssetBridgingMessage.Performative.REQUEST_BRIDGE:
            return reply_err(
                code=ErrorCode.Code.CODE_INVALID_PERFORMATIVE,
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

        amount = request.amount
        currency = Currency[request.source_token]
        source_chain = ChainID[request.source_ledger_id.upper()]
        target_chain = ChainID[request.target_ledger_id.upper()]

        if request.source_ledger_id == "derive":  # withdraw
            connection.logger.info(f"Transferring {amount} {request.source_token} from subaccount to funding account.")
            derive_tx_result: DeriveTxResult = client.transfer_from_subaccount_to_funding(
                amount=amount,
                asset_name=request.source_token,
                subaccount_id=client.subaccount_id,
            )

            if derive_tx_result.status is not DeriveTxStatus.SETTLED:
                extra_info = {
                    "derive_status": derive_tx_result.status.value,
                    "transaction_id": derive_tx_result.transaction_id,
                    "derive_tx_hash": derive_tx_result.tx_hash or "",
                    **{k: str(v) for k, v in derive_tx_result.error_log.items()},
                }
                status = DERIVE_TX_TO_BRIDGE_STATUS[derive_tx_result.status]
                result = BridgeResult(
                    request=request,
                    status=status,
                    extra_info=extra_info,
                )
            else:
                connection.logger.info(
                    f"Withdrawing {amount} {request.source_token} to {client.signer.address} on {target_chain.name}."
                )
                bridge_tx_result: BridgeTxResult = client.withdraw_from_derive(
                    chain_id=target_chain,
                    currency=currency,
                    amount=amount,
                )
                # bridge_tx_result = client.poll_bridge_progress(bridge_tx_result)

                match bridge_tx_result.status:
                    case TxStatus.FAILED:
                        status = BridgeResult.Status.STATUS_FAILED
                    case TxStatus.SUCCESS:
                        status = BridgeResult.Status.STATUS_SUCCESS
                    case TxStatus.PENDING:
                        status = BridgeResult.Status.STATUS_PENDING
                    case TxStatus.ERROR:
                        return reply_err(
                            code=ErrorCode.CODE_OTHER_EXCEPTION,
                            err_msg=f"{bridge_tx_result}",
                        )

                extra_info = {"bridge_type": bridge_tx_result.bridge.name}
                result = BridgeResult(
                    request=request,
                    source_tx_hash=bridge_tx_result.source_tx.tx_hash,
                    target_tx_hash=None,
                    target_from_block=bridge_tx_result.target_from_block,
                    status=status,
                    extra_info=extra_info,
                )

        else:
            connection.logger.info(
                f"Depositing {amount} {request.source_token} to Derive wallet {client.wallet} on {source_chain.name}."
            )
            bridge_tx_result: BridgeTxResult = client.deposit_to_derive(
                chain_id=source_chain,
                currency=currency,
                amount=amount,
            )
            # bridge_tx_result = client.poll_bridge_progress(bridge_tx_result)

            match bridge_tx_result.status:
                case TxStatus.FAILED:
                    status = BridgeResult.Status.STATUS_FAILED
                case TxStatus.SUCCESS:
                    status = BridgeResult.Status.STATUS_SUCCESS
                case TxStatus.PENDING:
                    status = BridgeResult.Status.STATUS_PENDING
                case TxStatus.ERROR:
                    return reply_err(
                        code=ErrorCode.CODE_OTHER_EXCEPTION,
                        err_msg=f"{bridge_tx_result}",
                    )

            extra_info = {"bridge_type": bridge_tx_result.bridge.name}
            result = BridgeResult(
                request=request,
                source_tx_hash=bridge_tx_result.source_tx.tx_hash,
                target_tx_hash=None,
                target_from_block=bridge_tx_result.target_from_block,
                status=status,
                extra_info=extra_info,
            )

            # if bridge_tx_result.status == TxStatus.SUCCESS:

            #     connection.logger.info(f"Transferring {amount} {request.source_token} to subaccount.")
            #     derive_tx_result: DeriveTxResult = client.transfer_from_funding_to_subaccount(
            #         amount=amount,
            #         asset_name=request.source_token,
            #         subaccount_id=client.subaccount_id,
            #     )

            #     if derive_tx_result.status is not DeriveTxStatus.SETTLED:
            #         extra_info = {
            #             "derive_status": derive_tx_result.status.value,
            #             "transaction_id": derive_tx_result.transaction_id,
            #             "derive_tx_hash": derive_tx_result.tx_hash or "",
            #             **{k: str(v) for k, v in derive_tx_result.error_log.items()},
            #         }
            #         result.status = BridgeResult.Status.STATUS_ERROR
            #         result.extra_info = extra_info

        return dialogue.reply(
            performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
            target_message=message,
            result=result,
        )

    async def request_status(
        self,
        message: AssetBridgingMessage,
        dialogue: AssetBridgingDialogue,
    ) -> AssetBridgingMessage | None:
        """Handle incoming asset bridge status update request."""

        reply_err = partial(self._error_reply, dialogue=dialogue, target_message=message)

        if message.performative != AssetBridgingMessage.Performative.REQUEST_STATUS:
            return reply_err(
                code=ErrorCode.INVALID_PERFORMATIVE,
                err_msg="Expecting REQUEST_STATUS performative",
            )

        result: BridgeResult = message.result
        request: BridgeRequest = result.request

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

        source_chain_id = ChainID[request.source_chain.upper()]

        try:
            w3 = get_w3_connection(chain_id=source_chain_id)
            tx_receipt = wait_for_tx_receipt(w3=w3, tx_hash=result.tx_hash)
        except ConnectionError:
            return reply_err(
                code=ErrorCode.CONNECTION_ERROR,
                err_msg=f"Failed to connect to {source_chain_id}",
            )
        except TimeoutError:
            return dialogue.reply(
                performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
                target_message=message,
                result=result,
            )

        match tx_receipt.status:  # ∈ {0, 1} (EIP-658)
            case TxStatus.SUCCESS:
                status = BridgeResult.COMPLETED
            case _:
                status = BridgeResult.FAILED

        result.status = status
        return dialogue.reply(
            performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
            target_message=message,
            result=result,
        )

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
