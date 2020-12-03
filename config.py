import logging
import json


def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


""" Read Config File """
with open("config.json") as json_data_file:
    config = json.load(json_data_file)

""" Set Config File Values """
port_name = config["port"]
json_path = config["json_path"]
csv_path = config["csv_path"]
remote_server = config["remote_server"]
remote_server_path = config["remote_server_path"]
email_list = config["email_list"]


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.debug("Start of program")