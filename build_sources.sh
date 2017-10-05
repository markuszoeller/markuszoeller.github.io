#!/usr/bin/env bash

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

rm -rf ./.doctrees/
rm -rf ./_website/

# workaround --->
echo "=== MZO: apply private fixes"
echo "Trying to find the file to patch..."
ls -l .venv/local/lib/python2.7/site-packages/ablog/blog.py
find / -name blog.py -type f 2>/dev/null
# <--- workaround

ablog build

deactivate
