#!/usr/bin/env python

import sys
import re
from urllib import urlretrieve
import urllib2
import urlparse
from bs4 import BeautifulSoup
import os

def try_make_dir(dir_path):
    """ If directory does not exist, make it!"""
    # path_pieces = dir_path.split("/")
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def pull_images(soup, url, out_folder, html_folder):
    """ find all images, pull them, and put them in folders
    'soup' is sent in order to modify the image src html to 
    point images at local files
    """
    images = soup.findAll('img')
    if len(images) > 0:
        try_make_dir(out_folder)

    for image in images:
        try:
            img_source = image["src"]
        except KeyError:
            print image
            continue

        filename = img_source.split("/")[-1]
        print filename, img_source
        outpath = os.path.join(out_folder, filename)
        html_path = os.path.join(html_folder, filename)
        if image["src"].lower().startswith("http"):
            urlretrieve(image["src"], outpath)
            new_image = soup.find("img", src=image["src"])
            new_image["src"] = html_path
            soup.find("img", src=image["src"]).replaceWith(new_image)

        #else:
            #urlretrieve(urlparse.urlunparse(img_source))
    return soup

crawl_limit = 2
try:
    tocrawl = set([sys.argv[1]])
    linkregex = re.compile('<a\s*href=[\'"](.*?)[\'"].*?>')
# default to crawling the LotR wiki
except IndexError:
    tocrawl = set(['http://www.lotr.wikia.com'])
    #linkregex = re.compile('<a\s+href=[\'"](\/wiki\/.*?)[\'"].*?>')

crawled = set([])

while 1:
    try:
        crawling = tocrawl.pop()
        print len(crawled), crawling
    except KeyError:
        raise StopIteration
# don't fully understand this
    url = urlparse.urlparse(crawling)     
    print "crawling:", crawling
    print "url:", url
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

    try_make_dir('wiki/images')
    soup = pull_images(soup, url, 'wiki/images/' + strip_title  + '/', 'images/' + strip_title + '/')

    body = soup.find(id="WikiaArticle")
    print title
    #print body

    try_make_dir("wiki")

# Get a file-like object for the Python Web site's home page.
    site = urllib2.urlopen(crawling)
    f = open('wiki/' + title, 'w')
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

    print 'links', links

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
