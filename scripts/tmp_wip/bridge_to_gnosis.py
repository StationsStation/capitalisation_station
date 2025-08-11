"""
Simple script to test whether can deposit and withdraw from the drv platform.
"""

from pathlib import Path
import sys
from aea_ledger_ethereum import EthereumApi, Address, EthereumCrypto
from dataclasses import asdict, dataclass

from web3 import Web3
from deposit_to_drv import load_contract
from rich import print
from deposit_to_drv import sign_and_send_txn, check_allowance, increase_allowance

from packages.eightballer.contracts.omni_bridge.contract import OmniBridge as OmniBridgeContract

contract: OmniBridgeContract = load_contract(
    Path("packages/eightballer/contracts/omni_bridge")
)

@dataclass
class DepositData():
    token: Address
    receiver: Address
    value: int


olas_address = "0x0001A500A6B18995B03f44bb040A5fFc28E45CB0"


ledger_api = EthereumApi(
    address="https://eth.drpc.org",
    chain_id=str(1),
)

crypto = EthereumCrypto(
    private_key_path="ethereum_private_key.txt",
)

transfer_data = DepositData(
    token=olas_address,
    receiver=crypto.address,
    value=int(1* 1e18),
)

contract_address = Web3.to_checksum_address("0x88ad09518695c6c3712ac10a214be5109a655671")
func = contract.relay_tokens_1(
    ledger_api=ledger_api,
    contract_address=contract_address,
    **asdict(transfer_data)
)

if not check_allowance(
    token_address=transfer_data.token,
    owner=crypto.address,
    spender=contract_address,
    amount=transfer_data.value,
    ledger_api=ledger_api
):
    print("Increasing allowance")
    result = increase_allowance(
        token_address=transfer_data.token,
        spender=contract_address,
        amount=transfer_data.value,
        ledger_api=ledger_api,
        crypto=crypto
    )
    if not result:
        raise ValueError("Failed to increase allowance")

txn = func.build_transaction({
    "from": crypto.address,
    "nonce": ledger_api.api.eth.get_transaction_count(crypto.address),
    "gas": 500_000,
    "gasPrice": ledger_api.api.eth.gas_price * 1.05,
    "value": 0}
)

print(txn)


if input("Do you want to send this transaction? (y/n): ") == "y":
    if sign_and_send_txn(txn, crypto, ledger_api):
        print("Token deposited successfully!")
    else:
        print("Failed to execute transaction!")
        sys.exit(1)





