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
    # SupportedLedgers.ETHEREUM: "http://eth.chains.wtf:8545",
    SupportedLedgers.BASE: "https://rpc.ankr.com/base",
    SupportedLedgers.OPTIMISM: "https://rpc.ankr.com/optimism",
    SupportedLedgers.GNOSIS: "https://rpc.ankr.com/gnosis",
    SupportedLedgers.POLYGON_POS: "https://rpc.ankr.com/polygon",
    SupportedLedgers.ARBITRUM: "https://rpc.ankr.com/arbitrum",
}

WORMHOLE_CHAIN_ID_MAPPING = {
    SupportedLedgers.ETHEREUM: 2,
    SupportedLedgers.BASE: 30,
    SupportedLedgers.OPTIMISM: 24,
    SupportedLedgers.POLYGON_POS: 5,
    SupportedLedgers.ARBITRUM: 23,
}

WORMHOLE_TOKEN_RELAYER_MAPPING = {
    SupportedLedgers.ETHEREUM: "0x3ee18B2214AFF97000D974cf647E7C347E8fa585",
    SupportedLedgers.BASE: "0x8d2de8d2f73F1F4cAB472AC9A881C9b123C79627",
    SupportedLedgers.OPTIMISM: "0x1D68124e65faFC907325e3EDbF8c4d84499DAa8b",
    SupportedLedgers.POLYGON_POS: "0x5a58505a96D1dbf8dF91cB21B54419FC36e93fdE",
    SupportedLedgers.ARBITRUM: "0x0b2402144Bb366A632D14B83F244D2e0e21bD39c",
}

token_receiver_mapping = dict()



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

async def transfer_tokens(lp_token, sender_address, receiver_address, ledger):
    """Transfer LP tokens from L2 to ETH mainnet."""
    # ABI: function transferTokens(address token, uint256 amount, uint16 recipientChain, bytes32 recipient, uint256 arbiterFee, uint32 nonce) external payable returns (uint64 sequence);
    # https://github.com/wormhole-foundation/wormhole/blob/e717f538721739d9f6fc690e16bc7ef7cfd3ee4c/ethereum/contracts/bridge/interfaces/ITokenBridge.sol#L77C5-L77C30

    # Get LP balance
    amount = lp_token.balance_of(sender_address)
    # Approve if needed
    lp_token.approve(WORMHOLE_TOKEN_RELAYER_MAPPING[ledger], amount)
    # Wormhole transfers only 8 decimals
    if amount > 10^10:
        tx = contract_or_abi(WORMHOLE_TOKEN_RELAYER_MAPPING[ledger]).functions.transfer_tokens(
            token: lp_token,
            amount,
            recipient_chain: WORMHOLE_CHAIN_ID_MAPPING[SupportedLedgers.ETHEREUM]
            recipient: "0x" + "0".repeat(24) + address_without_0x(receiver_address),
            arbiter_fee: 0,
            nonce: whatever
        ).send(sender_address)

        # Sequence is in the LogMessagePublished event, see example: https://optimistic.etherscan.io/tx/0x6d4b46eca09db3e1c3016ba042730134dae7bebbb633ad511ee00706243bd0d5#eventlog
        sequence = tx.hash.events[4].sequence

        # Form an API string and append it to token transfers dict according to the receiver address
        if not found token_receiver_mapping[receiver_address]:
            token_receiver_mapping[receiver_address] = list()
        token_receiver_mapping[receiver_address].append(url({https://api.wormholescan.io/v1/signed_vaa/${WORMHOLE_CHAIN_ID_MAPPING[ledger]}/${sender_address}/${sequence}))


async def complete_any_pending_transfer(receiver_address):
    """Completes transfer of any LP tokens received from L2."""

    # Needs to be called once in a while, since the average transfer takes 15-30 mins

    # ABI: function completeTransfer(bytes memory encodedVm) external;
    # https://github.com/wormhole-foundation/wormhole/blob/e717f538721739d9f6fc690e16bc7ef7cfd3ee4c/ethereum/contracts/bridge/interfaces/ITokenBridge.sol#L89

    # Traverse dict and pull any formed VAAs
    items = token_receiver_mapping[receiver_address]
    for item in items:
        if receiver_address is NOT in item:
            continue

        # example: https://api.wormholescan.io/v1/signed_vaa/5/00000000000000000000000027428dd2d3dd32a4d7f7c497eaaa23130d894911/247208
        response = fetch(item)
        if response not None:
            # Get Base64 VAA data
            vaa_bytes_base64 = response["vaaBytes"]
            # Get Hex VAA bytes
            vaa_bytes_hex = hexlify(vaa_bytes_base64)
            # Complete token transfer
            tx = contract_or_abi(WORMHOLE_TOKEN_RELAYER_MAPPING[SupportedLedgers.ETHEREUM]).complete_transfer(
                encoded_vm: vaa_bytes_hex
            ).send(receiver_address)


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
