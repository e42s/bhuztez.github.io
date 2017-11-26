#!/usr/bin/env bash

pelican-3 -s publishconf.py
./commit.py
