import json
import random
import datetime
import time
import logging


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
