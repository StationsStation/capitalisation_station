import requests

from derive_client.data_types import ChainID, Currency, TxResult, Address
from derive_client.clients.async_client import AsyncClient

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeRequest, BridgeResult
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogue
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


class AssetBridgingInterface(BaseInterface):
    """Interface for the asset bridging protocol."""

    protocol_id = AssetBridgingMessage.protocol_id
    dialogue_class = AssetBridgingDialogue
    dialogues_class = BaseAssetBridgingDialogues

    async def request_bridge(
            self, message: AssetBridgingMessage, dialogue: AssetBridgingDialogue, connection
        ) -> AssetBridgingMessage | None:

        if not message.performative == AssetBridgingMessage.Performative.REQUEST_BRIDGE:
            raise RuntimeError()

        request: BridgeRequest = message.request

        if not request.bridge == "derive":
            raise NotImplementedError(f"Bridge '{request.bridge}' not supported")
        if not (request.source_chain == "derive" or request.target_chain == "derive"):
            raise NotImplementedError("Can only bridge FROM or TO derive at this time")
        if request.target_token and request.target_token != request.source_token:
            raise NotImplementedError(f"Socket superbridge requires source_token == target_token, got {request}")
        if request.receiver is not None:
            raise NotImplementedError(
                "Providing a custom receiver isn’t supported for the Derive superbridge.\n"
                "We automatically use:\n"
                f"  • Your EOA ({client.signer.address}) when withdrawing FROM Derive.\n"
                f"  • The Derive contract wallet ({client.wallet}) when depositing TO Derive."
            )

        ledger_id = exchange_id = request.bridge
        exchange: DeriveClient = connection.exchanges[ledger_id][exchange_id]
        client: AsyncClient = exchange.client

        currency = Currency[request.source_token]
        source_chain_id = ChainID[request.source_chain.upper()]
        target_chain_id = ChainID[request.target_chain.upper()]

        if request.source_chain == "derive":
            receiver = client.signer.address
            tx_result = client.withdraw_from_derive(
                chain_id=target_chain_id,
                currency=currency,
                amount=request.amount,
                receiver=request.receiver,
            )
        else:
            receiver = client.wallet
            tx_result = client.deposit_to_derive(
                chain_id=source_chain_id,
                currency=currency,
                amount=request.amount,
                receiver=request.receiver,
            )

        match tx_result.status:
            case TxStatus.FAILED:
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_FAILED
            case TxStatus.SUCCESS:
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_COMPLETED
            case TxStatus.PENDING:
                status = BridgeResult.BridgeStatus.BRIDGE_STATUS_PENDING_TX_RECEIPT
            case TxStatus.ERROR:
                response_message = dialogue.reply(
                    performative=AssetBridgingMessage.Performative.ERROR,
                    target_message=message,
                    message=f"{tx_result}",
                    code=AssetBridgingMessage.ErrorCode.ERROR_CODE_ENUM_OTHER_EXCEPTION,
                )
                return response_message

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
        if not message.performative == AssetBridgingMessage.Performative.REQUEST_STATUS:
            raise RuntimeError()

        result: BridgeResult = message.result
        request: BridgeRequest = result.request
        if not request.bridge == "derive":
            raise NotImplementedError(f"Bridge '{request.bridge}' not supported")
        if not result.status == BridgeResult.BridgeStatus.BRIDGE_STATUS_PENDING_TX_RECEIPT:
            # TODO: log: All other status values are final
            return

        # TODO: poll for receipt or check logs for TokensBridged event
        # Protocol is atomic; we currently don't have context of original bridge request
        # This orignal bridge request provide the context necessary to check for status
