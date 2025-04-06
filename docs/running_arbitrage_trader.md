# Setup a Machine to Run the Trader
# -------------------------------
#

## Introduction

This guide will walk you through the process of setting up a machine to run the Arbitrage Trader.

The arbitrage trader is a tool to automatically execute arbitrage trades between different cryptocurrency exchanges.

## Prerequisites

Before you begin, you will need the following:

- A machine running a recent version of Ubuntu or Debian.
- Python 3.11 installed on the machine.

## Steps 

### Step 1: Create a new machine

Create a new machine on your cloud provider of choice. We recommend using a machine with at least 2 CPUs and 4GB of RAM.

We assume that you have already created a new machine and have SSH access to it.

### Step 2: Install Python 3.11 (Optional)

We recommend using the `pyenv` tool to install Python 3.11.

```bash
curl https://pyenv.run | bash
```

NOTE: Please follow the instructions on the [Pyenv Installer](https://github.com/pyenv/pyenv#b-set-up-your-shell-environment-for-pyenv)

```bash
pyenv install 3.11
```

### Step 3: Checkout The Code

```bash
git clone https://github.com/StationsStation/capitalisation_station.git --recurse-submodules
```

### Step 4: Install the Dependencies


#### LINUX ONLY!
```bash
## Linux Dependencies
sudo apt install -y \
apt-get install make build-essential gcc \
  libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev libffi-dev \
  liblzma-dev uuid-dev xz-utils tk-dev \
  libncursesw5-dev libgdbm-dev libnss3-dev \
  libxml2-dev libxmlsec1-dev \
  libzstd-dev curl wget git -y
```


#### MACOS ONLY!

```bash
## MacOS Dependencies
brew :TODO
```



Ensure shell can be accessed.

```bash
poetry self add poetry-plugin-shell
```

### Step 5: Install the Trader

```bash
cd capitalisation_station
make install

```


### Step 6: Create acounts on Derive
You can create an account at [Derive](https://www.derive.xyz/invite/A0HQW)

You will need to create a smart contract wallet on Derive.
This is available on the [Developer](https://www.derive.xyz/developers)


Once you have an account with derive, you can deposit funds into your wallet and then generate a sub account for the trader.

You will receive a sub account address that you can use to deposit funds into the wallet.


### Step 7: Configure the Trader.

```bash
# create keys MAKE SURE TO SAVE THE GENERATED KEY!
poetry run autonomy generate-key ethereum
```

NOTE: You will need to save the generated key for the next step.

The key has been generated and saved to the file `ethereum_private_key.txt` in the current directory.

NOTE: Available agents are located in the packages/AUTHOR/agents directory.

There are a few necessarcy variables that need to be set in order to run the trader.

- DERIVE_WALLET: This is the smart contract wallet generated on Derive upon signing up. You can get one by signing up at [Derive](https://www.derive.xyz/invite/A0HQW)

- DERIVE_SUB_ACCOUNT: This is the sub account generated on Derive upon signing up. You can get one by signing up at [Derive](https://www.derive.xyz/invite/A0HQW)



```bash
export AGENT=eightballer/derive_arbitrage_agent
poetry run python scripts/generator.py $AGENT
```

### Step 8: Run the Trader

```
# enter the virtual environment
poetry shell
```

```bash
adev run dev $AGENT --no-use-tendermint --force 
```

### Step 9: Monitor the Trader

The agent exposes a HTTP API that you can use to monitor the trader is alive and well.

```bash
curl localhost:8888
{}
```


