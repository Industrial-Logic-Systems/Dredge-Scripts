import json
import logging
import xml.etree.ElementTree as ET

import serial
from dredge_logger import fileHandler
from dredge_logger.config import config
from pyModbusTCP import utils
from pyModbusTCP.client import ModbusClient

_logger = logging.getLogger(__name__)


def getSerial():
    """Listen on the serial port for data string"""
    try:
        ser = serial.Serial(config.vars["port"], 9600, timeout=20, parity=serial.PARITY_ODD)
        _logger.debug("Serial port listening on port {}".format(config.vars["port"]))
        data = ser.read_until(b"\r").strip(b"\n\r")

        # Decode the serial data
        data = data.decode("ASCII")
        _logger.debug("Data Received: {}".format(data))
    except Exception as e:
        _logger.error("Serial string not received. Retrying...")
        _logger.debug(e, exc_info=True)
        return None

    return data


def getJSON(data):
    """Convert Raw Serial Data to JSON"""
    try:
        json_obj = json.loads(data)
    except Exception as e:
        _logger.error("JSON Exception")
        _logger.error("Could not convert received serial data to JSON")
        _logger.debug(e, exc_info=True)
        try:
            if len(str(data)) != 0:
                fileHandler.write_file(config.vars["json_path"] + "\\..\\failed", "failed.txt", str(data))
        except Exception as e:
            _logger.debug("Save Exception")
            _logger.debug("Couldn't save failed string!")
            _logger.debug(e, exc_info=True)
        return None

    return json_obj


def getXML(data):
    """Convert Raw Serial Data to JSON"""
    try:
        xml_obj = ET.fromstring(data)
    except Exception as e:
        _logger.error("XML Exception")
        _logger.error("Could not convert received serial data to XML")
        _logger.debug("Data: {}".format(data))
        _logger.debug(e, exc_info=True)
        try:
            if len(str(data)) != 0:
                fileHandler.write_file(config.vars["xml_path"] + "\\..\\failed", "failed.txt", str(data))
        except Exception as e:
            _logger.debug("Save Exception")
            _logger.debug("Couldn't save failed string!")
            _logger.debug(e, exc_info=True)
        return None

    return xml_obj


def getCSV(data_obj, modbus=True):
    # Uses the json object to make a list that is used for the csv
    csv_obj = []

    if config.vars["dredge_type"] == "pipeline":
        # Work Event
        try:
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["msg_time"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["vert_correction"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["ch_latitude"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["ch_longitude"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["ch_depth"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["ch_heading"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["slurry_velocity"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["slurry_density"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["pump_rpm"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["vacuum"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["outlet_psi"])
            csv_obj.append(data_obj["DQM_Data"]["messages"][0]["work_event"]["comment"].strip())
        except Exception as e:
            _logger.error("CSV Exception Parsing Work Event")
            _logger.debug(e, exc_info=True)
            return None, None

    elif config.vars["dredge_type"] == "hopper":
        try:
            csv_obj.append(data_obj.find("DREDGE_NAME").text)

            hopper_data = data_obj.find("HOPPER_DATA_RECORD")
            csv_obj.append(hopper_data.find("DATE_TIME").text)
            csv_obj.append(hopper_data.find("CONTRACT_NUMBER").text)
            csv_obj.append(hopper_data.find("LOAD_NUMBER").text)
            csv_obj.append(hopper_data.find("VESSEL_X").text)
            csv_obj.append(hopper_data.find("VESSEL_Y").text)
            csv_obj.append(hopper_data.find("PORT_DRAG_X").text)
            csv_obj.append(hopper_data.find("PORT_DRAG_Y").text)
            csv_obj.append(hopper_data.find("STBD_DRAG_X").text)
            csv_obj.append(hopper_data.find("STBD_DRAG_Y").text)
            csv_obj.append(hopper_data.find("HULL_STATUS").text)
            csv_obj.append(hopper_data.find("VESSEL_COURSE").text)
            csv_obj.append(hopper_data.find("VESSEL_SPEED").text)
            csv_obj.append(hopper_data.find("VESSEL_HEADING").text)
            csv_obj.append(hopper_data.find("TIDE").text)
            csv_obj.append(hopper_data.find("DRAFT_FORE").text)
            csv_obj.append(hopper_data.find("DRAFT_AFT").text)
            csv_obj.append(hopper_data.find("ULLAGE_FORE").text)
            csv_obj.append(hopper_data.find("ULLAGE_AFT").text)
            csv_obj.append(hopper_data.find("HOPPER_VOLUME").text)
            csv_obj.append(hopper_data.find("DISPLACEMENT").text)
            csv_obj.append(hopper_data.find("EMPTY_DISPLACEMENT").text)
            csv_obj.append(hopper_data.find("DRAGHEAD_DEPTH_PORT").text)
            csv_obj.append(hopper_data.find("DRAGHEAD_DEPTH_STBD").text)
            csv_obj.append(hopper_data.find("PORT_DENSITY").text)
            csv_obj.append(hopper_data.find("STBD_DENSITY").text)
            csv_obj.append(hopper_data.find("PORT_VELOCITY").text)
            csv_obj.append(hopper_data.find("STBD_VELOCITY").text)
            csv_obj.append(hopper_data.find("PUMP_RPM_PORT").text)
            csv_obj.append(hopper_data.find("PUMP_RPM_STBD").text)

        except Exception as e:
            _logger.error("CSV Exception Parsing XML")
            _logger.debug(e, exc_info=True)
            return None, None

    try:
        modbusValues = dict()
        if modbus:
            # Get Values from Modbus Addresses
            modbusValues = getModbus()
            # add them to csv
            for val in modbusValues:
                csv_obj.append(modbusValues[val])

    except Exception as e:
        _logger.error("CSV Exception Parsing Modbus Values")
        _logger.debug(e, exc_info=True)
        return None, None

    if config.vars["dredge_type"] == "pipeline":
        try:
            events = data_obj["DQM_Data"]["messages"]

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
            _logger.error("CSV Exception parsing NE and OF Events")
            _logger.debug(e, exc_info=True)
            return None, None

    return csv_obj, modbusValues


def getModbus():
    SERVER_HOST = config.vars["plc_ip"]
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
            _logger.debug("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
            _logger.error(f"Could not connect to PLC over IP at {config.vars['plc_ip']}")
            return dict()

    values = dict()

    for name in config.vars["modbus"]:
        address = config.vars["modbus"][name]["address"]
        isFloat = config.vars["modbus"][name]["float"]
        value = c.read_holding_registers(int(address), 2)
        value = value[1] << 16 | value[0]
        if isFloat:
            value = utils.get_2comp(value, 32) / 100
        else:
            value = utils.get_2comp(value, 32)
        values[name] = value
        _logger.debug(f"{name.title()}: {str(value)}")

    for name in config.vars["modbus_bits"]:
        address = config.vars["modbus_bits"][name]["address"]
        value = c.read_coils(int(address), 1)
        values[name] = value[0]
        _logger.debug(f"{name.title()}: {str(value)}")

    return values


def sendSerialBit(send):
    SERVER_HOST = config.vars["plc_ip"]
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
            _logger.debug("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
            return

    status = c.write_single_coil(0, send)

    if status:
        _logger.debug(f"Send Serial bit successfully set to {send}")
    else:
        _logger.debug(f"Failed to set Send Serial bit to {send}")


if __name__ == "__main__":
    # sendSerialBit(True)
    getModbus()
