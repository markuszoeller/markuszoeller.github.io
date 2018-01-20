#!/usr/bin/env bash

# ---------------------------------------------------------------------------
# Removes all locally existing build artifacts.
#
# getopts usage based on https://stackoverflow.com/a/16496491/1471946
# ---------------------------------------------------------------------------


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


# configuration -------------------------------------------------------------
source ${DIR}/_config.sh


# usage of this script ------------------------------------------------------
usage() {
    echo "Usage: $0 [-h] [-d]";
    echo "  -h  Print this help message."
    echo "  -d  Enable debug option."
    exit 0;
}


# options handling ----------------------------------------------------------
while getopts "hd" o; do
    case "${o}" in
        h)
            usage
            ;;
        d)
            DEBUG='true'
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))


# options evaluation --------------------------------------------------------
[ "$DEBUG" == 'true' ] && set -x



# script functionality ------------------------------------------------------
log "Removing everything..."
rm -rf ${OUTPUT_DIR}
rm -rf ${BUILD_DIR}
rm -rf ${SPHINX_DIR}
rm -rf ${SPELLING_OUT_DIR}
rm -rf ${ASCIINEMA_DIR}
log "Removed everything."
