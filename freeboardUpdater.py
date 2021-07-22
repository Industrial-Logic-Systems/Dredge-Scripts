import dweepy
import logging

# Function codes and their meanings
function_codes = {
    "AGV": "Assisting Grounded Vessels",
    "CCH": "Changing Cutterhead",
    "CCSH": "Clear Cutter Suction",
    "CLPJ": "Change Location Bar",
    "COLL": "Collision",
    "CPPL": "Clear Pump Pipeline",
    "CPR": "Change Impeller",
    "DR": "Dike Repair",
    "FBD": "Fire Boat Drills",
    "HPL": "Handling Pipe Line",
    "HSL": "Handling Swing Line",
    "HSP": "Handling Shore Pipe",
    "LDNE": "Loss Due to Natural Elements",
    "LDPV": "Loss Due to Passing Vessel",
    "LNL": "Transfer to New Location",
    "MISC": "Miscellaneous",
    "MOB": "Mobilization & Demobilization",
    "MSC": "Miscellaneous/Non-pay",
    "OC": "Out of Commission",
    "OR": "Operating Repairs",
    "P": "Preperation",
    "PREP": "Preparation & Making Up Tow",
    "RPL": "Repair Pipeline",
    "SB": "Sounding & Buoying",
    "SBT": "Stand-By Time as Directed",
    "SH": "Sundays-Holidays",
    "TFS": "Taking on Fuel & Supplies",
    "TOW": "Time on Tow",
    "WAP": "Waiting Attendant Plant",
}


def freeboard(name, data):
    # Sends out a dweet for freeboard
    try:
        dweepy.dweet_for(name, data)

        events = data["DQM_Data"]["messages"]
        for event in events:
            if "non_eff_event" in event:
                logging.debug("Non-Eff Freeboard")
                function_code = event["non_eff_event"]["function_code"].strip()
                message = function_codes[function_code]
                logging.debug(
                    f'{name + "_non_eff"}, code: {function_code}, message, {message}'
                )
                dweepy.dweet_for(name + "_non_eff", {"message": message})
    except Exception as e:
        logging.error("Freeboard failed to update")
        logging.debug(e, exc_info=True)
