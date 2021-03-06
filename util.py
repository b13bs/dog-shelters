import requests
import re
import pickle
import logging
import os
import configs.config as config
import facebook
import slackweb
from random import choice


project_path = os.path.dirname(os.path.abspath(__file__))


class MyException(Exception):
    pass

def query_facebook_album(album_id):
    try:
        graph = facebook.GraphAPI(config.facebook_token)
        obj = graph.get_object("%s?fields=count" % album_id)
        return obj
    except Exception as e:
        raise MyException(e)


def query_page(url):
    r = requests.get(url.strip())
    if r.status_code != 200:
        raise MyException("HTTP code %s: %s" % (r.status_code, url))

    return re.sub("(<!--|-->)", "", r.text, re.MULTILINE)


def get_prec_values():
    try:
        values = pickle.load(open(os.path.join(project_path, "stored_values.p"), "rb"))

    except FileNotFoundError:
        values = {}
        with open(os.path.join(project_path, "configs", "urls.txt")) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    shelter = line.split(" ")[0]
                    values[shelter] = 0
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
    with open(os.path.join(project_path, "configs", "urls.txt")) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                shelter, url = line.split(" ")
                if shelter_searched in shelter:
                    return url


def notify_me(title, body):
    emojis = [":proxy1:",":proxy10:",":proxy11:",":proxy2:",":proxy3:",":proxy4:",":proxy5:",":proxy6:",":proxy7:",":proxy8:",":proxy9:",":daisy1:",":daisy2:",":maggie1:",":maggie2:", ":pixelle1:", "pixelle2:", ":zoe1:", ":zoe2:"]
    slack = slackweb.Slack(url=config.slack_url)
    msg = "%s - %s" % (title, body)
    #slack.notify(text=msg, channel="#refuge-chien", username="dog-shelters", icon_emoji=choice(emojis))
