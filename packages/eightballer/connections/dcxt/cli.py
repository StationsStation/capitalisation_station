"""
Cli tool to enable fast access to the dcxt connection.
"""

import asyncio
from dataclasses import asdict, dataclass
from unittest.mock import MagicMock

import rich_click as click
from rich import print
from aea.mail.base import Envelope
from aea.identity.base import Identity
from aea.configurations.base import ConnectionConfig

from packages.eightballer.connections.dcxt.exchange import SupportedExchanges
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.connections.dcxt.connection import DcxtConnection
from packages.eightballer.protocols.tickers.dialogues import TickersDialogue, BaseTickersDialogues
from packages.eightballer.connections.dcxt.dcxt.balancer import SupportedLedgers
from packages.eightballer.connections.dcxt.interfaces.interface_base import get_dialogues


RPC_MAPPING = {
    SupportedLedgers.ETHEREUM: "https://rpc.ankr.com/eth",
    SupportedLedgers.BASE: "https://rpc.ankr.com/base",
    SupportedLedgers.OPTIMISM: "https://rpc.ankr.com/optimism",
    SupportedLedgers.GNOSIS: "https://rpc.ankr.com/gnosis",
    SupportedLedgers.POLYGON_POS: "https://rpc.ankr.com/polygon",
    SupportedLedgers.ARBITRUM: "https://rpc.ankr.com/arbitrum",
    SupportedLedgers.MODE: "https://mainnet.mode.network",
}


@dataclass
class ExchangeConfig:
    """Exchange configuration."""

    name: str
    key_path: str
    ledger_id: str
    rpc_url: str
    etherscan_api_key: str = "TEST_API_KEY"


def get_ledger_config(ledger: str) -> str:
    """Get the ledger configuration."""

    return ExchangeConfig(
        name="balancer",
        key_path="packages/eightballer/connections/dcxt/tests/data/key",
        ledger_id=ledger,
        rpc_url=RPC_MAPPING[ledger],
    )


class DcxtCliTool:
    """Tests cli tool for dcxt connection."""

    connection: DcxtConnection
    client_skill_id: str
    agent_identity: Identity
    ticker_dialogues = get_dialogues(BaseTickersDialogues, TickersDialogue)

    def setup(self, exchange_configs: list[ExchangeConfig]) -> None:
        """Initialise the class."""
        self.client_skill_id = "eightballer/dcxt:0.1.0"
        self.agent_identity = Identity("name", address="some string", public_key="some public_key")
        configuration = ConnectionConfig(
            target_skill_id=self.client_skill_id,
            exchanges=[asdict(exchange_configs) for exchange_configs in exchange_configs],
            connection_id=DcxtConnection.connection_id,
        )
        self.connection = DcxtConnection(
            configuration=configuration,
            data_dir=MagicMock(),
            identity=self.agent_identity,
        )


async def build_cli_tool(ledger_id: SupportedLedgers, exchange_id: SupportedExchanges) -> DcxtCliTool:
    """Build the cli tool."""
    cli_tool = DcxtCliTool()
    exchange_config = ExchangeConfig(
        name=exchange_id,
        key_path="packages/eightballer/connections/dcxt/tests/data/key",
        ledger_id=ledger_id,
        rpc_url=RPC_MAPPING[SupportedLedgers(ledger_id)],
    )
    cli_tool.setup([exchange_config])
    await cli_tool.connection.connect()
    return cli_tool


def create_envelope(cli_tool: DcxtCliTool, dialogues, performative, **kwargs):
    """Create envelope."""
    request, _ = dialogues.create(
        counterparty=str(cli_tool.connection.connection_id), performative=performative, **kwargs
    )
    request._sender = "eightballer/dcxt_cli:0.1.0"  # noqa
    envelope = Envelope(
        to=request.to,
        sender=request.sender,
        message=request,
    )
    return envelope


async def send_and_await_response(cli_tool: DcxtCliTool, envelope: Envelope):
    """Send and await response."""
    await cli_tool.connection.send(envelope)
    await asyncio.sleep(1)
    response = await cli_tool.connection.receive()
    return response


@click.command()
@click.argument("account", type=click.STRING)
@click.option("--ledger", type=click.Choice([f.value for f in SupportedLedgers] + ["all"]), default="all")
@click.option(
    "--supported-exchanges", type=click.Choice([f.value for f in SupportedExchanges] + ["all"]), default="all"
)
@click.option("--portfolio-requires", type=click.Path(), default=None)
@click.option("--output", type=click.Path(), default=None)
def check_balances(account: str, ledger: str, output: str, portfolio_requires: str, supported_exchanges: str):
    """
    Check the balances of the account.
    Use the --ledger option to specify the ledger.

    Example:
    check_balances 0x1234 --ledger ethereum
    """
    print(f"Checking balances for account {account} on ledger `{ledger}`.")
    print()
    connections = []
    if ledger == "all":
        ledgers = [f.value for f in SupportedLedgers]
    else:
        ledgers = [ledger]

    if supported_exchanges == "all":
        exchanges = [f.value for f in SupportedExchanges]

    for _ledger in ledgers:
        for exchange_id in exchanges:
            cli_tool = asyncio.run(build_cli_tool(_ledger, exchange_id))
            print(f"Connecting to {exchange_id!r} on {_ledger!r}")
            asyncio.run(cli_tool.connection.connect())
            connections.append(cli_tool)

            envelope = create_envelope(
                cli_tool,
                cli_tool.ticker_dialogues,
                TickersMessage.Performative.GET_ALL_TICKERS,
                exchange_id=exchange_id,
                ledger_id=_ledger,
            )
            response = asyncio.run(send_and_await_response(cli_tool, envelope))
            print(response)
    if output:
        print(f"Writing output to {output}")
    if portfolio_requires:
        print(f"Checking portfolio requires {portfolio_requires}")


@click.group()
def main():
    """Dcxt connection cli tool."""
    pass


main.add_command(check_balances)

if __name__ == "__main__":
    main()  # noqa
