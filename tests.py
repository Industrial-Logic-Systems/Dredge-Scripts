import json
import random
import datetime

def get_json():
    msg_time = str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
    vert_correction = round(random.uniform(0, 100), 2)
    ch_latitude = round(random.uniform(-90, 90), 6)
    ch_longitude = round(random.uniform(-180, 80), 6)
    ch_depth = round(random.uniform(0, 100), 2)
    ch_heading = random.randint(0, 359)
    slurry_velocity = round(random.uniform(0, 100), 2)
    slurry_density = round(random.uniform(0, 100), 2)
    pump_rpm = random.randint(0, 1000)
    vacuum = round(random.uniform(0, 100), 2)
    outlet_psi = round(random.uniform(0, 100), 2)
    comment = "Comment"

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

    j = json.dumps(json_dict)
    return j
