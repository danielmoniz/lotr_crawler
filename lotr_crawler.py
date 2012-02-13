#!/usr/bin/env python

import sys
import re
import urllib2
import urlparse
from bs4 import BeautifulSoup
import os

crawl_limit = 2
try:
    tocrawl = set([sys.argv[1]])
    linkregex = re.compile('<a\s*href=[\'"](.*?)[\'"].*?>')
# default to crawling the LotR wiki
except IndexError:
    tocrawl = set(['http://www.lotr.wikia.com'])
    linkregex = re.compile('<a\s+href=[\'"](\/wiki\/.*?)[\'"].*?>')

crawled = set([])

while 1:
    try:
        crawling = tocrawl.pop()
        print len(crawled), crawling
    except KeyError:
        raise StopIteration
# don't fully understand this
    url = urlparse.urlparse(crawling)     
    print url, crawling
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
    body = soup.find(id="WikiaArticle")
    print title
    #print body

# If wiki/ directory does not exist, make it!
    dirname = "wiki"
    if not os.path.isdir("./" + dirname + "/"):
        os.mkdir("./" + dirname + "/")

# Get a file-like object for the Python Web site's home page.
    site = urllib2.urlopen(crawling)
    f = open('wiki/' + title, 'w')
    f.write(repr(body))
    f.close()

    """startPos = msg.find('<title>')
    if startPos != -1:
        endPos = msg.find('</title>', startPos+7)
        if endPos != -1:
            title = msg[startPos+7:endPos]
            print title"""
    links = linkregex.findall(msg)
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
