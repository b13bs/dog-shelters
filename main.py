#!/usr/bin/env python3

import sys
import logging
import util
import os
from shelters import *


if __name__ == "__main__":
    logger = logging.getLogger('adoptions')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("%s.log" % os.path.splitext(os.path.abspath(__file__))[0])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    is_first_run = util.is_first_run()
    logger.debug("is first run: %s" % is_first_run)

    prec_values = util.get_prec_values()
    new_dict = {}

    for shelter, previous_value in prec_values.items():
        try:
            url = util.get_shelter_url(shelter)
            if shelter == "animadoption":
                present_value = check_animadoption(url)

            elif shelter == "aubergezen":
                present_value = check_aubergezen(url)

            elif shelter == "bergerblancmontreal":
                present_value = check_bergerblanc("montreal", url)

            elif shelter == "bergerblanclaval":
                present_value = check_bergerblanc("laval", url)

            elif shelter == "spcalaurentides":
                present_value = check_spcalaurentides(url)

            elif shelter == "nouveaudepart":
                present_value = check_nouveaudepart(url)

            elif shelter == "animatch":
                present_value = check_animatch(url)

            elif shelter == "rivesud":
                present_value = check_rivesud(url)

            elif shelter == "refugemagoo":
                present_value = check_refugemagoo(url)

            elif shelter == "cabanealiam":
                continue
                present_value = check_cabanealiam(url)

            elif shelter == "rosieanimaladoption":
                present_value = check_rosieanimaladoption(url)

            elif shelter == "spcamontreal":
                continue
                # present_value = check_spcamontreal()

            logger.info("%s: nb dogs=%s" % (shelter, present_value))

            if present_value > previous_value and not is_first_run:
                title = "Refuge %s" % shelter
                msg = "%s nouveaux chiens\n%s" % ((present_value - previous_value), url)
                logger.critical(msg)
                util.notify_me(title, msg)

            new_dict[shelter] = present_value

        except util.MyException as e:
            new_dict[shelter] = previous_value
            logger.error(e)
            util.notify_me("Adoptions", e)

    util.write_prec_values(new_dict)
    logger.debug("")
