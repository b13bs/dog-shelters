import requests
from pushbullet import Pushbullet
import re
import pickle
import logging


class MyException(Exception):
    pass


def query_page(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise MyException("HTTP code %s: %s" % (r.status_code, url))

    return re.sub("(<!--|-->)", "", r.text, re.MULTILINE)


def get_prec_values():
    try:
        values = pickle.load(open("stored_values.p", "rb"))
    except FileNotFoundError:
        values = {"animadoption": 0, "aubergezen": 0, "bergerblanclaval" : 0, "spcalaurentides": 0, "nouveaudepart": 0, "spcamontreal": 0, "bergerblancmontreal" : 0}
    return values


def write_prec_values(values):
    pickle.dump(values, open("stored_values.p", "wb"))
    logger = logging.getLogger('adoptions')
    logger.debug("pickled to disk: %s" % values)
            

def is_first_run():
    try:
        with open("stored_values.p"):
            pass
    except FileNotFoundError:
        return True
    else:
        return False
