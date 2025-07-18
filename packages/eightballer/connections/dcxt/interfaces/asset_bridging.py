"""Interface for asset_bridging protocol."""

import asyncio
from typing import TYPE_CHECKING
from functools import partial

from pydantic import BaseModel, ConfigDict
from derive_client.data_types import ChainID, Currency, TxStatus, BridgeTxResult, DeriveTxResult, DeriveTxStatus, TxResult, BridgeType

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

DERIVE_TX_FINAL_STATES = {
    DeriveTxStatus.SETTLED,
    DeriveTxStatus.REVERTED,
    DeriveTxStatus.IGNORED,
    DeriveTxStatus.TIMED_OUT,
}


class ExtraInfo(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra="allow")
    derive_status: str = ""
    transaction_id: str = ""
    derive_tx_hash: str = ""
    bridge_type: str = ""


def bridge_result_to_bridge_tx_result(
    result: BridgeResult,
) -> BridgeTxResult:
    """Reconstruct a BridgeTxResult from a prior BridgeResult."""

    req = result.request
    info = ExtraInfo(**result.extra_info)

    return BridgeTxResult(
        currency=Currency[req.source_token],
        bridge=BridgeType[info.bridge_type.upper()],
        source_chain=ChainID[req.source_ledger_id.upper()],
        target_chain=ChainID[req.target_ledger_id.upper()],
        source_tx=TxResult(tx_hash=result.source_tx_hash),
        target_tx=TxResult(tx_hash=result.target_tx_hash) if result.target_tx_hash else None,
        target_from_block=result.target_from_block,
    )



class AssetBridgingInterface(BaseInterface):
    """Interface for the asset bridging protocol."""

    protocol_id = AssetBridgingMessage.protocol_id
    dialogue_class = AssetBridgingDialogue
    dialogues_class = BaseAssetBridgingDialogues

    # def verify_request(self, message, reply_err):

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
            info = ExtraInfo(
                derive_status=derive_tx_result.status.value,
                transaction_id=derive_tx_result.transaction_id,
                derive_tx_hash=derive_tx_result.tx_hash or "",
                **{k: str(v) for k, v in derive_tx_result.error_log.items()},
            )

            if derive_tx_result.status is not DeriveTxStatus.SETTLED:
                status = DERIVE_TX_TO_BRIDGE_STATUS[derive_tx_result.status]
                result = BridgeResult(
                    request=request,
                    status=status,
                    extra_info=info.model_dump(),
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

                info.brige = bridge_tx_result.bridge.name
                result = BridgeResult(
                    request=request,
                    source_tx_hash=bridge_tx_result.source_tx.tx_hash,
                    target_tx_hash=None,
                    target_from_block=bridge_tx_result.target_from_block,
                    status=status,
                    extra_info=info.model_dump(),
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

            info = ExtraInfo(bridge_type=bridge_tx_result.bridge.name)
            result = BridgeResult(
                request=request,
                source_tx_hash=bridge_tx_result.source_tx.tx_hash,
                target_tx_hash=None,
                target_from_block=bridge_tx_result.target_from_block,
                status=status,
                extra_info=info.model_dump(),
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
        connection,
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

        if result.status is not BridgeResult.Status.STATUS_PENDING:
            return reply_err(
                code=ErrorCode.ALREADY_FINALIZED,
                err_msg="",
            )

        amount = request.amount
        currency = Currency[request.source_token]
        source_chain = ChainID[request.source_ledger_id.upper()]
        target_chain = ChainID[request.target_ledger_id.upper()]

        ledger_id = exchange_id = request.bridge
        exchange: DeriveClient = connection.exchanges[ledger_id][exchange_id]
        client: AsyncClient = exchange.client

        info = ExtraInfo(**result.extra_info)

        if request.source_ledger_id == "derive":
            # 1. DeriveTxResult not finalized
            if not info.derive_tx_hash:
                derive_tx_result: DeriveTxResult = client.get_transaction(info.transaction_id)
                info = ExtraInfo(
                    derive_status=derive_tx_result.status.value,
                    transaction_id=derive_tx_result.transaction_id,
                    derive_tx_hash=derive_tx_result.tx_hash or "",
                    **{k: str(v) for k, v in derive_tx_result.error_log.items()},
                )
                if derive_tx_result.status is not DeriveTxStatus.SETTLED:
                    status = DERIVE_TX_TO_BRIDGE_STATUS[derive_tx_result.status]
                    result = BridgeResult(
                        request=request,
                        status=status,
                        extra_info=info.model_dump(),
                    )
                    return dialogue.reply(
                        performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
                        target_message=message,
                        result=result
                    )
                else:  # we still need to start the bridge
                    connection.logger.info(
                        f"Withdrawing {amount} {request.source_token} to {client.signer.address} on {target_chain.name}."
                    )
                    bridge_tx_result: BridgeTxResult = client.withdraw_from_derive(
                        chain_id=target_chain,
                        currency=currency,
                        amount=amount,
                    )
                    bridge_tx_result = await asyncio.to_thread(client.poll_bridge_progress(bridge_tx_result))

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
                    info.brige = bridge_tx_result.bridge.name
                    result = BridgeResult(
                        request=request,
                        source_tx_hash=bridge_tx_result.source_tx.tx_hash,
                        target_tx_hash=None,
                        target_from_block=bridge_tx_result.target_from_block,
                        status=status,
                        extra_info=info.model_dump(),
                    )
            # 2. BridgeTxResult not finalized
            else:
                # re-hydrate the "in‐flight" BridgeTxResult
                bridge_tx_result = bridge_result_to_bridge_tx_result(result)
                bridge_tx_result = await asyncio.to_thread(client.poll_bridge_progress(bridge_tx_result))
        else:
            # re-hydrate the "in‐flight" BridgeTxResult
            bridge_tx_result = bridge_result_to_bridge_tx_result(result)

            # 3. BridgeTxResult not finalized
            if not bridge_tx_result.target_tx:
                connection.logger.info(
                    f"Depositing {amount} {request.source_token} to Derive wallet {client.wallet} on {source_chain.name}."
                )
                bridge_tx_result = await asyncio.to_thread(client.poll_bridge_progress(bridge_tx_result))

            # 4. DeriveTxResult not finalized
            if bridge_tx_result.status == TxStatus.SUCCESS:
                connection.logger.info(f"Transferring {amount} {request.source_token} to subaccount.")
                derive_tx_result: DeriveTxResult = client.transfer_from_funding_to_subaccount(
                    amount=amount,
                    asset_name=request.source_token,
                    subaccount_id=client.subaccount_id,
                )
                info = ExtraInfo(
                    derive_status=derive_tx_result.status.value,
                    transaction_id=derive_tx_result.transaction_id,
                    derive_tx_hash=derive_tx_result.tx_hash or "",
                    **{k: str(v) for k, v in derive_tx_result.error_log.items()},
                )
                status = DERIVE_TX_TO_BRIDGE_STATUS[derive_tx_result.status]
                result.status = status
                result.extra_info = info.model_dump()

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
