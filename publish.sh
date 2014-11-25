#!/usr/bin/env bash

pelican -s publishconf.py
python commit.py
