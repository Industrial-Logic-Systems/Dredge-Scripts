import config

import threading
import logging
import datetime

import dataHandler
import fileHandler
import dweetUpdater
import backup
import dredgeStatus


def saveFiles(json_data, csv_data):
    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))
    fileHandler.write_file(config.json_path, filename + ".json", str(json_data))
    fileHandler.write_file(
        config.csv_path, filename + ".csv", str(csv_data).strip("[]")
    )
    if config.csv0600:
        n = datetime.datetime.now().time()
        if n < datetime.time(6, 0):
            filename = str(
                (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                )
            )
        fileHandler.write_file(
            config.csv_path, filename + "_0600.csv", str(csv_data).strip("[]")
        )


def updateRunUntil():
    try:
        status = dredgeStatus.checkStatus()
        if status == True:
            config.last_run_update_date = datetime.date.today()
            config.save_config()
    except Exception as e:
        logging.error("Failed to update run until date")
        logging.error(f"Error Exception: {e}")


def log():
    # Update Run Until once a day
    # old_date = config.last_run_update_date  # Date when last successful update happened
    # cur_date = datetime.date.today()  # Current date
    # if old_date < cur_date:
    #    # If old date is different from the current date backup the files
    #    logging.debug("Attempting to update run until date")
    #    threading.Thread(target=updateRunUntil).start()

    # if datetime.date.today() > config.run_until:
    #    logging.warning("Runtime expired. Contact ILS Automation")
    #    dataHandler.sendSerialBit(False)
    #    threading.Thread(target=updateRunUntil).start()
    #    return [False, None]

    # dataHandler.sendSerialBit(True)

    # Get JSON Data
    logging.debug("Getting JSON Data")
    json_data = dataHandler.getJson()

    if not json_data:
        logging.error("Failed to Retrieve JSON String")
        return [False, None]

    # Get CSV Data
    logging.debug("Getting CSV Data")
    csv_data, modbusValues = dataHandler.getCSV(json_data)

    # Save JSON and CSV Files
    logging.debug("Saving Files")
    threading.Thread(target=saveFiles, args=(json_data, csv_data)).start()

    # Update Freeboard
    logging.debug("Sending Dweets")
    threading.Thread(
        target=dweetUpdater.freeboard,
        args=(config.freeboard_name, json_data, modbusValues),
    ).start()

    # Check if the 0600 file needs to be emailed
    if config.csv0600:
        if (
            datetime.datetime.now().time() > datetime.time(6, 0)
            and not config.csv0600_saved
        ):
            filename = str(
                (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                )
            )
            logging.debug("Backing up csv_0600 for the day: {}".format(filename))
            filename += "_0600"
            threading.Thread(
                target=backup.backup_files, args=(str(filename), True)
            ).start()
            config.csv0600_saved = True
            config.save_config()

    # Backup Files Once a Day
    old_time = config.last_save_date  # Date when the loop last ran
    cur_time = datetime.date.today()  # Current date
    if old_time < cur_time:
        # If old date is different from the current date backup the files
        logging.debug("Backing up files for the day: {}".format(old_time))
        threading.Thread(target=backup.backup_files, args=(str(old_time),)).start()
        config.last_save_date = cur_time
        config.csv0600_saved = False
        config.save_config()

    return [True, json_data]


if __name__ == "__main__":
    while True:
        log()
