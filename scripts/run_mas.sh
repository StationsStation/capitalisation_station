#! /bin/bash
# Start the MAS service.
set -e

echo "Using autonomy version: $(autonomy --version)"

# we check if the service alias is already used
# if it is, we hard exit
if [ -d "service" ]; then
    echo "Service $1 already exists at path ./service"
    exit 1
fi
echo "-----------------------------"
echo "Starting service $1"

# if the key path is not set, we hard exit
if [ -z "$MAS_KEYPATH" ]; then
    echo "MAS_KEYPATH is not set!"
    exit 1
fi

echo "-----------------------------"
echo "Using keys: $MAS_KEYPATH"

export MAS_ADDRESS=$(echo -n $(cat $MAS_KEYPATH | jq '.[].address' -r))

echo "Using Address: $MAS_ADDRESS"


# if the service name is not set, we hard exit
if [ -z "$1" ]; then
    echo "Service name is not set!"
    exit 1
fi

autonomy fetch --service $1 --local --alias service
cd service 
autonomy build-image --extra-dependency hypothesis
autonomy deploy build $MAS_KEYPATH 

echo "-----------------------------"
echo "Service $1 built!"

echo "Starting service $1"
cd abci_build && \
    docker-compose up -d --force-recreate
echo "Service $1 started!"
