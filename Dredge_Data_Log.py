"""
ToDo:
    Send Files to email and remote server
"""
import config

import threading
import logging
import datetime
import time

import freeboard_updater
import get_data
import file_handeling
import backup

import tests

# Create the cur_time variable that is used to tell when to backup files
cur_time = datetime.datetime.today().strftime("%Y-%m-%d")


def log():
    """The Main Loop of the program, this will read the data from serial
    and then take all the required steps to handle the data"""

    # json_obj = get_data.json_from_data(get_data.listen_on_serial())
    try:
        # Get the JSON object from the string sent over serial
        json_string = get_data.listen_on_serial()
        json_obj = get_data.json_from_data(json_string)
        # json_obj = get_data.json_from_data(tests.get_json_non_eff()) # Used for testing purposes
        # json_obj = get_data.json_from_data(tests.get_json()) # Used for testing purposes
        logging.debug("Json Object saved to json_obj")
    except:
        try:
            file_handeling.write_file("C:/Users/ILS_Data/Desktop/failed", "failed.txt", str(json_string))
        except:
            logging.error("Couldn't save failed string!")
        logging.error("There was a problem gettings the Serial String, Trying Again")
        return
    else:
        # Create a list from the json object that will be saved as a CSV
        csv_obj = get_data.generate_csv(json_obj)
        logging.debug("CSV created as csv_obj")

        # Create the filename for the CSV and JSON files by getting the current date I.E. ("2020-12-02")
        filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))

        # Write the JSON and CSV files
        file_handeling.write_file(config.json_path, filename + ".json", str(json_obj))
        file_handeling.write_file(
            config.csv_path, filename + ".csv", str(csv_obj).strip("[]")
        )

        # Go through all CSV files and make sure they have a header
        csv_header = "msg_time, vert_correction, ch_latitude, ch_longitude, ch_depth, ch_heading, slurry_velocity, slurry_density, pump_rpm, vacuum, outlet_psi, comment, msg_start_time, msg_end_time, function_code, comment, msg_time, outfall_location, outfall_latitude, outfall_longitude, outfall_heading, outfall_elevation, comment"
        file_handeling.add_headers(config.csv_path, csv_header)

        try:
            # Update the freeboard with new information
            freeboard_updater.freeboard("ILS-Dredge", json_obj)
        except:
            logging.error("Failed to updated freeboard!")

        # Backup the files once a day
        global cur_time
        old_time = cur_time  # Date when the loop last ran
        cur_time = datetime.datetime.today().strftime("%Y-%m-%d")  # Current date
        if old_time < cur_time:
            # If old date is different from the current date backup the files
            logging.debug("Backing up files for the day: {}".format(old_time))
            threading.Thread(target=backup.backup_files, args=(str(old_time),)).start()
            # backup.backup_files(str(old_time))


if __name__ == "__main__":
    while True:
        log()
