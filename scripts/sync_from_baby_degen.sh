#! /bin/bash

set -e

DOWN_STREAM_REPO=../../downstream/baby-degen
adev deps update \
    -p $DOWN_STREAM_REPO \
    --manual \
    -c .

make clean fmt lint
poetry run autonomy packages lock && autonomy push-all
git add packages
git commit -m "Sync packages from downstream at $(date)"
