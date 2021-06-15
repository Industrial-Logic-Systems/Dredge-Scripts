import datetime
import json
import logging
import logging.handlers
import os
import shutil

# Get the directory where the script is located
proj_dir = os.path.dirname(__file__)


def checkPath(path):
    """Will take a path, and remove the last directory, then check if it exists.
    If the path exists, then it returns the original path. If it doesn't, it defaults the path the the desktop"""

    split = path.rsplit("\\", 1)
    dir = split[0]
    foldername = split[1]

    if os.path.isdir(dir):
        return path
    else:
        logging.error(
            f'Directory "{dir}" does not exist for folder {foldername}, defaulting path to desktop'
        )
        return f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\\{foldername}"


def save_config():
    """ Takes any changes to the config variables and writes them to the config file """
    logging.debug("Writing config.json")

    # Set all the values in the dictionary to match the current variables
    config["csv_path"] = csv_path
    config["dredge_name"] = dredge_name
    config["email_list"] = email_list
    config["email"] = email
    config["enable_email"] = enable_email
    config["enable_ssh"] = enable_ssh
    config["json_path"] = json_path
    config["last_save_date"] = datetime.datetime.strftime(last_save_date, "%Y-%m-%d")
    config["plc_ip"] = plc_ip
    config["port"] = port_name
    config["remote_server_path"] = remote_server_path
    config["remote_server"] = remote_server

    # Open the config file and save the variables
    with open(proj_dir + "/config.json", "w") as f:
        json.dump(config, f, indent=4)


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
csv_path = config["csv_path"]
dredge_name = config["dredge_name"]
email = config["email"]
email_list = config["email_list"]
enable_email = config["enable_email"]
enable_ssh = config["enable_ssh"]
json_path = config["json_path"]
plc_ip = config["plc_ip"]
port_name = config["port"]
remote_server = config["remote_server"]
remote_server_path = config["remote_server_path"]

if "last_save_date" not in config:
    last_save_date = datetime.date.today()
else:
    last_save_date = datetime.date.fromisoformat(config["last_save_date"])

# Make sure the JSON and CSV paths are valid
json_path = checkPath(json_path)
csv_path = checkPath(csv_path)
save_config()
