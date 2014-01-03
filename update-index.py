#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import HTMLParser
import os
import os.path
import time
import urllib


HEADER = """<!doctype html>
<html>
<head>
<title>OOP &#8866; FP</title>
<link rel="stylesheet" type="text/css" href="base.css" />
</head>
<body>
<h1>OOP &#8866; FP</h1>
<ul>
"""
FOORTER = """
</ul></body></html>
"""


class MetaDataParser(HTMLParser.HTMLParser):

    def handle_startendtag(self, tag, attrs):
        if tag != 'meta':
            return

        attrs = dict(attrs)

        name = attrs.get("name", None)
        if name == 'og:title':
            self.title = attrs.get("content", None)
        elif name == 'created':
            self.date = attrs.get("content", None)


def find_pages():
    basedir = os.path.dirname(os.path.abspath(__file__))

    for d in os.listdir(basedir):
        subdir = os.path.join(basedir, d)

        if not os.path.isdir(subdir):
            continue

        for p in os.listdir(subdir):
            filename = os.path.join(subdir, p)

            if not p.endswith(".html"):
                continue

            parser = MetaDataParser()

            with open(filename, "r") as f:
                parser.feed(f.read())

            yield (
                os.path.join(d, p),
                parser.title,
                time.strptime(parser.date, "%Y-%m-%d"))


def main():
    pages = list(find_pages())
    pages.sort(key=lambda e: e[2], reverse=True)

    HTML = (
        HEADER +
        '\n'.join(
            [ '<li><a href="%s">%s</a></li>' % (path, title)
              for path, title, time in pages ]) +
        FOORTER)

    with open("index.html", "w") as f:
        f.write(HTML)


if __name__ == "__main__":
    main()
