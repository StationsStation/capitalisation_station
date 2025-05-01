import requests

from derive_client.data_types import ChainID, Currency
from derive_client.clients.async_client import AsyncClient

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeStatus
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
                chain_id=target_chain_id,
                currency=currency,
                amount=amount,
                receiver=receiver,
            )
        else:
            receiver = client.wallet
            client.deposit_to_derive(
                chain_id=source_chain_id,
                currency=currency,
                amount=amount,
                receiver=receiver,
            )

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
