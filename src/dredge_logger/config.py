from dotenv import load_dotenv
from pathlib import Path
import datetime
import json
import logging
import logging.handlers
import os
from appdirs import AppDirs


class Config:
    def __init__(self):
        # Setup Variables
        self._logger = logging.getLogger(__name__)
        self._dirs = AppDirs("dredge_logger", "ILS")
        self._proj_dir = os.path.dirname(__file__)
        self.setup_logging()

        self.vars = {}

        self.load_config()

        # Make sure the JSON and CSV paths are valid
        self.vars["json_path"] = self.checkPath(self.vars["json_path"])
        self.vars["csv_path"] = self.checkPath(self.vars["csv_path"])
        self.vars["image_path"] = self.checkPath(self.vars["image_path"])
        self.save_config()

    def setup_logging(self):
        """Setup basic logging"""
        # Create the log folder if it does not exist
        if not os.path.isdir(self._dirs.user_log_dir):
            os.makedirs(self._dirs.user_log_dir)

        logformat = "[%(asctime)s] %(levelname)s:%(name)s - %(message)s"

        stream = logging.StreamHandler()
        stream.setLevel(logging.INFO)

        # Define the Logging config
        logging.basicConfig(
            format=logformat,
            level=logging.DEBUG,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.handlers.RotatingFileHandler(
                    self._dirs.user_log_dir + "/debug.log",
                    maxBytes=(1048576 * 2),
                    backupCount=7,
                ),
                stream,
            ],
        )

        self._logger.debug("Logging Started")

    def load_config(self):
        """Load the config file"""

        try:
            # Open the config file and read the settings
            with open(self._dirs.user_config_dir + "/config.json") as json_data_file:
                config_file = json.load(json_data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            self._logger.error("Config file not found, using default settings")
            config_file = {}

        # Set all the variables from the dictionary
        self.vars["env"] = self.load_env()
        self.vars["port"] = config_file.get("port", "COM1")
        self.vars["json_path"] = config_file.get("json_path", "C:\\Users\\USERNAME\\Desktop\\json")
        self.vars["csv_path"] = config_file.get("csv_path", "C:\\Users\\USERNAME\\Desktop\\csv")
        self.vars["image_path"] = config_file.get("image_path", "C:\\Users\\USERNAME\\Desktop\\image")
        self.vars["email_list"] = config_file.get("email_list", ["example@gmail.com"])
        self.vars["plc_ip"] = config_file.get("plc_ip", "192.168.1.10")
        self.vars["email"] = config_file.get("email", "ilsdqmsystem@gmail.com")
        self.vars["dredge_name"] = config_file.get("dredge_name", "Dredge Name")
        self.vars["freeboard_name"] = config_file.get("freeboard_name", "Freeboard Name")
        self.vars["modbus"] = config_file.get("modbus", {"offset": {"name": "offset", "address": "0", "float": True}})
        self.vars["modbus_bits"] = config_file.get("modbus_bits", {"vacuum": {"name": "vacuum", "address": "1"}})
        self.vars["csv0600"] = config_file.get("csv0600", False)
        self.vars["csv0600_saved"] = config_file.get("csv0600_saved", False)
        self.vars["header"] = self.genHeader()
        self.vars["last_save_date"] = datetime.date.fromisoformat(
            config_file.get("last_save_date", datetime.date.today().isoformat())
        )

    def save_env(self, env):
        if not os.path.exists(self._dirs.user_data_dir):
            os.makedirs(self._dirs.user_data_dir)
        with open(self._dirs.user_data_dir + "/.env", "w") as f:
            if env["user"] is not None:
                f.write("DWEET_USER=" + env["user"] + "\n")
            if env["pass"] is not None:
                f.write("DWEET_PASS=" + env["pass"] + "\n")
            if env["key"] is not None:
                f.write("MASTER_KEY=" + env["key"] + "\n")

    def load_env(self):
        if os.path.exists(self._dirs.user_data_dir + "/.env"):
            dotenv_path = Path(self._dirs.user_data_dir + "/.env")
            load_dotenv(dotenv_path=dotenv_path)
        env = {}
        env["user"] = os.getenv("DWEET_USER", None)
        env["pass"] = os.getenv("DWEET_PASS", None)
        env["key"] = os.getenv("MASTER_KEY", None)
        return env

    def genHeader(self):
        csv_header = [
            "msg_time",
            "vert_correction",
            "ch_latitude",
            "ch_longitude",
            "ch_depth",
            "ch_heading",
            "slurry_velocity",
            "slurry_density",
            "pump_rpm",
            "vacuum",
            "outlet_psi",
            "comment",
        ]
        for name in self.vars["modbus"]:
            csv_header.append(name)
        for name in self.vars["modbus_bits"]:
            csv_header.append(name)
        csv_header += [
            "msg_start_time",
            "msg_end_time",
            "function_code",
            "comment_ne",
            "msg_time_of",
            "outfall_location",
            "outfall_latitude",
            "outfall_longitude",
            "outfall_heading",
            "outfall_elevation",
            "comment_of",
        ]
        return csv_header

    def checkPath(self, path):
        """Will take a path, and remove the last directory, then check if it exists.
        If the path exists, then it returns the original path. If it doesn't, it defaults the path the the desktop"""

        split = path.rsplit("\\", 1)
        directory = split[0]
        foldername = split[1]

        if os.path.isdir(directory):
            return path

        self._logger.error(f'Directory "{directory}" does not exist for folder {foldername}, using default directory')
        return f"{self._dirs.user_data_dir}\\{foldername}"

    def save_config(self):
        """Takes any changes to the config variables and writes them to the config file"""
        self._logger.debug("Writing config.json")

        config_file = {}

        # Set all the values in the dictionary to match the current variables
        config_file["port"] = self.vars["port"]
        config_file["json_path"] = self.vars["json_path"]
        config_file["csv_path"] = self.vars["csv_path"]
        config_file["image_path"] = self.vars["image_path"]
        config_file["email_list"] = self.vars["email_list"]
        config_file["plc_ip"] = self.vars["plc_ip"]
        config_file["email"] = self.vars["email"]
        config_file["dredge_name"] = self.vars["dredge_name"]
        config_file["freeboard_name"] = self.vars["freeboard_name"]
        config_file["modbus"] = self.vars["modbus"]
        config_file["modbus_bits"] = self.vars["modbus_bits"]
        config_file["csv0600"] = self.vars["csv0600"]
        config_file["csv0600_saved"] = self.vars["csv0600_saved"]
        config_file["last_save_date"] = datetime.datetime.strftime(self.vars["last_save_date"], "%Y-%m-%d")

        self.save_env(self.vars["env"])

        if not os.path.exists(self._dirs.user_config_dir):
            os.makedirs(self._dirs.user_config_dir)

        # Open the config file and save the variables
        with open(self._dirs.user_config_dir + "/config.json", "w") as f:
            json.dump(config_file, f, indent=4)


config = Config()
