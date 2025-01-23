# Simple script to generate all the protocol files.
set -euo pipefail

SPEC_PATH='../specs/protocols/'

tmp_agent_name='tmp_agent'
function generate_protocol {
    echo "Generating protocol $1"
    rm -rf packages/eightballer/protocols/$1
    aea create $tmp_agent_name
    cd $tmp_agent_name
    adev scaffold protocol $(echo $SPEC_PATH/$1.yaml)
    aea publish --local --push-missing
    cd ..
    rm -rf $tmp_agent_name
    rm -rf packages/eightballer/agents/$tmp_agent_name
    adev -v fmt -p  packages/eightballer/protocols/$1
    adev -v lint -p packages/eightballer/protocols/$1
    pytest packages/eightballer/protocols/$1
}



# generate_protocol 'default'
# generate_protocol 'spot_asset'
# generate_protocol 'ohlcv'
# 
# generate_protocol 'order_book'
# generate_protocol 'markets'

generate_protocol 'orders'
generate_protocol 'balances'
# generate_protocol 'positions'
# 
# generate_protocol 'tickers'
