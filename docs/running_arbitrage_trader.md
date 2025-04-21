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

### Step 2: Make Sure Docker is Installed.

Please visit the [Docker installation guide](https://docs.docker.com/engine/install/) for your operating system.
Make sure to install the latest version of Docker.
You can check if Docker is installed by running the following command:

```bash
docker --version
```
### Step 3: Install Install the Agent runner from [autodev.sh]


### Step 4: Create acounts on Derive
You can create an account at [Derive](https://www.derive.xyz/invite/A0HQW)

You will need to create a smart contract wallet on Derive.
This is available on the [Developer](https://www.derive.xyz/developers)


Once you have an account with derive, you can deposit funds into your wallet and then generate a sub account for the trader.

You will receive a sub account address that you can use to deposit funds into the wallet.


### Step 7: Configure the Trader.

```bash
# create keys MAKE SURE TO SAVE THE GENERATED KEY!
docker run --workdir /app/tmp -v $(pwd):/app/tmp  -it --entrypoint /app/.venv/bin/autonomy 8ball030/capitalisation_station:latest generate-key ethereum
```

NOTE: You will need to save the generated key for the next step.

The key has been generated and saved to the file `ethereum_private_key.txt` in the current directory.

NOTE: Available agents are located in the packages/AUTHOR/agents directory.

There are a few necessarcy variables that need to be set in order to run the trader.

- DERIVE_WALLET: This is the smart contract wallet generated on Derive upon signing up. You can get one by signing up at [Derive](https://www.derive.xyz/invite/A0HQW)

- DERIVE_SUB_ACCOUNT: This is the sub account generated on Derive upon signing up. You can get one by signing up at [Derive](https://www.derive.xyz/invite/A0HQW)



```bash
export AGENT=eightballer/derive_arbitrage_agent
docker run --workdir /app/tmp -v $(pwd):/app/tmp -it --entrypoint /app/.venv/bin/python 8ball030/capitalisation_station:latest scripts/generator.py $AGENT
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


