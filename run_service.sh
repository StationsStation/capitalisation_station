#! env bash

set -euo pipefail 

# This script is used to run the service


echo "Running Arbing Service..."

function create_keys() {
    if [ ! -d ".runner" ]; then
        echo "Creating environment"
        poetry run python scripts/create_keys.py
    fi
}

function run_service() {
    echo "Running service"
    export MAS_KEYPATH=$(echo -n $(pwd)/.runner/ethereum_private_key.json)
    source .runner/.env
    bash scripts/run_mas.sh eightballer/sol_evm_arbitrage 
}

create_keys

run_service

