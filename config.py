import logging
import json


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

    # Open the config file and save the variables
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


# Open the config file and read the settings
with open("config.json") as json_data_file:
    config = json.load(json_data_file)

# Set all the variables from the dictionary
port_name = config["port"]
json_path = config["json_path"]
csv_path = config["csv_path"]
remote_server = config["remote_server"]
remote_server_path = config["remote_server_path"]
email_list = config["email_list"]

# Define the Logging config
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.debug("Start of program")