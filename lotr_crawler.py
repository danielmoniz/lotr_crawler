#!/usr/bin/env python

import sys
import re
import urllib2
import urlparse
from bs4 import BeautifulSoup
from file_functions import try_make_dir, pull_images, get_full_formatted_url

crawl_limit = 5
#image_limit_per_page = 1
try:
    tocrawl = sys.argv[1]
# default to crawling the LotR wiki
except IndexError:
    tocrawl = 'http://www.lotr.wikia.com'
# save base url as the relevant domain. Ensure we stay on that domain
domain_url_object = urlparse.urlparse(tocrawl)
# set domain as 'google' in (eg) "http://maps.google.com/toronto?p=1
domain = domain_url_object[1].split(".")[-2]
#domain = domain_url_object[1]
tocrawl = set([tocrawl])
print 'tocrawl:', tocrawl
print 'domain:', domain
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
    try:
        soup = BeautifulSoup(msg)
# if HTML fails to parse, just move on
    except:
        print "Failed to parse page:", crawling
        continue
# find script tags and remove them
    to_extract = soup.findAll('script')
    for item in to_extract:
        item.extract() # a BeautifulSoup function for removing tags

    title = soup.title.string
    strip_title = title.strip().replace(' ', '-')

    try_make_dir(domain)
    try_make_dir(domain + '/images')
    soup = pull_images(soup, url, domain + '/images/' + strip_title  + '/', 'images/' + strip_title + '/')

    body = soup.find("body")
    print title, crawling

# Get a file-like object for the Python Web site's home page.
    site = urllib2.urlopen(crawling)
    f = open(domain + '/' + strip_title, 'w')
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
        link_domain = url[1].split(".")[-2]
        link = get_full_formatted_url(url, link)
        if link not in crawled and link_domain == domain:
            tocrawl.add(link)
        # temporary: print off url if the domain does not match
        elif url[1] != domain:
            pass
            #print "Incorrect domain name:", link_domain
