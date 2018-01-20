#!/usr/bin/env bash

# ---------------------------------------------------------------------------
# Creates the build directory.
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
log "Creating the build directory..."

virtualenv ${BUILD_DIR}
${BUILD_DIR}/bin/pip install -r ${DIR}/../requirements.txt

# private fixes --->
log "Applying private fix for https://github.com/abakan/ablog/issues/94"
patch --forward --unified --quiet -d ${DIR}/../.venv/local/lib/python2.7/site-packages/ablog < ${DIR}/../patches/tomorrow.diff ; \

if [ $? -eq 1 ] ; then echo "Already patched." ; fi
# <--- private fixes

log "Created the build directory."
