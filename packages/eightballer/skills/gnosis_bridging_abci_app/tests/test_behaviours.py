"""Test the metrics skill."""

from pathlib import Path
from unittest.mock import patch

import pytest
from aea.test_tools.test_skill import BaseSkillTestCase

from packages.eightballer.skills.gnosis_bridging_abci_app import PUBLIC_ID
from packages.eightballer.skills.gnosis_bridging_abci_app.strategy import GnosisL1L2DepositData, GnosisL1L2WithdrawData
from packages.eightballer.skills.gnosis_bridging_abci_app.behaviours import (
    ClaimRound,
    StartRound,
    DepositRound,
    CheckAllowanceRound,
    WaitForMessageRound,
    WaitForSignatureRound,
    IncreaseAllowanceRound,
    GnosisbridgingabciappEvents,
)


ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent

ROUNDS = [
    DepositRound,
    CheckAllowanceRound,
    IncreaseAllowanceRound,
    WaitForMessageRound,
    StartRound,
]


BRIDGE_REQUEST_1 = GnosisL1L2DepositData(
    amount=1,
    deposit_txn="0xb7b97e3319afd6fd6f0cd6eab6df13b9eccbbbdf125030885e4b8014768ba374",
    msg="0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000b5000500004ac82b41bd819dd871590b510316f2385cb196fb0000000000029a1988ad09518695c6c3712ac10a214be5109a655671f6a78083ca3e2a662d6dd1703c939c8ace2e268d001e84800101000164125e4cfb0000000000000000000000000001a500a6b18995b03f44bb040a5ffc28e45cb000000000000000000000000061030434a8535b649cfe36c5f6194f2b6e9bf24700000000000000000000000000000000000000000000000000000000000000010000000000000000000000",
    msg_id="0x000500004ac82b41bd819dd871590b510316f2385cb196fb0000000000029a19",
    msg_data="0x000500004ac82b41bd819dd871590b510316f2385cb196fb0000000000029a1988ad09518695c6c3712ac10a214be5109a655671f6a78083ca3e2a662d6dd1703c939c8ace2e268d001e84800101000164125e4cfb0000000000000000000000000001a500a6b18995b03f44bb040a5ffc28e45cb000000000000000000000000061030434a8535b649cfe36c5f6194f2b6e9bf2470000000000000000000000000000000000000000000000000000000000000001",
)

BRIDGE_REQUEST_2 = GnosisL1L2WithdrawData(
    amount=1,
    msg="0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000b500050000a7823d6f1e31569f51861e345b30c6bebf70ebe70000000000018ddef6a78083ca3e2a662d6dd1703c939c8ace2e268d88ad09518695c6c3712ac10a214be5109a655671000927c00101806401272255bb0000000000000000000000000001a500a6b18995b03f44bb040a5ffc28e45cb000000000000000000000000061030434a8535b649cfe36c5f6194f2b6e9bf24700000000000000000000000000000000000000000000000000000000000000010000000000000000000000",
    deposit_txn="0xb8a0ae7cfea98b27a60c53d4437c5b41d50a3c4c65688ae7e42d7fea05431ddf",
    claim_txn=None,
    msg_id="0x00050000a7823d6f1e31569f51861e345b30c6bebf70ebe70000000000018dde",
    msg_data="0x00050000a7823d6f1e31569f51861e345b30c6bebf70ebe70000000000018ddef6a78083ca3e2a662d6dd1703c939c8ace2e268d88ad09518695c6c3712ac10a214be5109a655671000927c00101806401272255bb0000000000000000000000000001a500a6b18995b03f44bb040a5ffc28e45cb000000000000000000000000061030434a8535b649cfe36c5f6194f2b6e9bf2470000000000000000000000000000000000000000000000000000000000000001",
    signatures="0x041b1c1c1bcf0e6ef486a78c0ffcd6ea4cd5ca681706d4a2d759e893ebb8a6dbbe5b7f9ece64b46e08bf0bf41c0f38e5ef6d9cead3169c5199f110c891c8534144edca08f062e436ed462ef9a8d1f6f871f6eac5755f775d54d060f8cbf17792084df357204c4ff8cffefed37cd796a89f1991016ef14060cc41e9f48e07e448f6a3688d1b64a901539549d803502e74d1faa548920f0cfa9c6b09ba9ccd8f48d97f0f7617018f92365121846675c3b4c976b55e318d497bd96aadefd1168e4df6bfa3f9252794826e4b12fbe4aba6ec0435c375b04f1007981d971a3f0ac85041ff8bcbaa32b91b5804ccb3e68d2aab25bc5e4ab2c7d26bcfae54f52cc5b741b516bb82df",
)


class TestDepositRound(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)
    round_class = DepositRound

    @pytest.mark.parametrize("bridge_request", [BRIDGE_REQUEST_1, BRIDGE_REQUEST_2])
    def test_act_deposit(self, bridge_request):
        """Test the act method of the round."""
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        state.strategy.current_bridge_request = bridge_request
        # we path the build_transaction and sign and send transaction methods
        with (
            patch.object(state.strategy, "build_transaction", return_value="transaction"),
            patch.object(state.strategy, "sign_and_send_txn", return_value=[True, bridge_request.deposit_txn]),
        ):
            state.act()
        assert state.is_done
        assert state.event == GnosisbridgingabciappEvents.DONE


class TestWaitForMessageRound(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)
    round_class = WaitForMessageRound

    @pytest.mark.parametrize("bridge_request", [BRIDGE_REQUEST_1, BRIDGE_REQUEST_2])
    def test_act(self, bridge_request):
        """Test the act method of the round."""
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        state.strategy.current_bridge_request = bridge_request
        state.act()
        assert state.is_done
        assert state.event == GnosisbridgingabciappEvents.DONE


class TestWaitForSignatureRound(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)
    round_class = WaitForSignatureRound

    @pytest.mark.parametrize(
        "bridge_request",
        [
            BRIDGE_REQUEST_1,
        ],
    )
    def test_act(
        self,
        bridge_request,
    ):
        """Test the act method of the round."""
        state = self.round_class(name="test", skill_context=self.skill.skill_context)

        def dummy_function(*args, **kwargs):
            del args, kwargs  # unused
            return {"events": [{"transactionHash": bridge_request.deposit_txn.encode()}]}

        state.strategy.l2_amb.get_tokens_bridged_events = dummy_function
        state.strategy.current_bridge_request = bridge_request
        state.act()
        assert state.is_done
        assert state.event == GnosisbridgingabciappEvents.DONE


class TestClaimRound(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)
    round_class = ClaimRound

    @pytest.mark.parametrize("bridge_request", [BRIDGE_REQUEST_1, BRIDGE_REQUEST_2])
    def test_act(
        self,
        bridge_request,
    ):
        """Test the act method of the round."""
        state = self.round_class(name="test", skill_context=self.skill.skill_context)
        state.strategy.current_bridge_request = bridge_request
        with (
            patch.object(state.strategy, "build_transaction", return_value="transaction"),
            patch.object(state.strategy, "sign_and_send_txn", return_value=[True, bridge_request.claim_txn]),
        ):
            state.act()
        assert state.is_done
        assert state.event == GnosisbridgingabciappEvents.DONE
