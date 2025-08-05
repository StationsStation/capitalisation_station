"""This module contains tests for the DCXT cli module."""

import pytest
from click.testing import CliRunner

from packages.eightballer.connections.dcxt.cli import main, RPC_MAPPING
from packages.eightballer.connections.dcxt.exchange import SupportedExchanges
from packages.eightballer.connections.dcxt.dcxt.balancer import SupportedLedgers


NULL_ADDRESS = "0x0000000000000000000000000000000000000000"

SUPPORTED = {
    SupportedLedgers.ETHEREUM: [
        SupportedExchanges.BALANCER,
        SupportedExchanges.COWSWAP,
    ],
    SupportedLedgers.BASE: [
        SupportedExchanges.BALANCER,
        SupportedExchanges.COWSWAP,
    ],
    SupportedLedgers.OPTIMISM: [
        SupportedExchanges.BALANCER,
        # SupportedExchanges.COWSWAP,  # not supported
    ],
    SupportedLedgers.POLYGON_POS: [
        SupportedExchanges.BALANCER,
        # SupportedExchanges.COWSWAP,  # new: need to bump cowdao_cowpy
    ],
    SupportedLedgers.GNOSIS: [
        SupportedExchanges.BALANCER,
        SupportedExchanges.COWSWAP,
    ],
    SupportedLedgers.ARBITRUM: [
        SupportedExchanges.BALANCER,
        SupportedExchanges.COWSWAP,
    ],
    SupportedLedgers.MODE: [
        SupportedExchanges.BALANCER,
        # SupportedExchanges.COWSWAP,  # not supported
    ],
    SupportedLedgers.DERIVE: [
        SupportedExchanges.DERIVE,
    ],
}

PARAM_LIST = list((le, ex) for le, exs in SUPPORTED.items() for ex in exs)
PARAM_IDS = [f"{ledger.name}-{exchange.name}" for ledger, exchange in PARAM_LIST]


def test_rpc_support():
    unsupported  = set(SupportedLedgers).difference(RPC_MAPPING)
    assert not unsupported, "Missing ledger support in RPC_MAPPING"


@pytest.mark.parametrize("ledger, exchange", PARAM_LIST, ids=PARAM_IDS)
def test_check_balances(ledger: SupportedLedgers, exchange: SupportedExchanges):
    runner = CliRunner()
    result = runner.invoke(main, ["check-balances", NULL_ADDRESS, "--ledger", ledger.value, "--supported-exchanges", exchange.value])
    assert result.exit_code == 0
