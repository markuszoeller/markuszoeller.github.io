#!/usr/bin/env bash

# This should be possible on mailing lists and git commit messages:
# """
# According to [99] [... and so on ...].
# References:
# [99] http://www.markusz.io/posts/YYYY/MM/DD/permalink-to-the-referenced-post/
# """
# This is 77 chars long, which makes it "line-break save" for mailing lists and
# git commit messages.
# It breaks down to this:
#    "[99] "                                      ==  5 chars
#    "http://www.markusz.io/"                     == 22 chars
#    "posts/YYYY/MM/DD/"                          == 17 chars
#    "permalink-to-the-referenced-post/"          == 33 chars
# This means we have to check for 33 chars.

POST_DIR_NAME_LEN_MAX=33

# only the directories with an "index.rst" file are posts
for POST_DIR_PATH in $(find posts/ -type f -name index.rst -printf '%h\n')
do
    POST_DIR_NAME=`basename "$POST_DIR_PATH"`
    size=${#POST_DIR_NAME}
    if [ ${size} -ge ${POST_DIR_NAME_LEN_MAX} ]
    then
        echo "$POST_DIR_NAME is longer than $POST_DIR_NAME_LEN_MAX chars."
    fi
done

