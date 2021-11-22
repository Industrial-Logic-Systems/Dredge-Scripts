from dotenv import load_dotenv
from pathlib import Path
import datetime
import json
import logging
import logging.handlers
import os
import shutil

"""
config.json has the following information:
    Com Port
    Json Path
    CSV Path
    Email List
    PLC IP
    Email To Send With
    Dredge Name
    List of Modbus Addresses with Name and type
"""

# Get the directory where the script is located
proj_dir = os.path.dirname(__file__)


def save_env(env):
    with open(proj_dir + "/.env", "w") as f:
        if env["user"] is not None:
            f.write("DWEET_USER=" + env["user"] + "\n")
        if env["pass"] is not None:
            f.write("DWEET_PASS=" + env["pass"] + "\n")
        if env["key"] is not None:
            f.write("MASTER_KEY=" + env["key"] + "\n")


def load_env():
    if os.path.exists(proj_dir + "/.env"):
        dotenv_path = Path(proj_dir + "/.env")
        load_dotenv(dotenv_path=dotenv_path)
    env = {}
    env["user"] = os.getenv("DWEET_USER", None)
    env["pass"] = os.getenv("DWEET_PASS", None)
    env["key"] = os.getenv("MASTER_KEY", None)
    return env


def checkPath(path):
    """Will take a path, and remove the last directory, then check if it exists.
    If the path exists, then it returns the original path. If it doesn't, it defaults the path the the desktop"""

    split = path.rsplit("\\", 1)
    directory = split[0]
    foldername = split[1]

    if os.path.isdir(directory):
        return path

    logging.error(
        f'Directory "{directory}" does not exist for folder {foldername}, defaulting path to desktop'
    )
    return f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\\{foldername}"


def save_config():
    """Takes any changes to the config variables and writes them to the config file"""
    logging.debug("Writing config.json")

    # Set all the values in the dictionary to match the current variables
    config["port"] = port
    config["json_path"] = json_path
    config["csv_path"] = csv_path
    config["image_path"] = image_path
    config["email_list"] = email_list
    config["plc_ip"] = plc_ip
    config["email"] = email
    config["dredge_name"] = dredge_name
    config["freeboard_name"] = freeboard_name
    config["modbus"] = modbus
    config["modbus_bits"] = modbus_bits
    config["csv0600"] = csv0600
    config["csv0600_saved"] = csv0600_saved
    config["date_1"] = datetime.datetime.strftime(last_save_date, "%Y-%m-%d")
    config["date_2"] = datetime.datetime.strftime(last_run_update_date, "%Y-%m-%d")
    config["date_3"] = datetime.datetime.strftime(run_until, "%Y-%m-%d")

    save_env(env)

    # Open the config file and save the variables
    with open(proj_dir + "/config.json", "w") as f:
        json.dump(config, f, indent=4)


def genHeader():
    csv_header = "msg_time, vert_correction, ch_latitude, ch_longitude, ch_depth, ch_heading, slurry_velocity, slurry_density, pump_rpm, vacuum, outlet_psi, comment, "
    for name in modbus:
        csv_header += f"{name}, "
    for name in modbus_bits:
        csv_header += f"{name}, "
    csv_header += "msg_start_time, msg_end_time, function_code, comment, msg_time, outfall_location, outfall_latitude, outfall_longitude, outfall_heading, outfall_elevation, comment"
    return csv_header


# Create the log folder if it does not exist
if not os.path.isdir(proj_dir + "/logs"):
    os.makedirs(proj_dir + "/logs")

stream = logging.StreamHandler()
stream.setLevel(logging.INFO)

# Define the Logging config
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.handlers.RotatingFileHandler(
            proj_dir + "/logs/debug.log", maxBytes=(1048576 * 2), backupCount=7
        ),
        stream,
    ],
)

logging.debug("Start of program")

# Make sure config file exists
if not os.path.isfile(proj_dir + "/config.json"):
    logging.warning(
        "config.json not found, using example_config.json. Please set correct config settings"
    )
    shutil.copy(proj_dir + "/example_config.json", proj_dir + "/config.json")

# Open the config file and read the settings
with open(proj_dir + "/config.json") as json_data_file:
    config = json.load(json_data_file)

# Set all the variables from the dictionary
env = load_env()
port = config.get("port", "COM1")
json_path = config.get("json_path", "C:\\Users\\USERNAME\\Desktop\\json")
csv_path = config.get("csv_path", "C:\\Users\\USERNAME\\Desktop\\csv")
image_path = config.get("image_path", "C:\\Users\\USERNAME\\Desktop\\image")
email_list = config.get("email_list", ["example@gmail.com"])
plc_ip = config.get("plc_ip", "192.168.1.10")
email = config.get("email", "ilsdqmsystem@gmail.com")
dredge_name = config.get("dredge_name", "Dredge Name")
freeboard_name = config.get("freeboard_name", "Freeboard Name")
modbus = config.get(
    "modbus", {"offset": {"name": "offset", "address": "0", "float": True}}
)
modbus_bits = config.get("modbus_bits", {"vacuum": {"name": "vacuum", "address": "1"}})
csv0600 = config.get("csv0600", False)
csv0600_saved = config.get("csv0600_saved", False)

header = genHeader()

if "date_1" not in config:
    last_save_date = datetime.date.today()
else:
    last_save_date = datetime.date.fromisoformat(config["date_1"])

if "date_2" not in config:
    last_run_update_date = datetime.date.today()
else:
    last_run_update_date = datetime.date.fromisoformat(config["date_2"])

if "date_3" not in config:
    run_until = datetime.date.today()
else:
    run_until = datetime.date.fromisoformat(config["date_3"])

# Make sure the JSON and CSV paths are valid
json_path = checkPath(json_path)
csv_path = checkPath(csv_path)
image_path = checkPath(image_path)
save_config()
