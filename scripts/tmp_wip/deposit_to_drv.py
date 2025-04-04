"""
Simple script to test whether can deposit and withdraw from the drv platform.
"""

from rich import print
import pytest
from aea_ledger_ethereum import EthereumApi, EthereumCrypto
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, cast
from aea_ledger_ethereum import Address
from packages.eightballer.contracts.lbtc.contract import Lbtc
from packages.eightballer.contracts.socket_bridge.contract import SocketBridge as SocketBridgeContract
from packages.eightballer.contracts.erc_20.contract import Erc20
from packages.eightballer.connections.dcxt.dcxt.one_inch import try_send_signed_transaction, signed_tx_to_dict
from aea_ledger_ethereum import EthereumApi
from aea.contracts.base import Contract, contract_registry
from aea_ledger_ethereum import EthereumApi, EthereumCrypto
from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration

import requests
import json

chain_id = "8453"
token_to_deposit = "weETH"
AMOUNT = int(1 * 1e18)
msg_gas_limit = 100000

reciever = "0xe768E236ED96F686F62697B7c50727BF33CfC792" # This is the derive wallet address generated on the derive chain.

TARGET_ID = "957"
TARGET_SPEED = "FAST"

def get_addresses():
    res = requests.get("https://raw.githubusercontent.com/0xdomrom/socket-plugs/refs/heads/main/deployments/superbridge/prod_lyra_addresses.json")
    data = res.json()
    with open("prod_lyra_addresses.json", "w") as f:
        json.dump(data, f, indent=4,)

    return data


@dataclass
class TokenData():
    isAppChain: bool
    NonMintableToken: Address
    Vault: Address
    LyraTSAShareHandlerDepositHook: Address
    connectors: dict[str, dict[str, str]]




def load_contract(
    CONTRACT_PATH = Path("packages/eightballer/contracts/socket_bridge")
):

    configuration = cast(
        ContractConfig,
        load_component_configuration(ComponentType.CONTRACT, CONTRACT_PATH),
    )
    configuration._directory = CONTRACT_PATH  # noqa
    if str(configuration.public_id) not in contract_registry.specs:
        # load contract into sys modules
        Contract.from_config(configuration)
    contract = contract_registry.make(str(configuration.public_id))
    return contract




def check_allowance(
    token_address: Address,
    owner: Address,
    spender: Address,
    amount: int,
    ledger_api: EthereumApi,
) -> int:
    
    erc20_contract: Lbtc = load_contract(Path("packages/eightballer/contracts/lbtc"))
    allowance = erc20_contract.allowance(
        ledger_api=ledger_api,
        contract_address=token_address,
        owner=owner,
        spender=spender,
    )['int']
    return allowance >= amount

def check_balance(
    token_address: Address,
    account: Address,
    amount: int,
    ledger_api: EthereumApi,
) -> int:

    erc20_contract: Lbtc = load_contract(Path("packages/eightballer/contracts/lbtc"))
    balance = erc20_contract.balance_of(
        ledger_api=ledger_api,
        contract_address=token_address,
        account=account,
    )['int']
    print(f"Balance: {balance}")
    print(f"Amount:  {amount}")
    print(f"Balance >= Amount: {balance >= amount}")
    return balance >= amount, balance



def increase_allowance(
    token_address: Address,
    spender: Address,
    amount: int,
    ledger_api: EthereumApi,
    crypto: EthereumCrypto,
) -> None:

    erc20_contract: Lbtc = load_contract(Path("packages/eightballer/contracts/lbtc"))
    func = erc20_contract.approve(
        ledger_api=ledger_api,
        contract_address=token_address,
        spender=spender,
        value=int(amount * 1e6), # infinite allowance
    )
    txn = func.build_transaction({
        "from": crypto.address,
        "nonce": ledger_api.api.eth.get_transaction_count(crypto.address),
        "gas": 100000,
        "gasPrice": ledger_api.api.eth.gas_price,
    })

    return sign_and_send_txn(txn, crypto, ledger_api)



