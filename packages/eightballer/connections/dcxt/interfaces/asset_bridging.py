<<<<<<< HEAD
"""Interface for asset_bridging protocol."""

from typing import TYPE_CHECKING
from functools import partial

from derive_client.utils import get_w3_connection, wait_for_tx_receipt
from derive_client.data_types import ChainID, Currency, TxStatus

from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogues
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeResult, BridgeRequest
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


if TYPE_CHECKING:
    from derive_client.clients.async_client import AsyncClient

    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient


ErrorCode = AssetBridgingMessage.ErrorInfo.Code


=======
import requests

from derive_client.data_types import ChainID, Currency
from derive_client.clients.async_client import AsyncClient

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeStatus
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogue
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


>>>>>>> def61c3 (feat: AssetBridgingInterface draft)
class AssetBridgingInterface(BaseInterface):
    """Interface for the asset bridging protocol."""

    protocol_id = AssetBridgingMessage.protocol_id
    dialogue_class = AssetBridgingDialogue
    dialogues_class = BaseAssetBridgingDialogues

<<<<<<< HEAD
    async def request_bridge(  # noqa: PLR0911
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

        if request.bridge != "derive":
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=f"Bridge '{request.bridge}' not supported",
            )
        if ChainID.DERIVE.name not in {request.source_chain, request.target_chain}:
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
=======
    async def request_bridge(
            self, message: AssetBridgingMessage, dialogue: AssetBridgingDialogue, connection
        ) -> AssetBridgingMessage | None:

        if not message.performative == AssetBridgingMessage.Performative.REQUEST_BRIDGE:
            raise RuntimeError()

        source_chain: str = message.source_chain
        target_chain: str = message.target_chain
        source_token: str = message.source_token
        target_token: str | None = message.target_token
        bridge: str = message.bridge
        kwargs: dict[str, str] | None = message.kwargs

        if not bridge == "derive":
            raise NotImplementedError()
        if not (source_chain == "derive" or target_chain == "derive"):
            raise NotImplementedError()
        if target_token and target_token != source_token:
            raise NotImplementedError()
        
        ledger_id = exchange_id = bridge
        exchange: DeriveClient = connection.exchanges[ledger_id][exchange_id]
        client: AsyncClient = exchange.client

        currency = Currency[source_token]
        source_chain_id = ChainID[source_chain.upper()]
        target_chain_id = ChainID[target_chain.upper()]

        amount = 1  # TODO: update protocol performative

        if source_chain == "derive":
            receiver = client.signer.address
            client.withdraw_from_derive(
>>>>>>> def61c3 (feat: AssetBridgingInterface draft)
                chain_id=target_chain_id,
                currency=currency,
                amount=amount,
                receiver=receiver,
            )
        else:
            receiver = client.wallet
<<<<<<< HEAD
            tx_result = client.deposit_to_derive(
=======
            client.deposit_to_derive(
>>>>>>> def61c3 (feat: AssetBridgingInterface draft)
                chain_id=source_chain_id,
                currency=currency,
                amount=amount,
                receiver=receiver,
            )

<<<<<<< HEAD
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
                code=ErrorCode.CODE_INVALID_PERFORMATIVE,
                err_msg="Expecting REQUEST_STATUS performative",
            )

        result: BridgeResult = message.result
        request: BridgeRequest = result.request

        if request.bridge != "derive":
            return reply_err(
                code=ErrorCode.CODE_INVALID_PARAMETERS,
                err_msg=f"Bridge '{request.bridge}' not supported",
            )
        if result.status != BridgeResult.BridgeStatus.BRIDGE_STATUS_PENDING_TX_RECEIPT:
            return reply_err(
                code=ErrorCode.CODE_ALREADY_FINALIZED,
                err_msg="BridgeResult.status is already final",
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
            ),
        )
=======
        # TODO: 
        # - obtain tx_hash (not currently returned by client)
        # - obtain / determine status
        tx_hash = b""
        status = BridgeStatus(status=BridgeStatus.BridgeStatusEnum.BRIDGE_STATUS_ENUM_COMPLETED)

        response_message = dialogue.reply(
            performative=AssetBridgingMessage.Performative.BRIDGE_STATUS,
            target_message=message,
            status=status,
            tx_hash=tx_hash,
        )
        return response_message

    async def request_status(
            self, message: AssetBridgingMessage, dialogue: AssetBridgingDialogue, connection
        ) -> AssetBridgingMessage | None:
        if not message.performative == AssetBridgingMessage.Performative.REQUEST_STATUS:
            raise

        tx_hash: bytes = message.tx_hash

        # TODO: poll for receipt or check logs for TokensBridged event
        # Protocol is atomic; we currently don't have context of original bridge request
        # This orignal bridge request provide the context necessary to check for status
>>>>>>> def61c3 (feat: AssetBridgingInterface draft)
