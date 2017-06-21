import requests
import bs4
import sys
import xml.etree.ElementTree as ET
from pprint import pprint
import os
import configs.config as config
import re
import util


def download_page(url):
    r = requests.get(url.strip())
    if r.status_code != 200:
        raise Exception("HTTP code %s: %s" % (r.status_code, url))

    with open("/tmp/page.html", "w") as f:
        f.write(re.sub("(<!--|-->)", "", r.text, re.MULTILINE))


def check_lecaps(url):
    r = re.search("album_id=([0-9]+)", url)
    album_id = r.groups()[0]
    obj = util.query_facebook_album(album_id)

    return obj["count"] - 1


if __name__ == "__main__":
    url = "https://www.facebook.com/pg/lecapsst/photos/?tab=album&album_id=1545894222343392"
    if not os.path.isfile("/tmp/page.html"):
        download_page(url)
        print("DOWNLOADING")

    count = check_lecaps(url)
    print(count)
