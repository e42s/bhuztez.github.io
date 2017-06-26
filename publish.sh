#!/usr/bin/env bash

pelican -s publishconf.py
./commit.py
