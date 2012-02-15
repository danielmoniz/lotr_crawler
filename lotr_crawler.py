#!/usr/bin/env python

import sys
import re
import urllib2
import urlparse
from bs4 import BeautifulSoup
from file_functions import try_make_dir, pull_images

crawl_limit = 1
try:
    tocrawl = set([sys.argv[1]])
# default to crawling the LotR wiki
except IndexError:
    tocrawl = set(['http://www.lotr.wikia.com'])
crawled = set([])

while 1:
    try:
        crawling = tocrawl.pop()
    except KeyError:
        raise StopIteration
# Put the URL into an object for ease of use
    url = urlparse.urlparse(crawling)     
    try:
        response = urllib2.urlopen(crawling)
    except:
        continue
    msg = response.read()
    soup = BeautifulSoup(msg)
# find script tags and remove them
    to_extract = soup.findAll('script')
    for item in to_extract:
        item.extract() # a BeautifulSoup function for removing tags

    title = soup.title.string
    strip_title = title.replace(' ', '-')

    try_make_dir("wiki")
    try_make_dir('wiki/images')
    soup = pull_images(soup, url, 'wiki/images/' + strip_title  + '/', 'images/' + strip_title + '/')

    body = soup.find(id="WikiaArticle")
    print title

# Get a file-like object for the Python Web site's home page.
    site = urllib2.urlopen(crawling)
    f = open('wiki/' + strip_title, 'w')
    f.write(repr(body))
    f.close()

# pull all links and add them to the list of links to crawl
    temp_links = soup.findAll('a')
    links = []
    for link in temp_links:
# if <a> tag has no href, do not append it
        try:
            links.append(str(link['href']))
        except KeyError:
            pass

    crawled.add(crawling)
    if len(crawled) >= crawl_limit:
        break
    for link in (links.pop(0) for _ in xrange(len(links))):
        if link.startswith('/'):
            link = 'http://' + url[1] + link
        elif link.startswith('#'):
            link = 'http://' + url[1] + url[2] + link
        elif not link.startswith('http'):
            link = 'http://' + url[1] + '/' + link
        if link not in crawled:
            tocrawl.add(link)
