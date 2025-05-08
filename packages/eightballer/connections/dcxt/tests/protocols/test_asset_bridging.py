import asyncio
from typing import TYPE_CHECKING
from contextlib import ExitStack
from unittest.mock import patch

import pytest
from aea.mail.base import Envelope
from web3.datastructures import AttributeDict
from derive_client.data_types import ChainID, Currency, TxResult, Environment
from derive_client._bridge.client import BridgeClient

from dcxt.tests.test_dcxt_connection import BaseDcxtConnectionTest, get_dialogues
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogues
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeResult, BridgeRequest
from packages.eightballer.connections.dcxt.tests.test_dcxt_connection import TIMEOUT


if TYPE_CHECKING:
    from derive_client.clients import AsyncClient

    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient


VALID_BRIDGE_REQUESTS = (
    BridgeRequest(
        source_chain=ChainID.DERIVE.name,
        target_chain=ChainID.BASE.name,
        source_token=Currency.weETH.name,
        amount=0.1,
        bridge="derive",
    ),
    BridgeRequest(
        source_chain=ChainID.BASE.name,
        target_chain=ChainID.DERIVE.name,
        source_token=Currency.USDC.name,
        amount=100,
        bridge="derive",
    ),
)


@pytest.mark.asyncio
class TestAssetBridging(BaseDcxtConnectionTest):
    """Test asset bridging protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseAssetBridgingDialogues, AssetBridgingDialogue)

    @pytest.mark.parametrize("bridge_request", VALID_BRIDGE_REQUESTS)
    async def test_handles_valid_bridge_request(self, bridge_request: BridgeRequest) -> None:
        """Test handle valid bridge request messages."""

        request = bridge_request

        await self.connection.connect()
        dialogues = self.DIALOGUES(self.client_skill_id)  # pylint: disable=E1120

        message, _ = dialogues.create(
            counterparty=str(self.connection.connection_id),
            performative=AssetBridgingMessage.Performative.REQUEST_BRIDGE,
            request=request,
        )
        envelope = Envelope(
            to=message.to,
            sender=message.sender,
            message=message,
        )

        tx_receipt = AttributeDict(dictionary={"status": 1})
        fake_result = TxResult(tx_hash="0xdeadbeef", tx_receipt=tx_receipt, exception=None)

        exchanges = self.connection.protocol_interface.exchanges
        exchange: DeriveClient = exchanges[request.bridge][request.bridge]
        client: AsyncClient = exchange.client

        with ExitStack() as stack:
            stack.enter_context(patch.object(client, "env", Environment.PROD))
            stack.enter_context(patch.object(BridgeClient, "withdraw_with_wrapper", return_value=fake_result))
            stack.enter_context(patch.object(BridgeClient, "deposit", return_value=fake_result))

            await self.connection.send(envelope)
            async with asyncio.timeout(TIMEOUT):
                response = await self.connection.receive()

        assert response is not None
        assert isinstance(response.message, AssetBridgingMessage)
        assert response.message.performative == AssetBridgingMessage.Performative.BRIDGE_STATUS, f"Error: {response}"
        assert response.message.result.status == BridgeResult.BridgeStatus.BRIDGE_STATUS_COMPLETED
