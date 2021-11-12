import config

import serial
import json
import logging
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

import fileHandler


def getJson():
    """Listen on the serial port for data string and convert to JSON"""
    try:
        ser = serial.Serial(config.port, 9600, timeout=20, parity=serial.PARITY_ODD)
        logging.debug("Serial port listening on port {}".format(config.port))
        data = ser.read_until(b"\r").strip(b"\n\r")

        # Decode the serial data
        data = data.decode("ASCII")
        logging.debug(data)
        logging.debug("Data Received")
    except Exception as e:
        logging.error("Serial Exception")
        logging.debug(e, exc_info=True)
        # logging.error("Failed to Receive JSON Serial Data")
        return None

    try:
        json_obj = json.loads(data)
    except Exception as e:
        logging.error("JSON Exception")
        logging.debug(e, exc_info=True)
        try:
            if len(str(data)) != 0:
                fileHandler.write_file(
                    config.json_path + "\\..\\failed", "failed.txt", str(data)
                )
        except Exception as e:
            logging.error("Save Exception")
            logging.debug(e, exc_info=True)
            logging.error("Couldn't save failed string!")
        logging.error("Could not convert received serial data to JSON")
        return None

    return json_obj


def getCSV(json_obj):
    # Uses the json object to make a list that is used for the csv
    csv_obj = []
    # Work Event
    try:
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["msg_time"])
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["work_event"]["vert_correction"]
        )
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_latitude"])
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_longitude"]
        )
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_depth"])
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_heading"])
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["work_event"]["slurry_velocity"]
        )
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["work_event"]["slurry_density"]
        )
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["pump_rpm"])
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["vacuum"])
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["outlet_psi"])
        csv_obj.append(
            json_obj["DQM_Data"]["messages"][0]["work_event"]["comment"].strip()
        )

        # Get Values from Modbus Addresses
        modbusValues = getModbus()
        # add them to csv
        for val in modbusValues:
            csv_obj.append(modbusValues[val])

        events = json_obj["DQM_Data"]["messages"]

        # Non Effective Event
        non_eff = False
        for event in events:
            if "non_eff_event" in event:
                csv_obj.append(event["non_eff_event"]["msg_start_time"])
                csv_obj.append(event["non_eff_event"]["msg_end_time"])
                csv_obj.append(event["non_eff_event"]["function_code"].strip())
                csv_obj.append(event["non_eff_event"]["comment"].strip())
                non_eff = True
                break
        if not non_eff:
            csv_obj.append("")
            csv_obj.append("")
            csv_obj.append("")
            csv_obj.append("")

        # Outfall Event
        outfall = False
        for event in events:
            if "outfall_position" in event:
                csv_obj.append(event["outfall_position"]["msg_time"])
                csv_obj.append(event["outfall_position"]["outfall_location"].strip())
                csv_obj.append(event["outfall_position"]["outfall_latitude"])
                csv_obj.append(event["outfall_position"]["outfall_longitude"])
                csv_obj.append(event["outfall_position"]["outfall_heading"])
                csv_obj.append(event["outfall_position"]["outfall_elevation"])
                csv_obj.append(event["outfall_position"]["comment"].strip())
                outfall = True
                break
        if not outfall:
            csv_obj.append("")
            csv_obj.append("")
            csv_obj.append("")
            csv_obj.append("")
            csv_obj.append("")
            csv_obj.append("")
            csv_obj.append("")

    except Exception as e:
        logging.error("CSV Exception")
        logging.debug(e, exc_info=True)

    return csv_obj, modbusValues


def getModbus():
    SERVER_HOST = config.plc_ip
    SERVER_PORT = 502
    SERVER_U_ID = 1

    c = ModbusClient()

    # uncomment this line to see debug message
    # c.debug(True)

    # define modbus server host, port and unit_id
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)
    c.unit_id(SERVER_U_ID)

    if not c.is_open():
        if not c.open():
            logging.debug(
                "unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT)
            )
            logging.error(f"Could not connect to PLC over IP at {config.plc_ip}")
            return dict()

    values = dict()

    for name in config.modbus:
        address = config.modbus[name]["address"]
        isFloat = config.modbus[name]["float"]
        value = c.read_holding_registers(int(address))
        if isFloat:
            value = utils.get_2comp(value[0], 16) / 100
        else:
            value = value[0]
        values[name] = value
        logging.debug(f"{name.title()}: {str(value)}")

    return values


def sendSerialBit(send):
    SERVER_HOST = config.plc_ip
    SERVER_PORT = 502
    SERVER_U_ID = 1

    c = ModbusClient()

    # uncomment this line to see debug message
    # c.debug(True)

    # define modbus server host, port and unit_id
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)
    c.unit_id(SERVER_U_ID)

    if not c.is_open():
        if not c.open():
            logging.debug(
                "unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT)
            )
            return

    status = c.write_single_coil(0, send)

    if status:
        logging.debug(f"Send Serial bit successfully set to {send}")
    else:
        logging.debug(f"Failed to set Send Serial bit to {send}")


if __name__ == "__main__":
    sendSerialBit(True)
