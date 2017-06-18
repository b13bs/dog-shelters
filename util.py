import requests
from pushbullet import Pushbullet
import re
import pickle
import logging
import sys
import os
import config
import facebook

project_path = os.path.dirname(os.path.abspath(__file__))

class MyException(Exception):
    pass


def query_facebook_album(album_id):
    graph = facebook.GraphAPI(config.facebook_token)
    obj = graph.get_object("%s?fields=count" % album_id)

    return obj


def query_page(url):
    r = requests.get(url.strip())
    if r.status_code != 200:
        raise MyException("HTTP code %s: %s" % (r.status_code, url))

    return re.sub("(<!--|-->)", "", r.text, re.MULTILINE)


def get_prec_values():
    try:
        values = pickle.load(open(os.path.join(project_path, "stored_values.p"), "rb"))

    except FileNotFoundError:
        values = {"animadoption": 0, "aubergezen": 0, "bergerblanclaval": 0, "spcalaurentides": 0, "nouveaudepart": 0, "spcamontreal": 0, "bergerblancmontreal" : 0, "animatch": 0, "rivesud": 0, "cabanealiam": 0}
    return values


def write_prec_values(values):
    pickle.dump(values, open(os.path.join(project_path, "stored_values.p"), "wb"))
    logger = logging.getLogger('adoptions')
    logger.debug("pickled to disk: %s" % values)
            

def is_first_run():
    try:
        with open(os.path.join(project_path, "stored_values.p")):
            pass
    except FileNotFoundError:
        return True
    else:
        return False


def get_shelter_url(shelter_searched):
    with open(os.path.join(project_path, "urls.txt")) as f:
        for line in f:
            shelter, url = line.split(" ")
            if shelter_searched in shelter:
                return url


def notify_me(title, body):
    pb = Pushbullet(config.pushbullet_key)
    push = pb.push_note(title, body)
    logger = logging.getLogger('adoptions')
    logger.critical(push)
