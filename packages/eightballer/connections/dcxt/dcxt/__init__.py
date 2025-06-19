"""Imports supported decentralised exchanges."""

from packages.eightballer.connections.dcxt.dcxt import exceptions as base_exceptions
from packages.eightballer.connections.dcxt.dcxt.nabla import NablaFinanceClient

# pylint: disable=C0103
from packages.eightballer.connections.dcxt.dcxt.derive import DeriveClient
from packages.eightballer.connections.dcxt.dcxt.cowswap import CowSwapClient
from packages.eightballer.connections.dcxt.dcxt.balancer import BalancerClient
from packages.eightballer.connections.dcxt.dcxt.one_inch import OneInchApiClient


derive = DeriveClient
balancer = BalancerClient
one_inch = OneInchApiClient
nabla = NablaFinanceClient

cowswap = CowSwapClient

exceptions = base_exceptions
