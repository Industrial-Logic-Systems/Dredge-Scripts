from dredge_logger.config import config

import dweepy
import logging

from dredge_logger import dweet

function_codes = {
    "CCSH": "Clearing Cutter/Suction Head",
    "CESS": "Cessation",
    "CLPJ": "Change Cut/Area",
    "COLL": "Collisions",
    "CPPL": "Clearing Pump & Pipelines",
    "FBD": "Fire Drills",
    "HPL": "Handling Pipelines",
    "HSL": "Handling Swing Lines",
    "LDNE": "Loss Due to Natural Elements",
    "LDPV": "Traffic / Loss Due to Passing Vessel",
    "LNL": "Transferring Plant Between Works / Transfer to New Location",
    "MAJ": "Major Repairs",
    "MISC": "Miscellaneous",
    "MSC": "Miscellaneous / Non-Pay",
    "OR": "Minor Operating Repairs",
    "OSS": "Off Shift / Saturdays",
    "PREP": "Preparation & Making Up Tow",
    "SBT": "Stand By Time (As Directed)",
    "SH": "Sundays & Holidays",
    "SLSW": "Shore Line / Shore Work",
    "TFS": "Taking On Fuel & Supplies",
    "TFWA": "To/From Wharf/Anchorage",
    "WAP": "Waiting for Attendant Plant",
    "WFB": "Waiting For Booster",
    "WFS": "Waiting for Scows",
}
# Function codes and their meanings
function_codes_depreciated = {
    "AGV": "Assisting Grounded Vessels",
    "CCH": "Changing Cutterhead",
    "CPR": "Change Impeller",
    "DR": "Dike Repair",
    "HSP": "Handling Shore Pipe",
    "MOB": "Mobilization & Demobilization",
    "OC": "Out of Commission",
    "P": "Preperation",
    "RPL": "Repair Pipeline",
    "SB": "Sounding & Buoying",
    "TOW": "Time on Tow",
}


def freeboard(name, xml_data, modbus=None):
    # Sends out a dweet for freeboard

    hopper_data = xml_data.find("HOPPER_DATA_RECORD")

    data = {
        "DREDGE_NAME": xml_data.find("DREDGE_NAME").text,
        "DATE_TIME": hopper_data.find("DATE_TIME").text,
        "CONTRACT_NUMBER": hopper_data.find("CONTRACT_NUMBER").text,
        "LOAD_NUMBER": hopper_data.find("LOAD_NUMBER").text,
        "VESSEL_X": hopper_data.find("VESSEL_X").text,
        "VESSEL_Y": hopper_data.find("VESSEL_Y").text,
        "PORT_DRAG_X": hopper_data.find("PORT_DRAG_X").text,
        "PORT_DRAG_Y": hopper_data.find("PORT_DRAG_Y").text,
        "STBD_DRAG_X": hopper_data.find("STBD_DRAG_X").text,
        "STBD_DRAG_Y": hopper_data.find("STBD_DRAG_Y").text,
        "HULL_STATUS": hopper_data.find("HULL_STATUS").text,
        "VESSEL_COURSE": hopper_data.find("VESSEL_COURSE").text,
        "VESSEL_SPEED": hopper_data.find("VESSEL_SPEED").text,
        "VESSEL_HEADING": hopper_data.find("VESSEL_HEADING").text,
        "TIDE": hopper_data.find("TIDE").text,
        "DRAFT_FORE": hopper_data.find("DRAFT_FORE").text,
        "DRAFT_AFT": hopper_data.find("DRAFT_AFT").text,
        "ULLAGE_FORE": hopper_data.find("ULLAGE_FORE").text,
        "ULLAGE_AFT": hopper_data.find("ULLAGE_AFT").text,
        "HOPPER_VOLUME": hopper_data.find("HOPPER_VOLUME").text,
        "DISPLACEMENT": hopper_data.find("DISPLACEMENT").text,
        "EMPTY_DISPLACEMENT": hopper_data.find("EMPTY_DISPLACEMENT").text,
        "DRAGHEAD_DEPTH_PORT": hopper_data.find("DRAGHEAD_DEPTH_PORT").text,
        "DRAGHEAD_DEPTH_STBD": hopper_data.find("DRAGHEAD_DEPTH_STBD").text,
        "PORT_DENSITY": hopper_data.find("PORT_DENSITY").text,
        "STBD_DENSITY": hopper_data.find("STBD_DENSITY").text,
        "PORT_VELOCITY": hopper_data.find("PORT_VELOCITY").text,
        "STBD_VELOCITY": hopper_data.find("STBD_VELOCITY").text,
        "PUMP_RPM_PORT": hopper_data.find("PUMP_RPM_PORT").text,
        "PUMP_RPM_STBD": hopper_data.find("PUMP_RPM_STBD").text,
    }

    try:
        dweepy.dweet_for(name, data)

        if modbus:
            dweepy.dweet_for(name + "_Extra", modbus)

        send_dweet(name, data, modbus)

    except Exception as e:
        logging.error("Freeboard failed to update")
        logging.debug(e, exc_info=True)


def send_dweet(name, data, extra=None):
    # Sends out a dweet with the given name and data
    try:
        dqm_data = {"name": config.vars["dredge_name"], "type": "dqm", "data": data}
        dweet.send_dweet(name, dqm_data)

        if extra:
            extra["timestamp"] = data["DATE_TIME"]
            extra_data = {
                "name": config.vars["dredge_name"],
                "type": "extra",
                "data": extra,
            }
            dweet.send_dweet(name + "_Extra", extra_data)

    except Exception as e:
        logging.error("Dweet Fail to Send")
        logging.debug(e, exc_info=True)
