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


def check_refugemagoo():
    with open("/tmp/page.html") as f:
        text = f.read()

    soup = bs4.BeautifulSoup(text, "lxml")
    dogs = soup.select("div.wsb-image-inner a")

    count = 0
    for dog in dogs:
        if "petfinder.com" in dog.attrs["href"]:
            count += 1

    # remove nb of "Non disponible" images
    soup = bs4.BeautifulSoup(text, "lxml")
    for img in soup.find_all("img"):
        if re.search("height\w?:\w?230px", img.attrs["style"]) and count > 0:
            count -= 1

    return count

if __name__ == "__main__":
    if not os.path.isfile("/tmp/page.html"):
        download_page("http://www.refugemagoo.org/pour-adoption.html")
        print("DOWNLOADING")

    check_refugemagoo()
