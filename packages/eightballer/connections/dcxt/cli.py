"""
Cli tool to enable fast access to the dcxt connection.
"""

import asyncio
import contextlib
from dataclasses import asdict, dataclass
from unittest.mock import MagicMock

import pandas as pd
import rich_click as click
from rich import print
from web3 import Web3
from rich.table import Table
from rich.errors import NotRenderableError
from aea.mail.base import Envelope
from aea.identity.base import Identity
from aea.configurations.base import ConnectionConfig

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.connections.dcxt.exchange import SupportedExchanges
from packages.eightballer.protocols.tickers.message import TickersMessage
from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.eightballer.protocols.orders.dialogues import OrdersDialogue, BaseOrdersDialogues
from packages.eightballer.connections.dcxt.connection import DcxtConnection
from packages.eightballer.protocols.tickers.dialogues import TickersDialogue, BaseTickersDialogues
from packages.eightballer.protocols.balances.dialogues import BalancesDialogue, BaseBalancesDialogues
from packages.eightballer.connections.dcxt.dcxt.balancer import SupportedLedgers
from packages.eightballer.connections.dcxt.interfaces.interface_base import get_dialogues


RPC_MAPPING = {
    SupportedLedgers.ETHEREUM: "http://eth-archive.chains.wtf:8545",
    SupportedLedgers.BASE: "https://rpc.ankr.com/base",
    SupportedLedgers.OPTIMISM: "https://rpc.ankr.com/optimism",
    SupportedLedgers.GNOSIS: "https://rpc.ankr.com/gnosis",
    SupportedLedgers.POLYGON_POS: "https://rpc.ankr.com/polygon",
    SupportedLedgers.ARBITRUM: "https://rpc.ankr.com/arbitrum",
}


def rich_display_dataframe(df, title="Dataframe") -> None:
    """Display dataframe as table using rich library."""

    # ensure dataframe contains only string values
    df = df.astype(str)

    table = Table(title=title)
    for col in df.columns:
        table.add_column(col)
    for row in df.values:
        with contextlib.suppress(NotRenderableError):
            table.add_row(*row)
    print(table)


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
    balances_dialogues = get_dialogues(BaseBalancesDialogues, BalancesDialogue)
    orders_dialogues = get_dialogues(BaseOrdersDialogues, OrdersDialogue)

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
    return response.message


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

    tickers = {}
    balances = {}
    for _ledger in ledgers:
        if _ledger not in tickers:
            tickers[_ledger] = {}
        if _ledger not in balances:
            balances[_ledger] = {}
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
            tickers[_ledger][exchange_id] = {f.asset_a: f for f in response.tickers.tickers}
            envelope = create_envelope(
                cli_tool,
                cli_tool.balances_dialogues,
                BalancesMessage.Performative.GET_ALL_BALANCES,
                exchange_id=exchange_id,
                ledger_id=_ledger,
                address=Web3.to_checksum_address(account),
            )
            response: BalancesMessage = asyncio.run(send_and_await_response(cli_tool, envelope))
            balances[_ledger][exchange_id] = response.balances.balances

    all_balances = {}
    for ledger, exchange_balances in balances.items():
        if ledger not in all_balances:
            all_balances[ledger] = {}
        for exchange_id, account_balances in exchange_balances.items():
            data = [balance.dict() for balance in account_balances]
            df = pd.DataFrame(data)[["asset_id", "total"]]
            all_balances[ledger][exchange_id] = account_balances
            title = f"Balances for {exchange_id} on {ledger}"
            print()
            rich_display_dataframe(df, title=title)

    # We create a portfolio consisting of all the balances
    aggregated_portfolio = {}
    for ledger, exchange_balances in all_balances.items():
        for exchange_id, account_balances in exchange_balances.items():
            for balance in account_balances:
                if balance.asset_id not in aggregated_portfolio:
                    aggregated_portfolio[balance.asset_id] = 0
                aggregated_portfolio[balance.asset_id] += balance.total

    print()
    portfolio = pd.DataFrame(aggregated_portfolio.items(), columns=["asset_id", "total"])
    rich_display_dataframe(portfolio, title="Aggregated Portfolio")

    # We will make a table of balances, exchanges, and ledgers to create pivot tables
    # for the portfolio

    all_balances_rows = []
    for ledger, exchange_balances in all_balances.items():
        for exchange_id, account_balances in exchange_balances.items():
            for balance in account_balances:
                all_balances_rows.append(
                    {
                        "ledger": ledger,
                        "exchange": exchange_id,
                        "asset_id": balance.asset_id,
                        "total": balance.total,
                    }
                )

    print()
    all_balances = pd.DataFrame(all_balances_rows)
    asset_pivot = all_balances.pivot_table(index=["ledger"], columns="asset_id", values="total", aggfunc="sum")
    rich_display_dataframe(asset_pivot, title="Assets Pivoted by Ledger")

    # We calculate the portfolio value in USD
    # We will use the tickers to get the price of the assets
    # We will then calculate the value of the portfolio in USD
    def get_value(row):
        price = tickers[row["ledger"]][row["exchange"]][row["asset_id"]].bid
        return round(row["total"] * price, 2)

    all_balances["usd_value"] = all_balances.apply(get_value, axis=1)
    all_balances.sort_values(by="usd_value", ascending=False, inplace=True)

    rich_display_dataframe(all_balances, title="Balances with USD Value")

    # We calculate the total value of the portfolio
    total_value = all_balances["usd_value"].sum()
    print()
    print(f"Total USD value of the portfolio: ${total_value:,.2f}")


@click.command()
@click.argument("account", type=click.STRING)
@click.option("--ledger", type=click.Choice([f.value for f in SupportedLedgers] + ["all"]), default="all")
@click.option(
    "--supported-exchanges", type=click.Choice([f.value for f in SupportedExchanges] + ["all"]), default="all"
)
def fetch_trades(
    account: str,
    ledger: str,
    supported_exchanges: str,
):
    """Fetch trades."""
    if ledger == "all":
        ledgers = [f.value for f in SupportedLedgers]
    else:
        ledgers = [ledger]

    if supported_exchanges == "all":
        exchanges = [f.value for f in SupportedExchanges]

    trades = {}

    for _ledger in ledgers:
        if _ledger not in trades:
            trades[_ledger] = {}
        for exchange_id in exchanges:
            cli_tool = asyncio.run(build_cli_tool(_ledger, exchange_id))
            print(f"Connecting to {exchange_id!r} on {_ledger!r}")
            asyncio.run(cli_tool.connection.connect())
            envelope = create_envelope(
                cli_tool,
                cli_tool.orders_dialogues,
                OrdersMessage.Performative.GET_ORDERS,
                exchange_id=exchange_id,
                ledger_id=_ledger,
                account=Web3.to_checksum_address(account),
            )
            response = asyncio.run(send_and_await_response(cli_tool, envelope))
            trades[_ledger][exchange_id] = response.orders.orders

    breakpoint()


@click.group()
def main():
    """Dcxt connection cli tool."""
    pass


main.add_command(check_balances)
main.add_command(fetch_trades)

if __name__ == "__main__":
    main()  # noqa
