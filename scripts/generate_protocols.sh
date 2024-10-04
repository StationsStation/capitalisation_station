# Simple script to generate all the protocol files.
set -euo pipefail

SPEC_PATH='../specs/protocols/'

tmp_agent_name='tmp_agent'
function generate_protocol {
    echo "Generating protocol $1"
    rm -rf packages/eightballer/protocols/$1
    adev create $tmp_agent_name -t eightballer/base --force
    cd $tmp_agent_name
    adev scaffold protocol $(echo $SPEC_PATH/$1.yaml)
    aea publish --local --push-missing
    cd ..
    rm -rf $tmp_agent_name
    rm -rf packages/eightballer/agents/$tmp_agent_name
}


generate_protocol 'balances'