"""
Script to transfer funds from main account to subaccount
"""


import os
from aea_ledger_ethereum import EthereumCrypto
from derive_client.derive import DeriveClient
from derive_client.enums import CollateralAsset, Environment


def main():
    """
    Demonstrate canceling all orders on the derive client.
    """


    crypto = EthereumCrypto(
        private_key_path="ethereum_private_key.txt",
    )

    client = DeriveClient(
        wallet=os.environ["DERIVE_WALLET"],
        private_key=crypto.entity.key, 
        env=Environment.PROD
    )
    order = client.cancel_all()
    client.transfer_collateral(
        amount=0.001,
        to=int(os.environ["DERIVE_SUBACCOUNT_ID"]),
        asset=CollateralAsset.WEETH
    )
    print(order)


if __name__ == "__main__":
    main()


