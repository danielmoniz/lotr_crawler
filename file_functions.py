import os
import urlparse
from urllib import urlretrieve

def try_make_dir(dir_path):
    """ If directory does not exist, make it! 
    @TODO Make this function build an entire path, not just 
    a folder. """
    # path_pieces = dir_path.split("/")
    if not os.path.isdir(dir_path):
        os.mkdirs(dir_path)

def pull_images(soup, url, out_folder, html_folder):
    """ find all images, pull them, and put them in folders
    'soup' is sent in order to modify the image src html to 
    point images at local files """
    images = soup.findAll('img')
    if len(images) > 0:
        try_make_dir(out_folder)

    for image in images:
        try:
            img_source = image["src"]
        except KeyError:
            #print image
            continue

        filename = img_source.split("/")[-1]
        #print filename, img_source
        outpath = os.path.join(out_folder, filename)
        html_path = os.path.join(html_folder, filename)
        if image["src"].lower().startswith("http"):
            full_image_source = image["src"]
        elif image["src"].lower().startswith("//"):
            full_image_source = url[0] + ":" + image["src"]
        elif image["src"].lower().startswith("/"):
            parsed_url = list(url)
            url = list(url)
            url[2] = img_source
            full_image_source = urlparse.urlunparse(url)
            #print "urlretrieve: ", full_img_source, urlretrieve(full_img_source)
        else:
            print "Image failed to pull:", full_img_source
            continue

# retrieve image and replace img src in HTML with local image path
        urlretrieve(full_image_source, outpath)
        new_image = soup.find("img", src=image["src"])
        new_image["src"] = html_path
        soup.find("img", src=image["src"]).replaceWith(new_image)


# return the BeautifulSoup object with the modified image src attributes.
    return soup

def get_full_formatted_url(url, link):
    """ Take in a url object and a link, as found in an <a> tag. 
        Use the url object to generate any remaining pieces of the 
        link, and add http:// if necessary (etc.) """
    if link.startswith('/'):
        link = 'http://' + url[1] + link
    elif link.startswith('#'):
        link = 'http://' + url[1] + url[2] + link
    elif not link.startswith('http'):
        link = 'http://' + url[1] + '/' + link
    return link
