#!/usr/bin/python3

import sys
import logging
import util
from shelters import *
from pprint import pprint

### Create your module for api key and notification method
try:
    import secrets
except ImportError:
    print("Comment import line or create secrets.py module")
    sys.exit()

logger = logging.getLogger('adoptions')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('adoptions.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

is_first_run = util.is_first_run()
logger.debug("is first run: %s" % is_first_run)

prec_values = util.get_prec_values()
new_dict = {}

for shelter, nb_prev in prec_values.items():
    try:
        if shelter == "animadoption":
            nb_dogs = check_animadoption()

        elif shelter == "aubergezen":
            nb_dogs = check_aubergezen()

        elif shelter == "bergerblancmontreal":
            nb_dogs = check_bergerblanc("montreal")

        elif shelter == "bergerblanclaval":
            nb_dogs = check_bergerblanc("laval")

        elif shelter == "spcalaurentides":
            nb_dogs = check_spcalaurentides()

        elif shelter == "nouveaudepart":
            nb_dogs = check_nouveaudepart()

        elif shelter == "spcamontreal":
            continue
            nb_dogs = check_spcamontreal()

        logger.info("%s: nb dogs=%s" % (shelter, nb_dogs))

        if nb_dogs > nb_prev and not is_first_run:
            msg = " à %s! %s -> %s" % (shelter, nb_prev, nb_dogs)
            logger.critical(msg)
            secrets.notify_me(msg, shelter)

        new_dict[shelter] = nb_dogs

    except util.MyException as e:
        new_dict[shelter] = nb_prev
        logger.error(e)
        secrets.notify_me("Adoptions", e)

util.write_prec_values(new_dict)
logger.debug("")

