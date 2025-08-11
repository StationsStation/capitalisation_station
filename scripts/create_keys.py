"""
Simple script to prepare the runner folder for the first time.

"""
import json
from pathlib import Path

from rich import print
from rich.prompt import Prompt as prompt
from aea_ledger_solana import SolanaCrypto
from aea_ledger_ethereum import EthereumCrypto
from aea.cli.generate_key import _generate_multiple_keys


RUNNER_FOLDER_NAME = ".runner"
DEFAULT_RUNNER_PATH = Path(__file__).parent.parent / RUNNER_FOLDER_NAME

REQUIRED_KEYS = {
    "SAFE_ADDRESS",
    "APPRISE_ENDPOINT",
}

class EnvPreparation():
    """Crypto keys and runner folder preparation."""

    def __init__(self):
        self.runner_path = DEFAULT_RUNNER_PATH
        return self.execute()

    def create_runner_folder_if_not_exists(self):
        """Create the runner folder if it does not exist."""
        if not self.runner_path.exists():
            self.runner_path.mkdir()
            print(f"\t ✅ - Runner folder created at `{self.runner_path}`")
            return 
        raise Exception(f"\t ❌ - Runner folder already exists at `{self.runner_path}`")
    
    def create_keys(self):
        """Create the crypto keys."""
        
        # we first generate the agent keys.
        for crypto in [EthereumCrypto, SolanaCrypto]:
            _generate_multiple_keys(
                n=1,
                type_=crypto.identifier,
                file=self.runner_path / f"{crypto.identifier}_private_key.json",
            )
            print(f"\t ✅ - Generated {crypto.identifier} private key")
            # We read in the public address and display to the user.
            json_file = self.runner_path / f"{crypto.identifier}_private_key.json"
            data = json.loads(json_file.read_text()).pop()
            print(f"\t\t Public Address: \t `{data['address']}`")
        # we then generate the owner/operator key.
        _generate_multiple_keys(
            n=1,
            type_=EthereumCrypto.identifier,
            file=self.runner_path / "operator_private_key.json",
        )




    def check_for_dotenv(self):
        """Check if the .env file exists."""
        if (self.runner_path / ".env").exists():
            raise Exception(f"Please create a .env file in the runner folder at {self.runner_path} \t :warning:")
        # We have a set of necessary keys we need to populate the .env file with.
        key_vals = {
            k: prompt.ask(f"Please enter the value for key {k}: ", password=True) for k in REQUIRED_KEYS
        }
        with open(self.runner_path / ".env", "w") as f:
            for k, v in key_vals.items():
                f.write(f"export {k}={v}\n")

    def execute(self):
        """Execute the preparation."""
        print("Creating runner folder...PLEASE WAIT")
        self.create_runner_folder_if_not_exists()
        print("Generating crypto keys...")
        self.create_keys()
        print("Checking for .env file...", )
        self.check_for_dotenv()
        print("\t :tada: Environment preparation completed. ")

        # We now have the runner folder and the crypto keys.

if __name__ == "__main__":
    env = EnvPreparation()