def get_min_fees():
    return bridge_contract.get_min_fees(
        ledger_api=ledger_api,
        contract_address=token_data.Vault,
        payload_size_=161,
        msg_gas_limit_=msg_gas_limit,
        connector_=token_data.connectors[TARGET_ID][TARGET_SPEED],
    )['totalFees']



def build_deposit_txn(
        deposit_amount_int: int ,
) -> dict:
    """
    Build a deposit transaction to deposit token to bridge.
    """
    func = bridge_contract.bridge(
        ledger_api=ledger_api,
        contract_address=token_data.Vault,
        receiver_=reciever,
        amount_=deposit_amount_int,
        msg_gas_limit_=msg_gas_limit,
        connector_=token_data.connectors[TARGET_ID][TARGET_SPEED],
        extra_data_=b"",
        options_=b""
    )

    fees = get_min_fees()
    func.call({"from": crypto.address, "value": fees})
    txn = func.build_transaction({
        "from": crypto.address,
        "nonce": ledger_api.api.eth.get_transaction_count(crypto.address),
        "gas": 420000,
        "gasPrice": ledger_api.api.eth.gas_price,
        "value": fees + 1
    })

    return txn 


def sign_and_send_txn(txn, crypto: EthereumCrypto, ledger_api):
    """Sign and send transaction."""

    signed_txn = signed_tx_to_dict(crypto.entity.sign_transaction(txn))
    txn_hash = try_send_signed_transaction(ledger_api, signed_txn)
    print(f"Txn hash: {txn_hash}")
    result = False
    try:
        result = ledger_api.api.eth.wait_for_transaction_receipt(txn_hash, timeout=600)
    except Exception as e:
        print(e)

    if not result:
        print("Failed to execute transaction!")

    if result.get("status") == 0:
        print("Failed to execute transaction!")
        return False, txn_hash
    else:
        print("Token deposited successfully!")
        return True, txn_hash


if __name__ == "__main__":
    data = get_addresses()


    token_data = TokenData(
        **data[chain_id][token_to_deposit]
    )
    ledger_api = EthereumApi(
        address="https://base.llamarpc.com",
        chain_id=str(chain_id),
    )

    crypto = EthereumCrypto(
        private_key_path="ethereum_private_key.txt",
    )

    bridge_contract: SocketBridgeContract = load_contract()



    enouh_balance, balance = check_balance(
        token_address=token_data.NonMintableToken,
        account=crypto.address,
        amount=AMOUNT,
        ledger_api=ledger_api,
    )

    print (f"Currrent balance: {balance}")

    dep_amount = input(f"Enter amount to deposit (default: {AMOUNT}): ")
    if dep_amount:

        if not dep_amount.isdigit():
            if dep_amount == "all":
                amount = balance
            else:
                raise ValueError("Invalid amount")
        else:
            amount = int(dep_amount)
    else:
        amount = AMOUNT

    if not balance >= amount:
        raise ValueError("Insufficient balance")

    if not check_allowance(
        ledger_api=ledger_api,
        token_address=token_data.NonMintableToken,
        owner=crypto.address,
        spender=token_data.Vault,
        amount=amount,
    ):
        print("Increasing allowance")
        result = increase_allowance(
            ledger_api=ledger_api,
            token_address=token_data.NonMintableToken,
            spender=token_data.Vault,
            amount=amount,
            crypto=crypto,
        )
        if not result:
            raise ValueError("Failed to increase allowance")
        

    deposit_txn = build_deposit_txn(
        deposit_amount_int=amount,
    )

    print("Deposit txn: ")
    print(deposit_txn)

    if not input("Proceed with deposit? (y/n): ").lower() == "y":
        raise ValueError("Deposit aborted")

    if sign_and_send_txn(
        deposit_txn,
        crypto,
        ledger_api
    ):
        print("Success!")
    else:
        exit(1)
