"""Test the asset_bridging protocol."""

import asyncio
from typing import TYPE_CHECKING
from contextlib import ExitStack
from dataclasses import dataclass
from unittest.mock import patch

import pytest
from aea.mail.base import Envelope
from web3.datastructures import AttributeDict
from derive_client.data_types import (
    ChainID,
    Currency,
    TxResult,
    BridgeType,
    Environment,
    BridgeTxResult,
    DeriveTxResult,
    DeriveTxStatus,
    BridgeTxDetails,
    PreparedBridgeTx,
    PSignedTransaction,
)

from dcxt.tests.test_dcxt_connection import BaseDcxtConnectionTest, get_dialogues
from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogues
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeResult, BridgeRequest
from packages.eightballer.connections.dcxt.tests.test_dcxt_connection import TIMEOUT


if TYPE_CHECKING:
    from derive_client.clients import AsyncClient

    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
    from packages.eightballer.connections.dcxt.interfaces.asset_bridging import AssetBridgingInterface


# ruff: noqa: D101, D103


ErrorCode = AssetBridgingMessage.ErrorInfo.Code


DUMMY_TX_HASH = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"


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
            request_id="withdraw_from_derive",
            source_ledger_id=ChainID.BASE.name.lower(),
            target_ledger_id=ChainID.DERIVE.name.lower(),
            source_token=Currency.USDC.name,
            amount=0.1,
            bridge="derive",
        ),
    ),
    ValidTestCase(
        name="DeriveClient.deposit_to_derive",
        request=BridgeRequest(
            request_id="deposit_to_derive",
            source_ledger_id=ChainID.BASE.name.lower(),
            target_ledger_id=ChainID.DERIVE.name.lower(),
            source_token=Currency.USDC.name,
            target_token=Currency.USDC.name,
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
class TestAssetBridging(BaseDcxtConnectionTest):
    """Test asset bridging protocol messages are handled."""

    DIALOGUES = get_dialogues(BaseAssetBridgingDialogues, AssetBridgingDialogue)

    @pytest.mark.parametrize("case", VALID_BRIDGE_REQUESTS)
    async def test_handles_valid_bridge_request(self, case: ValidTestCase) -> None:  # noqa: PLR0914
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
        fake_result = TxResult(tx_hash=DUMMY_TX_HASH, tx_receipt=tx_receipt, exception=None)

        fake_prepared_tx = PreparedBridgeTx(
            amount=0,
            value=0,
            currency=Currency.USDC,
            source_chain=ChainID.BASE,
            target_chain=ChainID.DERIVE,
            bridge_type=BridgeType.SOCKET,
            fee_value=0,
            fee_in_token=1,
            tx_details=BridgeTxDetails(
                contract="0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
                method="some_method",
                kwargs={"some_arg": "some_value"},
                signed_tx=PSignedTransaction(
                    raw_transaction="0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
                    hash="0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbe",
                    r=1,
                    s=1,
                    v=1,
                ),
                tx={},
            ),
        )
        fake_bridge_result = BridgeTxResult(
            currency=Currency.USDC,
            source_chain=ChainID[request.source_ledger_id.upper()],
            target_chain=ChainID[request.target_ledger_id.upper()],
            source_tx=fake_result,
            target_tx=fake_result,
            bridge="socket",
            target_from_block=0,
            prepared_tx=fake_prepared_tx,
        )

        fake_derive_tx = DeriveTxResult(
            transaction_hash=DUMMY_TX_HASH,
            exception=None,
            data={},
            status=DeriveTxStatus.SETTLED,
            error_log={},
            transaction_id="some_tx_id",
        )

        exchanges = self.connection.protocol_interface.exchanges
        exchange: DeriveClient = exchanges[request.bridge][request.bridge]
        client: AsyncClient = exchange.client
        interfaces = self.connection.protocol_interface.supported_protocols
        bridging_interface: AssetBridgingInterface = interfaces[AssetBridgingMessage.protocol_id]
        bridging_interface.sleep_time = 0.1

        with ExitStack() as stack:
            stack.enter_context(patch.object(client, "env", Environment.PROD))
            stack.enter_context(patch.object(client, "prepare_deposit_to_derive", return_value=fake_prepared_tx))
            stack.enter_context(patch.object(client, "submit_bridge_tx", return_value=fake_bridge_result))
            stack.enter_context(patch.object(client, "poll_bridge_progress", return_value=fake_bridge_result))
            stack.enter_context(
                patch.object(client, "transfer_from_funding_to_subaccount", return_value=fake_derive_tx)
            )
            stack.enter_context(
                patch.object(client, "transfer_from_subaccount_to_funding", return_value=fake_derive_tx)
            )

            await self.connection.send(envelope)
            async with asyncio.timeout(TIMEOUT):
                response = await self.connection.receive()

        assert response is not None
        assert isinstance(response.message, AssetBridgingMessage)
        assert response.message.performative == AssetBridgingMessage.Performative.BRIDGE_STATUS, f"Error: {response}"
        assert response.message.result.status == BridgeResult.Status.STATUS_SUCCESS, f"Error: {response}"

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
        exchange: DeriveClient = exchanges[request.bridge][request.bridge]
        client: AsyncClient = exchange.client

        tx_receipt = AttributeDict(dictionary={"status": 0})
        fake_result = TxResult(tx_hash=DUMMY_TX_HASH, tx_receipt=tx_receipt, exception=Exception("Some error"))

        with ExitStack() as stack:
            stack.enter_context(patch.object(client, "env", Environment.PROD))
            stack.enter_context(patch.object(client, "transfer_from_subaccount_to_funding", return_value=fake_result))
            stack.enter_context(patch.object(client, "transfer_from_funding_to_subaccount", return_value=fake_result))
            await self.connection.send(envelope)
            async with asyncio.timeout(TIMEOUT):
                response = await self.connection.receive()

        assert response is not None
        assert isinstance(response.message, AssetBridgingMessage)
        assert response.message.performative == AssetBridgingMessage.Performative.ERROR, f"Error: {response}"
        assert response.message.info.code == case.error_code
        assert case.expected_error_msg in response.message.info.message
