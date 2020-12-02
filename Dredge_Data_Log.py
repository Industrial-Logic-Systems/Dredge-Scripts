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




def log():
    # json_obj = get_serial.json_from_data(get_serial.listen_on_serial())
    json_obj = get_data.json_from_data(tests.get_json())
    logging.debug("Json Object saved to json_obj")

    csv_obj = get_data.generate_csv(json_obj)
    logging.debug("CSV created as csv_obj")

    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))

    file_handeling.write_file(config.json_path, filename + ".json", str(json_obj)+',')
    file_handeling.write_file(config.csv_path, filename + ".csv", str(csv_obj).strip("[]"))

    csv_header = "msg_time, vert_correction, ch_latitude, ch_longitude, ch_depth, ch_heading, slurry_velocity, slurry_density, pump_rpm, vacuum, outlet_psi, comment, msg_start_time, msg_end_time, function_code, comment"
    file_handeling.add_headers(config.csv_path, csv_header)

    freeboard_updater.freeboard("ILS-Dredge", json_obj)
    backup.backup_files(filename)

if __name__ == "__main__":
    while True:
        log()
        logging.info("Sleeping for 5 seconds")
        time.sleep(5)