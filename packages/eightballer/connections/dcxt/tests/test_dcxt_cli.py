"""This module contains tests for the DCXT cli module."""


from packages.eightballer.connections.dcxt.cli import RPC_MAPPING
from packages.eightballer.connections.dcxt.dcxt.balancer import SupportedLedgers


def test_rpc_support():
    unsupported  = set(SupportedLedgers).difference(RPC_MAPPING)
    assert not unsupported, "Missing ledger support in RPC_MAPPING"
