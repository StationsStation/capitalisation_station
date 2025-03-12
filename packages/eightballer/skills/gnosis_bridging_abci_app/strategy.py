"""Simple Strategy model."""

from typing import cast
from pathlib import Path
from dataclasses import dataclass

from web3 import Web3
from aea.skills.base import Model
from aea.contracts.base import Contract, contract_registry
from aea_ledger_ethereum import Address, EthereumApi, EthereumCrypto
from aea.configurations.loader import ComponentType, ContractConfig, load_component_configuration

from packages.eightballer.contracts.olas import PUBLIC_ID as OLAS_PUBLIC_ID
from packages.eightballer.contracts.erc_20 import PUBLIC_ID as ERC_20_PUBLIC_ID
from packages.eightballer.contracts.amb_gnosis import PUBLIC_ID as AMB_GNOSIS_PUBLIC_ID
from packages.eightballer.contracts.amb_mainnet import PUBLIC_ID as AMB_MAINNET_PUBLIC_ID
from packages.eightballer.contracts.omni_bridge import PUBLIC_ID as OMNI_BRIDGE_PUBLIC_ID
from packages.eightballer.contracts.amb_gnosis_helper import PUBLIC_ID as AMB_GNOSIS_HELPER_PUBLIC_ID


GAS_PREMIUM = 1.1


def load_contract(contract_path: Path) -> Contract:
    """Helper function to load a contract."""
    configuration = cast(
        ContractConfig,
        load_component_configuration(ComponentType.CONTRACT, contract_path),
    )
    configuration._directory = contract_path  # noqa
    if str(configuration.public_id) not in contract_registry.specs:
        # load contract into sys modules
        Contract.from_config(configuration)
    return contract_registry.make(str(configuration.public_id))


GNOSIS_AMB_ADDRESS_HELPER = Web3.to_checksum_address("0x7d94ece17e81355326e3359115D4B02411825EdD")
GNOSIS_OLAS_ADDRESS = "0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f"
GNOSIS_CONTRACT_ADDRESS = Web3.to_checksum_address("0x75Df5AF045d91108662D8080fD1FEFAd6aA0bb59")

MAINNET_BRIDGE_CONTRACT_ADDRESS = Web3.to_checksum_address("0x88ad09518695c6c3712ac10a214be5109a655671")
MAINNET_OLAS_ADDRESS = "0x0001A500A6B18995B03f44bb040A5fFc28E45CB0"
GNOSIS_l2_AMB = "0xf6A78083ca3e2a662D6dd1703c939c8aCE2e268d"

POA_EXECUTOR = "0x4C36d2919e407f0Cc2Ee3c993ccF8ac26d9CE64e"


@dataclass
class BaseL1L2DepositData:
    """Class to represent a base deposit data."""

    amount: int
    # amount of the token to deposit in solidity units
    from_ledger_id: str
    # the ledger id of the source chain
    from_ledger_chain_id: str
    # the chain id of the source chain
    to_ledger_id: str
    # the ledger id of the destination chain
    to_ledger_chain_id: str
    # the chain id of the destination chain
    from_bridge_address: Address
    # the bridge address on the source chain
    to_bridge_address: Address
    # the bridge address on the destination chain
    from_token_address: Address
    # the token address on the source chain
    to_token_address: Address
    # the token address on the destination chain

    deposit_txn: str = None
    claim_txn: str = None


