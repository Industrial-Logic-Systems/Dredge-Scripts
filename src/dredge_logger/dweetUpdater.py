import logging

import dweepy
from dredge_logger import dweet
from dredge_logger.config import config

_logger = logging.getLogger(__name__)

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


def xml_to_json(xml):
    hopper_data = xml.find("HOPPER_DATA_RECORD")
    data = {
        "DREDGE_NAME": xml.find("DREDGE_NAME").text,
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
    return data


def freeboard(name, data, modbus=None):
    # Sends out a dweet for freeboard

    if config.vars["dredge_type"] == "hopper":
        data = xml_to_json(data)
        try:
            send_dweet(name, data, modbus)

            dweepy.dweet_for(name, data)

            if modbus:
                dweepy.dweet_for(name + "_Extra", modbus)

        except Exception as e:
            _logger.error("Freeboard failed to update")
            _logger.debug(e, exc_info=True)
    else:
        try:
            send_dweet(name, data, modbus)

            dweepy.dweet_for(name, data)

            events = data["DQM_Data"]["messages"]
            for event in events:
                if "non_eff_event" in event:
                    _logger.debug("Non-Eff Freeboard")

                    msgStart = event["non_eff_event"]["msg_start_time"]
                    msgEnd = event["non_eff_event"]["msg_end_time"]
                    function_code = event["non_eff_event"]["function_code"].strip()
                    comment = event["non_eff_event"]["comment"].strip()

                    if function_code in function_codes_depreciated and function_code not in function_codes:
                        _logger.warning("Function code is Depreciated")
                        message = function_codes_depreciated[function_code]
                    else:
                        message = function_codes[function_code]

                    _logger.debug(f'{name + "_non_eff"}, code: {function_code}, message, {message}')
                    dweepy.dweet_for(
                        name + "_non_eff",
                        {
                            "msgStart": msgStart,
                            "msgEnd": msgEnd,
                            "function_code": function_code,
                            "comment": comment,
                            "message": message,
                        },
                    )

            if modbus:
                dweepy.dweet_for(name + "_Extra", modbus)

        except Exception as e:
            _logger.error("Freeboard failed to update")
            _logger.debug(e, exc_info=True)


def send_dweet(name, data, extra=None):
    # Sends out a dweet with the given name and data
    if config.vars["dredge_type"] == "hopper":
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
            _logger.error("Dweet Fail to Send")
            _logger.debug(e, exc_info=True)
    else:
        try:
            dqm_data = {"name": config.vars["dredge_name"], "type": "dqm", "data": data}
            dweet.send_dweet(name, dqm_data)

            events = data["DQM_Data"]["messages"]
            for event in events:
                if "non_eff_event" in event:
                    _logger.debug("Non-Eff Freeboard")

                    msgStart = event["non_eff_event"]["msg_start_time"]
                    msgEnd = event["non_eff_event"]["msg_end_time"]
                    function_code = event["non_eff_event"]["function_code"].strip()
                    comment = event["non_eff_event"]["comment"].strip()

                    if function_code in function_codes_depreciated and function_code not in function_codes:
                        _logger.warning("Function code is Depreciated")
                        message = function_codes_depreciated[function_code]
                    else:
                        message = function_codes[function_code]

                    _logger.debug(f'{name + "_non_eff"}, code: {function_code}, message, {message}')
                    non_eff_data = {
                        "name": config.vars["dredge_name"],
                        "type": "non_eff",
                        "data": {
                            "msgStart": msgStart,
                            "msgEnd": msgEnd,
                            "function_code": function_code,
                            "comment": comment,
                            "message": message,
                        },
                    }
                    dweet.send_dweet(name + "_non_eff", non_eff_data)

            if extra:
                extra["timestamp"] = data["DQM_Data"]["messages"][0]["work_event"]["msg_time"]
                extra_data = {
                    "name": config.vars["dredge_name"],
                    "type": "extra",
                    "data": extra,
                }
                dweet.send_dweet(name + "_Extra", extra_data)

        except Exception as e:
            _logger.error("Dweet Fail to Send")
            _logger.debug(e, exc_info=True)


if __name__ == "__main__":
    send_dweet(
        "ILS-Dredge",
        {
            "DQM_Data": {
                "messages": [
                    {
                        "work_event": {
                            "msg_time": "2022-01-21 09:28:12",
                            "vert_correction": 3.82,
                            "ch_latitude": 33.860394,
                            "ch_longitude": -117.819382,
                            "ch_depth": -94.15,
                            "ch_heading": 252,
                            "slurry_velocity": 10.36,
                            "slurry_density": 1.21,
                            "pump_rpm": 0,
                            "vacuum": -0.37,
                            "outlet_psi": 0.0,
                            "comment": "comment             ",
                        }
                    }
                ]
            }
        },
        {"offset": 0.0, "rot": 0.0, "heading": 0, "non_eff": True, "vacuum_break": False},
    )
