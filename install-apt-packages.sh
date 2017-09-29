#!/usr/bin/env bash

apt-get -qq update
apt-get install -y python-enchant  # for pypi package sphinxcontrib-spelling
apt-get install -y graphviz        # for sphinx directive graphviz
