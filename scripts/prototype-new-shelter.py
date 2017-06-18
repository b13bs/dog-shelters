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


def check_carrefourcanin():
    with open("/tmp/page.html") as f:
        text = f.read()

    soup = bs4.BeautifulSoup(text, "lxml")
    dogs = soup.select(".pet-file")

    return len(dogs)

if __name__ == "__main__":
    if not os.path.isfile("/tmp/page.html"):
        download_page("http://www.carrefourcanin.com/ui/s_public/animals.aspx?status=0")
        print("DOWNLOADING")

    check_carrefourcanin()
