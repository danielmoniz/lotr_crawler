import os
from urllib import urlretrieve

def try_make_dir(dir_path):
    """ If directory does not exist, make it!"""
    # path_pieces = dir_path.split("/")
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

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

# Not clear on why the 'else' is not working. Commented out for now.
        #else:
            #urlretrieve(urlparse.urlunparse(img_source))

# return the BeautifulSoup object with the modified image src attributes.
    return soup
