set -e 



# We check if a directory with the name of the agent exists.


agent_name=$(echo $1 | cut -d'/' -f2)
agent_author=$(echo $1 | cut -d'/' -f1)

echo "   Agent author: $agent_author"
echo "   Agent name:   $agent_name"


if [ -d $agent_name ]; then
    echo "Agent $1 already exists. Removing directory $agent_name"
    echo "Please confirm that you want to remove the agent directory $agent_name. This will delete all the agent's data."
    read -p "Are you sure? (y/n) " -n 1 -r
    echo 
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting..."
        exit 1
    fi
    rm -rf $agent_name
fi


# fetch the agent from the local package registry
echo "Fetching agent $1 from the local package registry..."
aea -s fetch $1 --local > /dev/null

# go to the new agent
# n the format eightballer/automation_station, we need to split by / nad go into the second part

cd $agent_name


# create and add a new ethereum key
if [ ! -f ../ethereum_private_key.txt ]; then
    aea -s generate-key ethereum && aea -s add-key ethereum
else
    cp ../ethereum_private_key.txt ./ethereum_private_key.txt
    aea -s add-key ethereum 
fi
# install any agent deps
aea -s install

docker compose up -d --force-recreate 
# issue certificates for agent peer-to-peer communications
if [ ! -f ../.certs ]; then
    aea -s issue-certificates
    cp -r ./.certs ../
else
    cp -r ../.certs ./
fi

# finally, run the agent
#

# We wait for 20 seconds or for the tm node to be ready.
tries=0
tm_started=false
while [ $tries -lt 20 ]; do
    tries=$((tries + 1))
    if curl localhost:8080/hard_reset > /dev/null 2>&1; then
        echo "Tendermint node is ready."
        tm_started=true
        break
    fi
    sleep 1
done
if [ "$tm_started" = false ]; then
    echo "Tendermint node did not start in time. Please verify that the docker tendermint node is running."
    exit 1
fi

echo "Starting the agent..."

aea -s run

echo "Killing tendermint"

docker compose kill && docker compose down
