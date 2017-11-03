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
# This means we have to check for 50 chars (17+33). To be precise, only the
# last part of 33 chars is flexible (the name of the post), the rest is fix.

URL_LEN_MAX=50

LONG_URLS=$(find posts/ -type d | awk "length>$URL_LEN_MAX")

if [[ ! -z "$LONG_URLS" ]]; then
  echo "$LONG_URLS"
  echo "These URLs are longer than the allowed $URL_LEN_MAX chars."
  exit 1
fi
