import requests
import bs4
import logging
import sys
import util
import hashlib
import xml.etree.ElementTree as ET
import secrets
from pprint import pprint

### Create your module for api key and notification method
try:
    import secrets
except ImportError:
    print("Comment import line or create secrets.py module")
    sys.exit()


def check_animadoption():
    url = "https://www.facebook.com/media/set/?set=a.728949963803199.1073741834.688504404514422"
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    images = soup("i",attrs={ "class": "uiMediaThumbImg"})
    count = 0
    for image in images:
        if "1340388899821365749" in image['style']:
            continue
        else:
            count += 1

    return count

def check_aubergezen():
    url = "https://www.facebook.com/media/set/?set=a.807747219323790.1073741849.530757323689449"
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    images = soup("i",attrs={ "class": "uiMediaThumbImg"})
    count = 0
    for image in images:
        count += 1

    return count

def check_bergerblanc(ville):
    url = "https://www.bergerblanc.com/?p=animaux&t=adoptions&s=4&l=%s" % ville
    text = requests.get(url).text

    soup = bs4.BeautifulSoup(text, "lxml")
    images = soup("div", attrs={ "class": "Result"})
    count = 0
    for image in images:
        if "Adopted" in str(image):
            continue
        else:
            count += 1

    return count

def check_spcalaurentides():
    url = "http://www.spcall.ca/adoption/adoption-de-chiens/"
    text = requests.get(url).text

    soup = bs4.BeautifulSoup(text, "lxml")
    images_div = soup("ul", attrs={"class": "list"})[0].contents

    count = 0
    for image in images_div:
        if image == "\n":
            continue
        elif "Adopt" in str(image):
            continue
        else:
            count += 1

    return count

def check_nouveaudepart():
    url = "http://www.animalnouveaudepart.com/services/adoption-d-animaux"
    text = requests.get(url).text

    soup = bs4.BeautifulSoup(text, "lxml")
    image_tag = soup("div", attrs={"class": "floatbox"})

    count = 0
    for img in image_tag:
        full_div = img.parent
        if "chat" in str(full_div).lower():
            continue
        elif "joignez-vous" in str(full_div).lower():
            continue
        elif "aider notre refuge" in str(full_div).lower():
            continue
        else:
            count += 1

    return count

def check_spcamontreal():
    key = secrets.get_petfinder_key()
    secret = secrets.get_petfinder_secret()

    string_to_hash = "%skey=%s" % (secret, key)
    sig = hashlib.md5(string_to_hash.encode()).hexdigest()
    url_api = "http://api.petfinder.com"

    url = "%s/auth.getToken?key=%s&sig=%s" % (url_api, key, sig)
    text = requests.get(url).text
    root = ET.fromstring(text)
    token = root.findall("./auth/token")[0].text

    url = "%s/shelter.getPets?key=%s&token=%s&id=QC06" % (url_api, key, token)
    text = requests.get(url).text

    with open("/tmp/out.xml", "w") as f:
        f.write(text)

    root = ET.fromstring(text)
    dogs = root.findall('./pets/pet[animal="Dog"]')[0]

    count = 0
    for dog in dogs:
        pprint(dog)
        count += 1

    print(count)


    sys.exit()

    with open("/tmp/out.html", "w") as f:
        f.write(text)

    soup = bs4.BeautifulSoup(text, "lxml")
    print(soup("em", attrs={"data-id": "totalresults"})[0])

    return 0


