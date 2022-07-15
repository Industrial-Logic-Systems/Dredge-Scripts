import base64
import binascii
import datetime
import logging
import threading

from dredge_logger import backup
from dredge_logger import dataHandler
from dredge_logger import dweetUpdater
from dredge_logger import fileHandler
from dredge_logger.config import config

_logger = logging.getLogger(__name__)


def saveFiles(raw_data, csv_obj):
    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))
    if config.vars["dredge_type"] == "hopper":
        fileHandler.write_file(config.vars["xml_path"], filename + ".xml_bak", str(raw_data))
    else:
        fileHandler.write_file(config.vars["json_path"], filename + ".json", str(raw_data))
    if csv_obj:
        fileHandler.write_file(config.vars["csv_path"], filename + ".csv", csv_obj)
        if config.vars["csv0600"]:
            n = datetime.datetime.now().time()
            if n < datetime.time(6, 0):
                filename = str((datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            fileHandler.write_file(config.vars["csv_path"], filename + "_0600.csv", csv_obj)


def verify_key():
    try:
        decoded = base64.b64decode(config.vars["program_key"]).decode("utf-8")
        date = datetime.datetime.strptime(decoded, "%m/%d/%Y")
        date = date.date()
        if date >= datetime.date.today():
            config.vars["last_check_for_update"] = datetime.date.today()
            config.save_config()
            return [True, False]
        else:
            config.vars["last_check_for_update"] = date
            config.save_config()
    except (binascii.Error, UnicodeDecodeError, ValueError):
        pass
    diff = datetime.date.today() - config.vars["last_check_for_update"]
    if diff >= datetime.timedelta(days=30):
        return [False, True]
    return [False, False]


def log():
    key_result = verify_key()
    if not key_result[0]:
        logging.error("Invalid or Expired Product key. Contact Industrial Logic Systems")
        if key_result[1]:
            dataHandler.sendSerialBit(False)
        return [False, None]
    dataHandler.sendSerialBit(True)

    # Get Serial String
    _logger.debug("Getting Serial String")
    raw_str = dataHandler.getSerial()
    if raw_str is None:
        return [False, None]

    # Convert to XML or JSON Depending on Dredge Type
    if config.vars["dredge_type"] == "pipeline":
        _logger.debug("Converting to JSON")
        data_obj = dataHandler.getJSON(raw_str)
    elif config.vars["dredge_type"] == "hopper":
        _logger.debug("Converting to XML")
        data_obj = dataHandler.getXML(raw_str)

    if not data_obj:
        return [False, None]

    # Create CSV File
    _logger.debug("Creating CSV File")
    csv_obj, modbusValues = dataHandler.getCSV(data_obj)

    # Save Files
    _logger.debug("Saving Files")
    threading.Thread(target=saveFiles, args=(raw_str, csv_obj)).start()

    # Update Freeboard
    if csv_obj:
        _logger.debug("Sending Dweets")
        threading.Thread(
            target=dweetUpdater.freeboard,
            args=(config.vars["freeboard_name"], data_obj, modbusValues),
        ).start()

    # Check if the 0600 file needs to be emailed
    if config.vars["csv0600"]:
        if datetime.datetime.now().time() > datetime.time(6, 0) and not config.vars["csv0600_saved"]:
            filename = str((datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            _logger.debug(f"Backing up csv_0600 for the day: {filename}")
            filename += "_0600"
            threading.Thread(target=backup.backup_files, args=(str(filename), True)).start()
            config.vars["csv0600_saved"] = True
            config.save_config()

    # Backup Files Once a Day
    old_time = config.vars["last_save_date"]  # Date when the loop last ran
    cur_time = datetime.date.today()  # Current date
    if old_time < cur_time:
        # If old date is different from the current date backup the files
        _logger.debug(f"Backing up files for the day: {old_time}")
        threading.Thread(target=backup.backup_files, args=(str(old_time),)).start()
        config.vars["last_save_date"] = cur_time
        config.vars["csv0600_saved"] = False
        config.save_config()

    return_data = {}
    if config.vars["dredge_type"] == "hopper":
        hopper_data = data_obj.find("HOPPER_DATA_RECORD")
        return_data = {
            "msg_time": hopper_data.find("DATE_TIME").text,
            "latitude": hopper_data.find("VESSEL_X").text,
            "longitude": hopper_data.find("VESSEL_Y").text,
        }
    else:
        return_data = {
            "msg_time": data_obj["DQM_Data"]["messages"][0]["work_event"]["msg_time"],
            "latitude": data_obj["DQM_Data"]["messages"][0]["work_event"]["ch_latitude"],
            "longitude": data_obj["DQM_Data"]["messages"][0]["work_event"]["ch_longitude"],
        }

    return [True, return_data]


if __name__ == "__main__":
    while True:
        log()
