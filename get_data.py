import serial
import json
import logging

import config
import getModBusTags


def listen_on_serial():
    """ Listen on the serial port for data string """
    ser = serial.Serial(config.port_name, 9600, timeout=20,
                        parity=serial.PARITY_ODD)
    logging.debug("Serial port listening on port {}".format(config.port_name))
    data = ser.read_until(b"\r").strip(b"\n\r")
    # Decode the serial data
    data = data.decode("ASCII")
    logging.debug(data)
    logging.debug("Data Received")
    return data


def json_from_data(data):
    # Takes a dict object and turn it into a json object
    json_obj = json.loads(data)
    return json_obj


def generate_csv(json_obj):
    # Uses the json object to make a list that is used for the csv
    csv_obj = []
    # Work Event
    csv_obj.append(json_obj["DQM_Data"]["messages"]
                   [0]["work_event"]["msg_time"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]
                   ["work_event"]["vert_correction"])
    csv_obj.append(json_obj["DQM_Data"]["messages"]
                   [0]["work_event"]["ch_latitude"])
    csv_obj.append(json_obj["DQM_Data"]["messages"]
                   [0]["work_event"]["ch_longitude"])
    csv_obj.append(json_obj["DQM_Data"]["messages"]
                   [0]["work_event"]["ch_depth"])
    csv_obj.append(json_obj["DQM_Data"]["messages"]
                   [0]["work_event"]["ch_heading"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]
                   ["work_event"]["slurry_velocity"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]
                   ["work_event"]["slurry_density"])
    csv_obj.append(json_obj["DQM_Data"]["messages"]
                   [0]["work_event"]["pump_rpm"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["vacuum"])
    csv_obj.append(json_obj["DQM_Data"]["messages"]
                   [0]["work_event"]["outlet_psi"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]
                   ["work_event"]["comment"].strip())

    # Extra Info Offset & ROT

    # Get offset and rot
    offset, rot = getModBusTags.getModbus()
    # add them to csv
    csv_obj.append(offset)
    csv_obj.append(rot)

    # Non Effective Event
    if "non_eff_event" in json_obj["DQM_Data"]["messages"][0]:
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["msg_start_time"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["msg_end_time"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["function_code"].strip()
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["comment"].strip()
        )
    else:
        csv_obj.append("")
        csv_obj.append("")
        csv_obj.append("")
        csv_obj.append("")

    # Non Effective Event
    if "outfall_position" in json_obj["DQM_Data"]["messages"][0]:
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["outfall_position"]["msg_time"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["outfall_position"][
                "outfall_location"
            ].strip()
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["outfall_position"]["outfall_latitude"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["outfall_position"]["outfall_longitude"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["outfall_position"]["outfall_heading"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["outfall_position"]["outfall_elevation"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["outfall_position"]["comment"].strip()
        )
    else:
        csv_obj.append("")
        csv_obj.append("")
        csv_obj.append("")
        csv_obj.append("")
        csv_obj.append("")
        csv_obj.append("")
        csv_obj.append("")

    return csv_obj
