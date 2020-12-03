"""
ToDo:
    Send Files to email and remote server
"""
import config

import logging
import datetime
import time

import freeboard_updater
import get_data
import file_handeling
import backup

import tests

cur_time = datetime.datetime.today().strftime("%Y-%m-%d")


def log():
    # Get the JSON object from the string sent over serial
    # json_obj = get_serial.json_from_data(get_serial.listen_on_serial())
    json_obj = get_data.json_from_data(tests.get_json())
    logging.debug("Json Object saved to json_obj")

    # Create a list from the json object that will be saved as a CSV
    csv_obj = get_data.generate_csv(json_obj)
    logging.debug("CSV created as csv_obj")

    # Create the filename for the CSV and JSON files by getting the current date I.E. ("2020-12-02")
    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))

    # Write the JSON and CSV files
    file_handeling.write_file(config.json_path, filename + ".json", str(json_obj) + ",")
    file_handeling.write_file(
        config.csv_path, filename + ".csv", str(csv_obj).strip("[]")
    )

    # Go through all CSV files and make sure they have a header
    csv_header = "msg_time, vert_correction, ch_latitude, ch_longitude, ch_depth, ch_heading, slurry_velocity, slurry_density, pump_rpm, vacuum, outlet_psi, comment, msg_start_time, msg_end_time, function_code, comment"
    file_handeling.add_headers(config.csv_path, csv_header)

    # Update the freeboard with new information
    freeboard_updater.freeboard("ILS-Dredge", json_obj)

    # Backup the files once a day
    global cur_time
    old_time = cur_time
    cur_time = datetime.datetime.today().strftime("%Y-%m-%d")
    if old_time < cur_time:
        logging.debug("Backing up files for the day: {}".format(old_time))
        backup.backup_files(str(old_time))


if __name__ == "__main__":
    while True:
        log()