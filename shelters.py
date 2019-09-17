import bs4
import requests
import sys
import json
import util
import hashlib
import xml.etree.ElementTree as ET
from pprint import pprint
import configs.config as config
import re


def check_lecaps(url):
    r = re.search("album_id=([0-9]+)", url)
    album_id = r.groups()[0]
    obj = util.query_facebook_album(album_id)
    return obj["count"] - 1

    #text = util.query_page(url)
    #r = re.search("album_id=([0-9]+)", url)
    #album_id = r.groups()[0]



def check_animadoption(url):
    r = re.search("album_id=([0-9]+)", url)
    album_id = r.groups()[0]
    obj = util.query_facebook_album(album_id)

    return obj["count"] - 1


def check_aubergezen(url):
    r = re.search("album_id=([0-9]+)", url)
    album_id = r.groups()[0]
    obj = util.query_facebook_album(album_id)

    return obj["count"]


def check_bergerblanc(url, shelter):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")

    if "montreal" in shelter:
        return len(soup.select(".chiens_sort.montreal_sort"))

    elif "laval" in shelter:
        a = soup.select(".chiens-laval_sort")
        b = len(a)
        return b

    else:
        print("PROBLEME")


def check_spcalaurentides(url):
    text = util.query_page(url)

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


def check_nouveaudepart(url):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    image_tag = soup("div", attrs={"class": "floatbox"})

    count = 0
    for img in image_tag:
        full_div = img.parent
        text = str(full_div).lower()
        if "chat" in text or "joignez-vous" in text or "aider notre refuge" in text or "conclusion" in text or "dog bazar" in text or "cochon d'inde" in text:
            continue
        else:
            count += 1

    return count


def check_animatch(url):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    images_container = soup("div", attrs={"class": "row entry-listing"})[0]

    count = 0
    for img in images_container.children:
        count += 1

    return count


def check_rivesud(url):
    r = re.search("album_id=([0-9]+)", url)
    album_id = r.groups()[0]
    obj = util.query_facebook_album(album_id)

    return obj["count"] - 1


def check_lacabanealiam(url):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    dogs = soup.select(".wsite-content-title")

    count = 0
    for dog in dogs:
        if "Chiens disponibles" not in dog.text and "ADOPT" not in dog.text and "non-disponible" not in dog.text:
            count += 1

    return count


def check_rosieanimaladoption(url):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    dogs_list = soup("div", attrs={"class": "item"})
    count = 0

    for dog in dogs_list:
        string = dog.h3.a.text.lower()
        if not re.search("is.*(reserved|not.*available)", string):
            count += 1

    return count


def check_refugemagoo(url):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    dogs = soup.select("div.img_rounded_corners > a")

    return len(dogs)


def check_carrefourcanin(url):
    text = util.query_page(url)
    count = 0

    soup = bs4.BeautifulSoup(text, "lxml")
    dogs = soup.find_all("div", {"class": "row", "style": "margin-bottom: 50px;"})

    for dog in dogs:
        if "chien" in str(dog).lower() or "chiot" in str(dog).lower():
            count += 1

    return count


def check_lespattesjaunes(url):
    burp0_url = "https://lespattesjaunes.com:443/wp-admin/admin-ajax.php"
    burp0_cookies = {"pll_language": "fr"}
    burp0_data = {"action": "ajax_filter_animals",
                  "filters": "{\"size\":[\"25\",\"24\"],\"gender\":[\"20\"],\"age\":[\"21\"],\"compatibility\":[\"27\"],\"energy\":[\"30\",\"31\"]}",
                  "cpt": "dogs"}
    r = requests.post(burp0_url, cookies=burp0_cookies, data=burp0_data)
    data = json.loads(r.text)['data']
    soup = bs4.BeautifulSoup(data, "lxml")
    dogs = soup("div", attrs={"class": "animal-archive-block"})
    return len(dogs)


def check_spamauricie(url):
    text = util.query_page(url)
    count = int(re.findall("([0-9]+) résultats", text, re.IGNORECASE)[0])
    return count


def check_refugeamr(url):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    nb_dogs = len(soup.select("div.gallery-item > span.img-wrap"))

    return nb_dogs


def check_spcalanaudiere(url):
    text = util.query_page(url)

    nb_dogs = len(re.findall("Chien \-.*Race", text, re.IGNORECASE))

    return nb_dogs


def check_lerefugefmv(url):
    r = re.search("album_id=([0-9]+)", url)
    album_id = r.groups()[0]
    obj = util.query_facebook_album(album_id)

    return obj["count"]



def check_spcamontreal(url):

    key = config.petfinder_key
    secret = config.petfinder_secret

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
        #pprint(dog)
        count += 1

    print(count)


    sys.exit()

    with open("/tmp/out.html", "w") as f:
        f.write(text)

    soup = bs4.BeautifulSoup(text, "lxml")
    print(soup("em", attrs={"data-id": "totalresults"})[0])

    return 0


