import requests
import bs4
import logging
import sys
from pprint import pprint
import util

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
    images = soup("div",attrs={ "class": "Result"})
    count = 0
    for image in images:
        if "Adopted" in str(image):
            continue
        else:
            count += 1

    return count

def check_spcalaurentides():
    return 0

def check_nouveaudepart():
    return 0

def check_spcamontreal():
    return 0


