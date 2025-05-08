from functools import partial

from derive_client.utils import get_w3_connection, wait_for_tx_receipt
from derive_client.data_types import ChainID, Currency, TxResult, TxStatus
from derive_client.clients.async_client import AsyncClient

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeRequest, BridgeResult
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogues
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


ErrorCode = AssetBridgingMessage.ErrorInfo.Code


class AssetBridgingInterface(BaseInterface):
    """Interface for the asset bridging protocol."""

    protocol_id = AssetBridgingMessage.protocol_id
    dialogue_class = AssetBridgingDialogue
    dialogues_class = BaseAssetBridgingDialogues

    async def request_bridge(
            self, message: AssetBridgingMessage, dialogue: AssetBridgingDialogue, connection
        ) -> AssetBridgingMessage | None:

        reply_err = partial(self._error_reply, dialogue=dialogue, target_message=message)
        if not message.performative == AssetBridgingMessage.Performative.REQUEST_BRIDGE:
            return reply_err(
                code=ErrorCode.CODE_INVALID_PERFORMATIVE,
                err_msg="Expecting REQUEST_BRIDGE performative",
            )

        request: BridgeRequest = message.request

        if not request.bridge == "derive":
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=f"Bridge '{request.bridge}' not supported",
            )
        if not (request.source_chain == ChainID.DERIVE.name or request.target_chain == ChainID.DERIVE.name):
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

        if request.receiver is not None:
            err_msg = (
                "Providing a custom receiver isn't supported for the Derive superbridge.\n"
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
        source_chain_id = ChainID[request.source_chain.upper()]
        target_chain_id = ChainID[request.target_chain.upper()]

        if request.source_chain == ChainID.DERIVE.name:
            receiver = client.signer.address
            tx_result = client.withdraw_from_derive(
                chain_id=target_chain_id,
                currency=currency,
                amount=amount,
                receiver=receiver,
            )
        else:
            receiver = client.wallet
            tx_result = client.deposit_to_derive(
                chain_id=source_chain_id,
                currency=currency,
                amount=amount,
                receiver=receiver,
            )

        match tx_result.status:
            case TxStatus.FAILED:
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_FAILED
            case TxStatus.SUCCESS:
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_COMPLETED
            case TxStatus.PENDING:
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_PENDING_TX_RECEIPT
            case TxStatus.ERROR:
                return reply_err(
                    code=ErrorCode.CODE_OTHER_EXCEPTION,
                    err_msg=f"{tx_result}",
                )

        result = BridgeResult(
            tx_hash=tx_result.tx_hash,
            status=status,
            request=request,
        )
        response_message = dialogue.reply(
            performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
            target_message=message,
            result=result,
        )
        return response_message

    async def request_status(
            self, message: AssetBridgingMessage, dialogue: AssetBridgingDialogue, connection
        ) -> AssetBridgingMessage | None:

        reply_err = partial(self._error_reply, dialogue=dialogue, target_message=message)
        if not message.performative == AssetBridgingMessage.Performative.REQUEST_STATUS:
            return reply_err(
                code=ErrorCode.CODE_INVALID_PERFORMATIVE,
                err_msg="Expecting REQUEST_STATUS performative",
            )

        result: BridgeResult = message.result
        request: BridgeRequest = result.request

        if not request.bridge == "derive":
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=f"Bridge '{request.bridge}' not supported",
            )
        if not result.status == BridgeResult.BridgeStatus.BRIDGE_STATUS_PENDING_TX_RECEIPT:
            return reply_err(
                code=ErrorCode.CODE_ALREADY_FINALIZED,
                err_msg=f"BridgeResult.status is already final",
            )

        source_chain_id = ChainID[request.source_chain.upper()]

        try:
            w3 = get_w3_connection(chain_id=source_chain_id)
            tx_receipt = wait_for_tx_receipt(w3=w3, tx_hash=result.tx_hash)
        except ConnectionError:
            return reply_err(
                code=ErrorCode.CODE_CONNECTION_ERROR,
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
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_COMPLETED
            case _:
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_FAILED

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
            )
        )
