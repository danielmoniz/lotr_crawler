import urllib
# Get a file-like object for the Python Web site's home page.
data = urllib.urlencode({"find" : "XMLForms", "findtype" : "t"})
site_url = "http://www.python.org"
site = urllib.urlopen(site_url, data)
# Read from the obhect, storing the page's contents in 'site_html'.
site_html = site.read()
site.close()

f = open('python_html', 'w')
f.write(site_html)
f.close()
