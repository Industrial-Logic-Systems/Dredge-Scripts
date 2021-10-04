import config

import logging
import datetime
import requests


def checkStatus():
    logging.debug("Reading 'dredge-status.txt' from Github")
    r = requests.get(
        "https://raw.githubusercontent.com/Industrial-Logic-Systems/Dredge-Status/master/dredge-status.txt"
    )
    dredges = r.text.split("\n")

    for i, text in enumerate(dredges):
        dredges[i] = text.rsplit(maxsplit=1)

    dredges = [ele for ele in dredges if ele != []]

    logging.debug(dredges)

    name_found = False

    for dredge_name, date in dredges:
        if config.dredge_name == dredge_name:
            new_date = datetime.date.fromisoformat(date)
            logging.debug(f"Updating run date to {new_date}")
            config.run_until = new_date
            config.save_config()
            name_found = True

    if not name_found:
        logging.warning(
            f"Dredge name '{config.dredge_name}' not in the system"
        )
        return False
    return True


if __name__ == "__main__":
    checkStatus()
