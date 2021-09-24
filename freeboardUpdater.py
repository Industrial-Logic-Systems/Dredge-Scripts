import dweepy
import logging

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


def freeboard(name, data):
    # Sends out a dweet for freeboard
    try:
        dweepy.dweet_for(name, data)

        events = data["DQM_Data"]["messages"]
        for event in events:
            if "non_eff_event" in event:
                logging.debug("Non-Eff Freeboard")

                msgStart = event["non_eff_event"]["msg_start_time"]
                msgEnd = event["non_eff_event"]["msg_end_time"]
                function_code = event["non_eff_event"]["function_code"].strip()
                comment = event["non_eff_event"]["comment"].strip()

                if (
                    function_code in function_codes_depreciated
                    and function_code not in function_codes
                ):
                    logging.warning("Function code is Depreciated")
                    message = function_codes_depreciated[function_code]
                else:
                    message = function_codes[function_code]

                logging.debug(
                    f'{name + "_non_eff"}, code: {function_code}, message, {message}'
                )
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

    except Exception as e:
        logging.error("Freeboard failed to update")
        logging.debug(e, exc_info=True)
