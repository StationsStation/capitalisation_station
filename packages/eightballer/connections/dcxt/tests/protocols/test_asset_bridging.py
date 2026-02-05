"""Test the asset_bridging protocol."""

import asyncio
from typing import TYPE_CHECKING
from contextlib import ExitStack
from dataclasses import dataclass
from unittest.mock import AsyncMock, patch

import pytest
from aea.mail.base import Envelope
from derive_client.data_types import (
    D,
    ChainID,
    Currency,
    TxResult,
    BridgeType,
    Environment,
    BridgeTxResult,
    TypedTxReceipt,
    BridgeTxDetails,
    PreparedBridgeTx,
    TypedSignedTransaction,
)
from derive_client.data_types.generated_models import (
    TxStatus as DeriveTxStatus,
    PrivateDepositResultSchema,
    PrivateWithdrawResultSchema,
    PublicGetTransactionResultSchema,
)
from derive_client._clients.rest.async_http.client import AsyncBridgeClient
from derive_client._clients.rest.async_http.collateral import CollateralOperations

from packages.zarathustra.protocols.asset_bridging.message import AssetBridgingMessage
from packages.zarathustra.protocols.asset_bridging.dialogues import AssetBridgingDialogue, BaseAssetBridgingDialogues
from packages.zarathustra.protocols.asset_bridging.custom_types import BridgeResult, BridgeRequest
from packages.eightballer.connections.dcxt.tests.test_dcxt_connection import (
    TIMEOUT,
    BaseDcxtConnectionTest,
    get_dialogues,
)


if TYPE_CHECKING:
    from derive_client import AsyncHTTPClient

    from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
    from packages.eightballer.connections.dcxt.interfaces.asset_bridging import AssetBridgingInterface


# ruff: noqa: D101, D103, PLC2701


ErrorCode = AssetBridgingMessage.ErrorInfo.Code

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
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

        tx_receipt = TypedTxReceipt(
            blockHash=b"",
            blockNumber=123,
            contractAddress=ZERO_ADDRESS,
            cumulativeGasUsed=1,
            effectiveGasPrice=1,
            from_=ZERO_ADDRESS,
            gasUsed=1,
            logs=[],
            logsBloom=b"",
            status=1,
            to=ZERO_ADDRESS,
            transactionHash=DUMMY_TX_HASH,
            transactionIndex=1,
            type=2,
        )
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
                fn_name="some_method",
                fn_kwargs={"some_arg": "some_value"},
                signed_tx=TypedSignedTransaction(
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

        mock_deposit_result = PrivateDepositResultSchema(
            status=DeriveTxStatus.pending,
            transaction_id="dummy-deposit-tx-id",
        )

        mock_withdraw_result = PrivateWithdrawResultSchema(
            status=DeriveTxStatus.pending,
            transaction_id="dummy-withdraw-tx-id",
        )

        fake_lightaccount_balance = D(1.0)
        fake_derive_tx = PublicGetTransactionResultSchema(
            transaction_hash=DUMMY_TX_HASH,
            data={},
            status=DeriveTxStatus.settled,
            error_log={},
        )
        fake_tx_receipt = fake_result.tx_receipt

        exchanges = self.connection.protocol_interface.exchanges
        exchange: DeriveClient = exchanges[request.bridge][request.bridge]
        client: AsyncHTTPClient = exchange.client
        interfaces = self.connection.protocol_interface.supported_protocols
        bridging_interface: AssetBridgingInterface = interfaces[AssetBridgingMessage.protocol_id]
        bridging_interface.sleep_time = 0.1

        with ExitStack() as stack:
            # Patch the environment BEFORE connect
            stack.enter_context(patch.object(client, "_env", Environment.PROD))

            # Patch the AsyncBridgeClient class methods BEFORE connect() creates an instance
            stack.enter_context(
                patch.object(
                    AsyncBridgeClient, "prepare_deposit_tx", new_callable=AsyncMock, return_value=fake_prepared_tx
                )
            )
            stack.enter_context(
                patch.object(
                    AsyncBridgeClient, "prepare_withdrawal_tx", new_callable=AsyncMock, return_value=fake_prepared_tx
                )
            )
            stack.enter_context(
                patch.object(AsyncBridgeClient, "submit_tx", new_callable=AsyncMock, return_value=fake_bridge_result)
            )
            stack.enter_context(
                patch.object(
                    AsyncBridgeClient, "poll_tx_progress", new_callable=AsyncMock, return_value=fake_bridge_result
                )
            )

            # Patch CollateralOperations class methods BEFORE connect() creates a Subaccount instance
            stack.enter_context(
                patch.object(
                    CollateralOperations,
                    "deposit_to_subaccount",
                    new_callable=AsyncMock,
                    return_value=mock_deposit_result,
                )
            )
            stack.enter_context(
                patch.object(
                    CollateralOperations,
                    "withdraw_from_subaccount",
                    new_callable=AsyncMock,
                    return_value=mock_withdraw_result,
                )
            )

            # Patch helper methods
            stack.enter_context(
                patch(
                    "packages.eightballer.connections.dcxt.interfaces.asset_bridging.get_lightaccount_currency_balance",
                    new_callable=AsyncMock,
                    return_value=fake_lightaccount_balance,
                )
            )
            stack.enter_context(
                patch(
                    "packages.eightballer.connections.dcxt.interfaces.asset_bridging.wait_for_settlement",
                    new_callable=AsyncMock,
                    return_value=fake_derive_tx,
                )
            )
            stack.enter_context(
                patch(
                    "packages.eightballer.connections.dcxt.interfaces.asset_bridging.wait_for_tx_finality",
                    new_callable=AsyncMock,
                    return_value=fake_tx_receipt,
                )
            )

            # NOW connect - the instances created will have mocked methods
            await client.connect()

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
        client: AsyncHTTPClient = exchange.client
        await client.connect()

        with ExitStack() as stack:
            stack.enter_context(patch.object(client, "_env", Environment.PROD))
            await self.connection.send(envelope)
            async with asyncio.timeout(TIMEOUT):
                response = await self.connection.receive()

        assert response is not None
        assert isinstance(response.message, AssetBridgingMessage)
        assert response.message.performative == AssetBridgingMessage.Performative.ERROR, f"Error: {response}"
        assert response.message.info.code == case.error_code
        assert case.expected_error_msg in response.message.info.message
