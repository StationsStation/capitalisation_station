#! /bin/bash

set -e

DOWN_STREAM_REPO=../../downstream/baby-degen
adev deps update \
    -c $DOWN_STREAM_REPO \
    --manual \
    -p .

cd $DOWN_STREAM_REPO 
make clean
poetry run autonomy packages lock && autonomy push-all
git add packages
git commit -m "Sync packages with upstream at $(date)"
