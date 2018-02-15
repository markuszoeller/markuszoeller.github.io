#!/usr/bin/env bash

# =====================================================================
# This script creates a "<post-name>*.tar.gz" file, which contains
# all contents of a post, to enable the download for others.
#
# Example:
#   ./tar-me.sh
# =====================================================================

post_name=$(basename $(pwd))

tar \
--exclude=".*" \
--exclude="tar-me.sh" \
--exclude="index.rst" \
--exclude="${post_name}.tar.gz" \
--directory="$(pwd)" \
-zcvf "${post_name}.tar.gz" *

# --exclude="./*"                   # exclude invisible dirs (like .vagrant)
# --exclude="tar-me.sh"             # exclude this script itself
# --exclude="index.rst"             # exclude the post
# --exclude="${post_name}.tar.gz"   # exclude previously created archives
# --directory="$(pwd)"              # use only the post dir in the archive
# -zcvf "${post_name}.tar.gz" *     # the archive has the name of the post
