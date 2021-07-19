import config

import threading
import logging
import datetime

import dataHandler
import fileHandler
import freeboardUpdater
import backup


def saveFiles(json_data, csv_data):
    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))
    fileHandler.write_file(config.json_path, filename + ".json", str(json_data))
    fileHandler.write_file(
        config.csv_path, filename + ".csv", str(csv_data).strip("[]")
    )


def log():
    # Get JSON Data
    logging.debug("Getting JSON Data")
    json_data = dataHandler.getJson()

    if not json_data:
        logging.warning("Failed to Retrieve JSON String")
        return [False, None]

    # Get CSV Data
    logging.debug("Getting CSV Data")
    csv_data = dataHandler.getCSV(json_data)

    # Save JSON and CSV Files
    logging.debug("Saving Files")
    threading.Thread(target=saveFiles, args=(json_data, csv_data)).start()

    # Update Freeboard
    logging.debug("Updating Freeboard")
    threading.Thread(
        target=freeboardUpdater.freeboard, args=(config.freeboard_name, json_data)
    ).start()

    # Backup Files Once a Day
    old_time = config.last_save_date  # Date when the loop last ran
    cur_time = datetime.date.today()  # Current date
    if old_time < cur_time:
        # If old date is different from the current date backup the files
        logging.debug("Backing up files for the day: {}".format(old_time))
        threading.Thread(target=backup.backup_files, args=(str(old_time),)).start()
        config.last_save_date = cur_time
        config.save_config()

    return [True, json_data]


if __name__ == "__main__":
    while True:
        log()
