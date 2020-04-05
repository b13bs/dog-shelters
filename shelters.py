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
        return int(soup.find("a", {"class": "chiens_sort_button"}).find("small").text.strip())

    elif "laval" in shelter:
        return int(soup.find("a", {"class": "chiens-laval_sort_button"}).find("small").text.strip())

    else:
        print("PROBLEME")


def check_spcalaurentides(url):
    count = 0

    for i in [0, 9, 19, 29]:
        text = util.query_page("%s?start=%s" % (url, i))
        soup = bs4.BeautifulSoup(text, "lxml")

        petpic = len(soup.find_all("div", {'class':'petPic'}))
        petstatus = len(soup.find_all("div", {'class':'petStatus'}))

        count += petpic
        count -= petstatus

    return count


def check_nouveaudepart(url):
    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    image_tag = soup("div", attrs={"class": "floatbox"})

    count = 0
    for img in image_tag:
        full_div = img.parent
        text = str(full_div).lower()
        if "chat" in text or "joignez-vous" in text or "aider notre refuge" in text or "conclusion" in text or "dog bazar" in text or "cochon d'inde" in text or "octodon" in text:
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


def check_proanima(url):
    text = util.query_page(url)

    count_dogs = int(re.findall("[0-9]+ résultats sur ([0-9]+)", text)[0])
    count_adoptés = len(re.findall("Adopté", text))

    count = count_dogs - count_adoptés

    return count


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

    count = len(dogs)

    for dog in dogs:
        if "chat" in str(dog).lower():
            count -= 1

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


def check_spcaroussillon(url):
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

    text = util.query_page(url)

    soup = bs4.BeautifulSoup(text, "lxml")
    nb_dogs = int(soup.find("span", {"class": "type-count"}).text)

    return nb_dogs

