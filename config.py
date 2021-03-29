import logging
import logging.handlers
import json
import os

# Define basic variables
proj_dir = os.path.dirname(__file__)
email = "frazzercoding@gmail.com"

# Create the log folder if it does not exist
if not os.path.isdir(proj_dir + "/logs"):
    os.makedirs(proj_dir + "/logs")

# Define the Logging config
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.handlers.RotatingFileHandler(
            proj_dir + "/logs/debug.log", maxBytes=(1048576 * 5), backupCount=7
        ),
        logging.StreamHandler(),
    ],
)

logging.debug("Start of program")


def save_config():
    """ Takes any changes to the config variables and writes them to the config file """
    logging.debug("Writing config.json")

    # Set all the values in the dictionary to match the current variables
    config["port"] = port_name
    config["json_path"] = json_path
    config["csv_path"] = csv_path
    config["remote_server"] = remote_server
    config["remote_server_path"] = remote_server_path
    config["email_list"] = email_list
    config["enable_email"] = enable_email
    config["enable_ssh"] = enable_ssh
    config["plc_ip"] = plc_ip

    # Open the config file and save the variables
    with open(proj_dir + "/config.json", "w") as f:
        json.dump(config, f, indent=4)


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


# Open the config file and read the settings
with open(proj_dir + "/config.json") as json_data_file:
    config = json.load(json_data_file)

# Set all the variables from the dictionary
port_name = config["port"]
json_path = config["json_path"]
csv_path = config["csv_path"]
remote_server = config["remote_server"]
remote_server_path = config["remote_server_path"]
email_list = config["email_list"]
enable_email = config["enable_email"]
enable_ssh = config["enable_ssh"]
plc_ip = config["plc_ip"]

# Make sure the JSON and CSV paths are valid
json_path = checkPath(json_path)
csv_path = checkPath(csv_path)
save_config()
