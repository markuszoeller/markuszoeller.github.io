#!/usr/bin/env bash

# ---------------------------------------------------------------------------
# Removes all locally existing build artifacts.
#
# getopts usage based on https://stackoverflow.com/a/16496491/1471946
# ---------------------------------------------------------------------------


# configuration -------------------------------------------------------------
source _config.sh


# usage of this script ------------------------------------------------------
usage() {
    echo "Usage: $0 [-h] [-d]";
    echo "  -h  Print this help message."
    echo "  -d  Enable debug option."
    exit 0;
}


# options handling ----------------------------------------------------------
while getopts "hdn:" o; do
    case "${o}" in
        h)
            usage
            ;;
        d)
            DEBUG='true'
            ;;
        n)
            DRAFT_NAME=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))


# options evaluation --------------------------------------------------------
[ "$DEBUG" == 'true' ] && set -x

echo $DRAFT_NAME
# TODO add slug validation
# TODO add name length validation


# script functionality ------------------------------------------------------
# TODO
# read slug of draft name
# use the template to create dir and main files
log "TODO"
