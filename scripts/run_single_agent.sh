set -e 

# fetch the agent from the local package registry
aea -s fetch $1 --local --alias agent

# go to the new agent
cd agent

# create and add a new ethereum key
aea -s generate-key ethereum && aea -s add-key ethereum

# install any agent deps
aea -s install

# issue certificates for agent peer-to-peer communications
aea -s issue-certificates

# finally, run the agent
aea -s run
