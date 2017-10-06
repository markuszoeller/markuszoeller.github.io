#!/usr/bin/env bash

# let's start clean
rm -rf build

# Don't output anything (the findings get saved in the build dir)
sphinx-build -Q -b spelling -d .doctrees . build/spelling

# Show me all the spelling findings
cat build/spelling/output.txt

# we also finish clean
rm -rf build

