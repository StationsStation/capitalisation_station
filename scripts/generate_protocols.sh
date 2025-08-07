# Simple script to generate all the protocol files.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SPEC_PATH="${REPO_ROOT}/specs/protocols"

tmp_agent_name='_tmp_agent'


function generate_protocol {
    proto=$1
    spec_file="${SPEC_PATH}/${proto}.yaml"
    author=$(awk -F': +' '/^author:/ { print $2; exit }' "$spec_file")

    echo "🔧 Generating protocol ${proto} by ${author}"
    rm -rf "packages/${author}/protocols/${proto}"

    function _cleanup {
      rm -rf "packages/${author}/agents/${tmp_agent_name}"
      rm -rf "${tmp_agent_name}"
    }
    trap '_cleanup' EXIT

    aea create "$tmp_agent_name"
    cd "$tmp_agent_name"
      adev scaffold protocol "$spec_file"
      aea publish --local --push-missing
    cd ..

    adev -v fmt -p  "packages/${author}/protocols/${proto}"
    adev -v lint -p "packages/${author}/protocols/${proto}"
    pytest "packages/${author}/protocols/${proto}"

}


generate_protocol 'asset_bridging'
generate_protocol 'order_book'
generate_protocol 'positions'
generate_protocol 'orders'
generate_protocol 'markets'
generate_protocol 'tickers'
generate_protocol 'balances'
generate_protocol 'liquidity_provision'
generate_protocol 'default'
generate_protocol 'spot_asset'
generate_protocol 'ohlcv'
