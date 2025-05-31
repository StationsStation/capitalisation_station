"""Imports supported decentralised exchanges."""

from packages.eightballer.connections.dcxt.dcxt import exceptions as base_exceptions

# pylint: disable=C0103
from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
from packages.eightballer.connections.dcxt.dcxt.cowswap import CowSwapClient
from packages.eightballer.connections.dcxt.dcxt.balancer import BalancerClient
from packages.eightballer.connections.dcxt.dcxt.one_inch import OneInchApiClient
from packages.eightballer.connections.dcxt.dcxt.kittypunch import KittyPunch


derive = DeriveClient
balancer = BalancerClient
one_inch = OneInchApiClient
kittypunch = KittyPunch

cowswap = CowSwapClient

exceptions = base_exceptions
