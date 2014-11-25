#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'me'
SITENAME = u'C-c C-k'
SITESUBTITLE = u'to impress your cat'
SITEURL = ''

PATH = 'content'

STATIC_PATHS = ['.']
IGNORE_FILES = ['.#*', '*~']

THEME = 'blue-penguin'
PLUGINS = ['more']

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'
LOCALE = "C"
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

# DOCUTILS_SETTINGS = {"math_output": "MathML"}

ARTICLE_URL = '{date:%Y}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = [('Quotes', 'quotes.html')]

ARCHIVES_SAVE_AS = 'archives.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = False
DAY_ARCHIVE_SAVE_AS = False

DEFAULT_CATEGORY = 'misc'
DISPLAY_CATEGORIES_ON_MENU = False
USE_FOLDER_AS_CATEGORY = False
CATEGORY_SAVE_AS = False
CATEGORIES_SAVE_AS = False

AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
TAG_SAVE_AS = False
TAGS_SAVE_AS = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = ()
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