@dataclass
class GnosisL1L2DepositData(BaseL1L2DepositData):
    """Deposit data class specific to the Gnosis bridge."""

    amount: int
    from_ledger_id: str = "ethereum"  # the ledger id of the source chain
    from_ledger_chain_id: str = "1"  # the chain id of the source chain
    to_ledger_id: str = "gnosis"  # the ledger id of the destination chain
    to_ledger_chain_id: str = "100"  # the chain id of the destination chain

    from_bridge_address: Address = MAINNET_BRIDGE_CONTRACT_ADDRESS
    to_bridge_address: Address = GNOSIS_CONTRACT_ADDRESS

    from_token_address: Address = MAINNET_OLAS_ADDRESS
    to_token_address: Address = GNOSIS_OLAS_ADDRESS
    l2_minter_address: Address = GNOSIS_l2_AMB

    msg: str = None
    msg_id: str = None
    msg_data: str = None

    def check_address_maps(self):
        """Check the address maps correctly to the target chain."""
        address_maps = {"ethereum": {"1": MAINNET_OLAS_ADDRESS}, "gnosis": {"100": GNOSIS_OLAS_ADDRESS}}
        # we now check the address maps correctly to the target chain
        assert self.from_bridge_address == address_maps[self.from_ledger_id][self.from_ledger_chain_id]
        assert self.to_bridge_address == address_maps[self.to_ledger_id][self.to_ledger_chain_id]

    def validate(self):
        """Validate the data."""
        try:
            assert self.from_ledger_id == "ethereum"
            assert self.from_ledger_chain_id == "1"
            assert self.to_ledger_id == "gnosis"
            assert self.to_ledger_chain_id == "100"
            self.check_address_maps()
        except AssertionError:
            return False
        return True

    def get_deposit_data(self, crypto):
        """Get the deposit data."""

        @dataclass
        class DepositData:
            token: Address
            receiver: Address
            value: int
            contract_address: Address

        return DepositData(
            token=self.from_token_address,
            receiver=crypto.address,
            value=self.amount,
            contract_address=self.from_bridge_address,
        )

    @property
    def deposit_function(self):
        """Return t."""
        return self.l1_deposit_contract.relay_tokens_1

    @property
    def l1_deposit_contract(self):
        """Return the deposit contract."""
        public_id = OMNI_BRIDGE_PUBLIC_ID
        is_built = Path("vendor").exists()
        root = (Path("packages") / public_id.author) if not is_built else Path("vendor") / public_id.author
        return load_contract(Path(root) / "contracts" / public_id.name)

    def get_allowance_data(self, crypto):
        """Get the allowance data."""

        @dataclass
        class AllowanceData:
            contract_address: Address
            owner: Address
            spender: Address

        return AllowanceData(
            contract_address=self.from_token_address,
            owner=crypto.address,
            spender=self.from_bridge_address,
        )


@dataclass
class GnosisL1L2WithdrawData(BaseL1L2DepositData):
    """Withdrawal data class specific to the Gnosis bridge."""

    amount: int
    from_ledger_id: str = "gnosis"  # the ledger id of the source chain
    from_ledger_chain_id: str = "100"  # the chain id of the source chain
    to_ledger_id: str = "ethereum"  # the ledger id of the destination chain
    to_ledger_chain_id: str = "1"  # the chain id of the destination chain

    from_bridge_address: Address = GNOSIS_l2_AMB
    to_bridge_address: Address = MAINNET_BRIDGE_CONTRACT_ADDRESS

    from_token_address: Address = GNOSIS_OLAS_ADDRESS
    to_token_address: Address = MAINNET_OLAS_ADDRESS
    l2_minter_address: Address = GNOSIS_l2_AMB

    amb_helper_address: Address = GNOSIS_AMB_ADDRESS_HELPER
    l1_claimer_address: Address = POA_EXECUTOR

    msg: str = None
    msg_id: str = None
    msg_data: str = None
    signatures: str = None

    def get_deposit_data(self, *args):
        """Get the deposit data.

        I.e. the data necessary to deposit to the bridge to withdraw the token on the other chain.
        """
        del args  # not used for this specific method

        @dataclass
        class Withdrawal:
            to: Address
            value: int
            contract_address: Address
            data: bytes = b""

        return Withdrawal(to=self.from_bridge_address, value=self.amount, contract_address=self.from_token_address)

    def get_allowance_data(self, crypto):
        """Get the allowance data."""

        @dataclass
        class AllowanceData:
            contract_address: Address
            owner: Address
            spender: Address

        return AllowanceData(
            contract_address=self.from_token_address,
            owner=crypto.address,
            spender=self.from_bridge_address,
        )

    @property
    def deposit_function(self):
        """Return the deposit function."""
        return self.l2_deposit_contract.transfer_and_call

    @property
    def l2_deposit_contract(self):
        """Return the deposit contract."""
        public_id = OLAS_PUBLIC_ID
        is_built = Path("vendor").exists()
        root = (Path("packages") / public_id.author) if not is_built else Path("vendor") / public_id.author
        return load_contract(Path(root) / "contracts" / public_id.name)

    @property
    def signing_bridge_contract(self):
        """Return the signing bridge contract."""
        pubic_id = AMB_GNOSIS_HELPER_PUBLIC_ID
        is_built = Path("vendor").exists()
        root = (Path("packages") / pubic_id.author) if not is_built else Path("vendor") / pubic_id.author
        return load_contract(Path(root) / "contracts" / pubic_id.name)

    @property
    def collected_signature_event_function(self):
        """Get the signature event function."""
        return self.signing_bridge_contract.get_signatures

    @property
    def l1_amb(
        self,
    ):
        """Get the claim function."""
        public_id = AMB_MAINNET_PUBLIC_ID
        is_built = Path("vendor").exists()
        root = (Path("packages") / public_id.author) if not is_built else Path("vendor") / public_id.author
        return load_contract(Path(root) / "contracts" / public_id.name)

    def get_claim_function(
        self,
    ):
        """Get the claim function."""
        return self.l1_amb.safe_execute_signatures_with_auto_gas_limit


