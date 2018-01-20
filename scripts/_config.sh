#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


BUILD_DIR=${DIR}/../.venv
OUTPUT_DIR=${DIR}/../_website
SPHINX_DIR=${DIR}/../.doctrees
ASCIINEMA_DIR=${DIR}/../.asciinema
SPELLING_OUT_DIR=${DIR}/../build/spelling

# Print a log message to stdout.
#   arg1  message to print
log() {
    local msg=$1
    echo "LOG: ${msg}"
}
#SPELLING_CMD=$(BUILD_DIR)/bin/sphinx-build -Q -b spelling -d .doctrees .
