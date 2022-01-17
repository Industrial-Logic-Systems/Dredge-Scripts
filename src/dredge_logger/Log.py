from dredge_logger.config import config

import datetime
import logging
import threading

from dredge_logger import backup
from dredge_logger import dataHandler
from dredge_logger import dweetUpdater
from dredge_logger import fileHandler


def saveFiles(xml_data, csv_data):
    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))
    fileHandler.write_file(config.vars["xml_path"], filename + ".xml", str(xml_data))
    if csv_data:
        fileHandler.write_file(config.vars["csv_path"], filename + ".csv", csv_data)
        if config.vars["csv0600"]:
            n = datetime.datetime.now().time()
            if n < datetime.time(6, 0):
                filename = str((datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            fileHandler.write_file(config.vars["csv_path"], filename + "_0600.csv", csv_data)


def log():
    # Get JSON Data
    logging.debug("Getting XML Data")
    xml_data = dataHandler.getXML()

    if not xml_data:
        logging.error("Failed to Retrieve XML String")
        return [False, None]

    # Get CSV Data
    logging.debug("Getting CSV Data")
    csv_data, modbusValues = dataHandler.getCSV(xml_data)

    # Save JSON and CSV Files
    logging.debug("Saving Files")
    threading.Thread(target=saveFiles, args=(xml_data, csv_data)).start()

    # Update Freeboard
    if csv_data:
        logging.debug("Sending Dweets")
        threading.Thread(
            target=dweetUpdater.freeboard,
            args=(config.vars["freeboard_name"], xml_data, modbusValues),
        ).start()

    # Check if the 0600 file needs to be emailed
    if config.vars["csv0600"]:
        if datetime.datetime.now().time() > datetime.time(6, 0) and not config.vars["csv0600_saved"]:
            filename = str((datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            logging.debug("Backing up csv_0600 for the day: {}".format(filename))
            filename += "_0600"
            threading.Thread(target=backup.backup_files, args=(str(filename), True)).start()
            config.vars["csv0600_saved"] = True
            config.save_config()

    # Backup Files Once a Day
    old_time = config.vars["last_save_date"]  # Date when the loop last ran
    cur_time = datetime.date.today()  # Current date
    if old_time < cur_time:
        # If old date is different from the current date backup the files
        logging.debug("Backing up files for the day: {}".format(old_time))
        threading.Thread(target=backup.backup_files, args=(str(old_time),)).start()
        config.vars["last_save_date"] = cur_time
        config.vars["csv0600_saved"] = False
        config.save_config()

    return [True, xml_data]


if __name__ == "__main__":
    while True:
        log()
