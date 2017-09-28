#!/usr/bin/env bash

echo "MZO: show the current date"
date -Is

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

rm -rf ./.doctrees/
rm -rf ./_website/
ablog build

deactivate
