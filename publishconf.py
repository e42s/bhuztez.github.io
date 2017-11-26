# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://bhuztez.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds.atom.xml'
FEED_ALL_RSS = 'feeds.rss.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing
DISQUS_SITENAME = "bhuztez-github-io"