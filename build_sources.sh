#!/usr/bin/env bash

rm -rf ./.doctrees/
rm -rf ./_website/
ablog build

echo "The newly built blog content is ready:"
ls -la
