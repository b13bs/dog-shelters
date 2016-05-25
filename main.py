#!/usr/bin/python3

import sys
from pprint import pprint
import logging
from refuges import *
import util

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

for refuge, nb_prec in prec_values.items():
    try:
        if refuge == "animadoption":
            continue
            nb_chiens = check_animadoption()

        elif refuge == "aubergezen":
            continue
            nb_chiens = check_aubergezen()

        elif refuge == "bergerblancmontreal":
            nb_chiens = check_bergerblanc("montreal")

        elif refuge == "bergerblanclaval":
            nb_chiens = check_bergerblanc("laval")

        elif refuge == "spcalaurentides":
            continue
            nb_chiens = check_spcalaurentides()

        elif refuge == "nouveaudepart":
            continue
            nb_chiens = check_nouveaudepart()

        elif refuge == "spcamontreal":
            continue
            nb_chiens = check_spcamontreal()

        logger.info("%s: nb chiens=%s" % (refuge, nb_chiens))

        if nb_chiens > nb_prec and not is_first_run:
            msg = "NOUVEAU CHIEN à %s! %s -> %s" % (refuge, nb_prec, nb_chiens)
            logger.critical(msg)
            util.notify_me(msg, refuge)

        new_dict[refuge] = nb_chiens

    except util.MyException as e:
        new_dict[refuge] = nb_prec
        logger.error(e)

util.write_prec_values(new_dict)
logger.debug("")