class BridgingStrategy(Model):
    """Strategy model class."""

    contracts = {
        "gnosis_olas": OLAS_PUBLIC_ID,
        "l1_amb": AMB_MAINNET_PUBLIC_ID,
        "l2_amb": AMB_GNOSIS_PUBLIC_ID,
        "gnosis_amb_helper": AMB_GNOSIS_HELPER_PUBLIC_ID,
        "erc_20": ERC_20_PUBLIC_ID,
        "omni_bridge": OMNI_BRIDGE_PUBLIC_ID,
    }

    bridge_requests = [
        GnosisL1L2DepositData(
            amount=1  # in decimals of the token
        ),
        GnosisL1L2WithdrawData(
            amount=1  # in decimals of the token
        ),
    ]

    current_bridge_request: BaseL1L2DepositData = None

    def setup(self) -> None:
        """Set up the strategy."""
        for contract_name, public_id in self.contracts.items():
            is_built = Path("vendor").exists()
            root = (Path("packages") / public_id.author) if not is_built else Path("vendor") / public_id.author
            contract = load_contract(Path(root) / "contracts" / public_id.name)
            setattr(self, contract_name, contract)

    @property
    def crypto(self):
        """Get the crypto object."""
        key_path = Path("ethereum_private_key.txt")
        if not key_path.exists():
            self.context.logger.warning("No private key found, generating ephemeral key!")
            return EthereumCrypto()
        return EthereumCrypto(
            private_key_path="ethereum_private_key.txt",
        )

    @property
    def l1_ledger_api(self):
        """Get the l1 ledger api."""
        return EthereumApi(address="https://eth.drpc.org", chain_id=str(1))

    @property
    def l2_ledger_api(self):
        """Get the l2 ledger api."""
        return EthereumApi(address="https://gnosis.drpc.org", chain_id=str(100))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

    def sign_and_send_txn(self, txn, crypto, ledger_api):
        """Sign and send transaction."""
        signed_txn = crypto.sign_transaction(txn)
        txn_hash = ledger_api.send_signed_transaction(signed_txn)
        self.context.logger.info(f"Txn hash: `{txn_hash}`")
        result = False
        try:
            result = ledger_api.api.eth.wait_for_transaction_receipt(txn_hash, timeout=600)
        except Exception as e:
            self.context.logger.exception(f"Error waiting for transaction receipt: {e}")
            self.context.logger.exception(f"Txn hash: {txn_hash}")
            self.context.logger.exception(f"Txn: {txn}")
        if not result:
            self.context.logger.error("Failed to execute transaction!")
            return False, txn_hash
        if result.get("status") == 0:
            self.context.logger.error("Transaction failed on chain!")
            return False, txn_hash
        self.context.logger.info("Transaction executed successfully!")
        return True, txn_hash

    def build_transaction(self, func, crypto, ledger_api):
        """Build the transaction."""
        return func.build_transaction(
            {
                "from": crypto.address,
                "nonce": ledger_api.api.eth.get_transaction_count(crypto.address),
                "gas": 500_000,
                "gasPrice": int(ledger_api.api.eth.gas_price * GAS_PREMIUM),
                "value": 0,
            }
        )
