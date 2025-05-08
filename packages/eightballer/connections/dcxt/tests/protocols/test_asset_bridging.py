"""Test the asset_bridging protocol."""

import asyncio
from typing import TYPE_CHECKING
from contextlib import ExitStack
from dataclasses import dataclass
from unittest.mock import patch

import pytest
from aea.mail.base import Envelope
from web3.datastructures import AttributeDict
from derive_client.data_types import ChainID, Currency, TxResult, Environment
from derive_client._bridge.client import BridgeClient  # noqa: PLC2701

from dcxt.tests.test_dcxt_connection import BaseDcxtConnectionTest, get_dialogues
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogues
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeResult, BridgeRequest
from packages.eightballer.connections.dcxt.tests.test_dcxt_connection import TIMEOUT


if TYPE_CHECKING:
    from derive_client.clients import AsyncClient

    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient


# ruff: noqa: D101, D103


ErrorCode = AssetBridgingMessage.ErrorInfo.Code


@dataclass
class ValidTestCase:
    name: str
    request: BridgeRequest


@dataclass
class InvalidTestCase(ValidTestCase):
    name: str
    request: BridgeRequest
    error_code: ErrorCode
    expected_error_msg: str


VALID_BRIDGE_REQUESTS = (
    ValidTestCase(
        name="DeriveClient.withdraw_from_derive",
        request=BridgeRequest(
            source_chain=ChainID.DERIVE.name,
            target_chain=ChainID.BASE.name,
            source_token=Currency.weETH.name,
            target_token=None,
            receiver=None,
            amount=0.1,
            bridge="derive",
        ),
    ),
    ValidTestCase(
        name="DeriveClient.deposit_to_derive",
        request=BridgeRequest(
            source_chain=ChainID.BASE.name,
            target_chain=ChainID.DERIVE.name,
            source_token=Currency.USDC.name,
            target_token=Currency.USDC.name,
            receiver=None,
            amount=100,
            bridge="derive",
        ),
    ),
)


def create_invalid_bridge_requests():
    valid_case = VALID_BRIDGE_REQUESTS[0]
    base = valid_case.request
    return (
        InvalidTestCase(
            name=f"{valid_case.name}: unsupported source and target chain combination",
            request=base.copy(update={"source_chain": ChainID.OPTIMISM.name}),
            error_code=ErrorCode.CODE_INVALID_PARAMETERS,
            expected_error_msg="Can only bridge FROM or TO Derive at this time",
        ),
        InvalidTestCase(
            name=f"{valid_case.name}: source token not equal to target token",
            request=base.copy(update={"target_token": Currency.LBTC.name}),
            error_code=ErrorCode.CODE_INVALID_PARAMETERS,
            expected_error_msg="Socket superbridge requires source_token == target_token",
        ),
        InvalidTestCase(
            name=f"{valid_case.name}: custom receiver provided",
            request=base.copy(update={"receiver": "0xdeadbeef"}),
            error_code=ErrorCode.CODE_INVALID_PARAMETERS,
            expected_error_msg="Providing a custom receiver isn't supported for the Derive",
        ),
    )


@pytest.mark.asyncio
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestAssetBridging(BaseDcxtConnectionTest):
    """Test asset bridging protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseAssetBridgingDialogues, AssetBridgingDialogue)

    @pytest.mark.parametrize("case", VALID_BRIDGE_REQUESTS)
    async def test_handles_valid_bridge_request(self, case: ValidTestCase) -> None:
        """Test handle valid bridge request messages."""

        request = case.request

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

    @pytest.mark.parametrize("case", create_invalid_bridge_requests())
    async def test_handles_invalid_bridge_request(self, case: InvalidTestCase) -> None:
        """Test handle invalid bridge request messages."""

        request = case.request

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

        exchanges = self.connection.protocol_interface.exchanges
        exchanges[request.bridge][request.bridge]

        await self.connection.send(envelope)
        async with asyncio.timeout(TIMEOUT):
            response = await self.connection.receive()

        assert response is not None
        assert isinstance(response.message, AssetBridgingMessage)
        assert response.message.performative == AssetBridgingMessage.Performative.ERROR, f"Error: {response}"
        assert response.message.info.code == case.error_code
        assert case.expected_error_msg in response.message.info.message
