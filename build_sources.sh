#!/usr/bin/env bash

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

rm -rf ./.doctrees/
rm -rf ./_website/

# private fixes --->
echo "=== MZO: apply private fix for https://github.com/abakan/ablog/issues/94"
patch --verbose -d .venv/local/lib/python2.7/site-packages/ablog < patches/tomorrow.diff
# <--- private fixes

ablog build

deactivate
