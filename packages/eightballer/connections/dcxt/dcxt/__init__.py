"""
Imports supported decentralised exchanges.
"""
from packages.eightballer.connections.dcxt.dcxt.balancer import BalancerClient

# pylint: disable=C0103
from packages.eightballer.connections.dcxt.dcxt.hundred_x import HundredXClient
from packages.eightballer.connections.dcxt.dcxt.lyra_v2 import LyraClient

lyra = LyraClient
hundred_x = HundredXClient
balancer = BalancerClient
