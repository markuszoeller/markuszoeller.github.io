#!/usr/bin/env bash

docker run \
-d \
-v $(pwd):/reveal.js/content:Z \
-p 50000:8000 \
--name slides \
markus:revealjs
