# Jupitar Swap

## Set up the environment inside the directory

- Run the following commands inside the directory:
  - `pipenv --python 3.11 && pipenv shell`
  - `pip install open-aea[all]`
  - `pip install open-aea-ledger-solana`
  - `pip install zstandard --force-reinstall` (This is related to M1 Mac)

Housekeeping and Setup
- Use the following command to find out where pipenv is located:
  - `pipenv --venv` (Add this to .vscode settings and launch for testing)
- For testing errors, `pytest --collect-only` is your friend
- For fingerprinting ` aea fingerprint contract dassy23/orca_whirlpool:0.1.0`
Set interpreter to your venv environment from the above command

Notes about the protocol

Docs: [Jup Documentation](https://station.jup.ag/docs)
