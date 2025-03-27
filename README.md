# Capitalisation Station

Agent components specifically built for financial trading using agents.

Built with the [Olas](https://olas.network) stack.

## Getting Started

This repository contains a number of components that can be used to build trading agents. The components are built with the [Olas](https://olas.network) stack.

The main components of interest are

### Connections

- [eightballer/ccxt](packages/eightballer/connections/ccxt)
    This connection enables the agents to send messages to the ccxt connection allowing generic trading on more than 300 centralised exchanges.
- [eightballer/dcxt](packages/eightballer/connections/dcxt)
    This connection enables the agents to send messages to the dcxt connection allowing generic trading on a number of decentralised exchanges.
    The included exchanges are:

    - [Balancer](https://balancer.finance/)
    - [Uniswap](https://uniswap.org/)
    - [JupyterSwap](https://jup.ag/)
    - [100x](https://100x.finance/)
    - [lyra](https://lyra.finance/)


In order to add a new exchange to the dcxt connection, you need to create a new connection in the [dcxt](packages/eightballer/connections/dcxt/dcxt/) directory.



### Setup for Development

If you're looking to contribute or develop with `capitalisation_station`, get the source code and set up the environment:

```shell
git clone https://github.com/StationsStation/capitalisation_station.git --recurse-submodules
cd capitalisation_station
make install
```

## Commands

Here are common commands you might need while working with the project:

### Formatting

```shell
make fmt
```

### Linting

```shell
make lint
```

### Testing

```shell
make test
```

### Locking

```shell
make hashes
```

### all

```shell
make all
```

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Upstream Dependenencies


All solana credit for the jupyter integration goes to

With specific reference to components;
contract/vybe/jupitar_swap/0.1.0
https://github.com/Dassy23/aea_contracts_solana/


### Autonomy repos
