import json
import random
import datetime
import time
import logging

function_codes = [
    "AGV",
    "CCH",
    "CCSH",
    "CLPJ",
    "COLL",
    "CPPL",
    "CPR",
    "DR",
    "FBD",
    "HPL",
    "HSL",
    "HSP",
    "LDNE",
    "LDPV",
    "LNL",
    "MISC",
    "MOB",
    "MSC",
    "OC",
    "OR",
    "P",
    "PREP",
    "RPL",
    "SB",
    "SBT",
    "SH",
    "TFS",
    "TOW",
    "WAP",
]


def get_json():
    # Generate random Values for all json objects
    msg_time = str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
    vert_correction = round(random.uniform(0, 100), 2)
    ch_latitude = round(random.uniform(-85, 85), 6)
    ch_longitude = round(random.uniform(-180, 180), 6)
    ch_depth = round(random.uniform(0, 100), 2)
    ch_heading = random.randint(0, 359)
    slurry_velocity = round(random.uniform(0, 100), 2)
    slurry_density = round(random.uniform(0, 100), 2)
    pump_rpm = random.randint(0, 1000)
    vacuum = round(random.uniform(0, 100), 2)
    outlet_psi = round(random.uniform(0, 100), 2)
    comment = "Comment"

    # Create the dictionary from the variables
    json_dict = {
        "DQM_Data": {
            "messages": [
                {
                    "work_event": {
                        "msg_time": msg_time,
                        "vert_correction": vert_correction,
                        "ch_latitude": ch_latitude,
                        "ch_longitude": ch_longitude,
                        "ch_depth": ch_depth,
                        "ch_heading": ch_heading,
                        "slurry_velocity": slurry_velocity,
                        "slurry_density": slurry_density,
                        "pump_rpm": pump_rpm,
                        "vacuum": vacuum,
                        "outlet_psi": outlet_psi,
                        "comment": comment,
                    }
                }
            ]
        }
    }

    # Turn the dict into a json object
    j = json.dumps(json_dict)

    logging.debug("Sleeping for 10 seconds to simulate getting serial input")
    time.sleep(10)

    return j


def get_json_non_eff():
    # Generate random Values for all json objects
    msg_time = str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
    vert_correction = round(random.uniform(0, 100), 2)
    ch_latitude = round(random.uniform(-85, 85), 6)
    ch_longitude = round(random.uniform(-180, 180), 6)
    ch_depth = round(random.uniform(0, 100), 2)
    ch_heading = random.randint(0, 359)
    slurry_velocity = round(random.uniform(0, 100), 2)
    slurry_density = round(random.uniform(0, 100), 2)
    pump_rpm = random.randint(0, 1000)
    vacuum = round(random.uniform(0, 100), 2)
    outlet_psi = round(random.uniform(0, 100), 2)
    comment = "Comment"

    # Non Eff
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(hours=1)
    msg_start_time = str(start_time.strftime("%m-%d-%Y %H:%M:%S"))
    msg_end_time = str(end_time.strftime("%m-%d-%Y %H:%M:%S"))
    function_code = random.choice(function_codes)
    comment_nef = "Comment"

    # Create the dictionary from the variables
    json_dict = {
        "DQM_Data": {
            "messages": [
                {
                    "work_event": {
                        "msg_time": msg_time,
                        "vert_correction": vert_correction,
                        "ch_latitude": ch_latitude,
                        "ch_longitude": ch_longitude,
                        "ch_depth": ch_depth,
                        "ch_heading": ch_heading,
                        "slurry_velocity": slurry_velocity,
                        "slurry_density": slurry_density,
                        "pump_rpm": pump_rpm,
                        "vacuum": vacuum,
                        "outlet_psi": outlet_psi,
                        "comment": comment,
                    },
                    "non_eff_event": {
                        "msg_start_time": msg_start_time,
                        "msg_end_time": msg_end_time,
                        "function_code": function_code,
                        "comment": comment_nef,
                    },
                }
            ]
        }
    }

    # Turn the dict into a json object
    j = json.dumps(json_dict)

    logging.debug("Sleeping for 10 seconds to simulate getting serial input")
    time.sleep(10)

    return j
