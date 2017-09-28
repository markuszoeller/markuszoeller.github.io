#!/usr/bin/env bash

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

rm -rf ./.doctrees/
rm -rf ./_website/
ablog build

deactivate
