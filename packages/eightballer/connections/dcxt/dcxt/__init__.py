"""
Imports supported decentralised exchanges.
"""
from packages.eightballer.connections.dcxt.dcxt import exceptions as base_exceptions
from packages.eightballer.connections.dcxt.dcxt.balancer import BalancerClient

# pylint: disable=C0103
from packages.eightballer.connections.dcxt.dcxt.lyra_v2 import LyraClient

lyra = LyraClient
balancer = BalancerClient


exceptions = base_exceptions
