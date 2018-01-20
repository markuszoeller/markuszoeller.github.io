#!/usr/bin/env bash


# ---------------------------------------------------------------------------
# Builds the whole website.
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


source ${BUILD_DIR}/bin/activate

log "Building the blog sources..."
${BUILD_DIR}/bin/ablog build
log "Built the blog sources."

deactivate
