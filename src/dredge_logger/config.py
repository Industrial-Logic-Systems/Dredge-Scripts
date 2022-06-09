import datetime
import json
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

        self.var_types = [
            ["dredge_type", "pipeline"],
            ["dredge_name", "Dredge Name"],
            ["port", "COM1"],
            ["json_path", "C:\\Users\\USERNAME\\Desktop\\json"],
            ["xml_path", "C:\\Users\\USERNAME\\Desktop\\xml"],
            ["csv_path", "C:\\Users\\USERNAME\\Desktop\\csv"],
            ["image_path", "C:\\Users\\USERNAME\\Desktop\\image"],
            ["email_list", ["example@example.com"]],
            ["plc_ip", "192.168.1.10"],
            ["email", "ilsdqmsystem@gmail.com"],
            ["freeboard_name", "ILS-Dredge"],
            ["modbus", {"offset": {"name": "offset", "address": "0", "float": True}}],
            ["modbus_bits", {"vacuum": {"name": "vacuum", "address": "1"}}],
            ["csv0600", False],
            ["csv0600_saved", False],
            [
                "images",
                {
                    "save": True,
                    "time": "msg_time",
                    "graphs": {
                        "Velocity": {"name": "Velocity", "unit": "FPS", "variable": "slurry_velocity"},
                        "Vacuum": {"name": "Vacuum", "unit": "Inches WC", "variable": "vacuum"},
                        "Discharge_Pressure": {"name": "Discharge_Pressure", "unit": "PSI", "variable": "outlet_psi"},
                        "Pump_Speed": {"name": "Pump_Speed", "unit": "RPM", "variable": "pump_rpm"},
                        "Depth": {"name": "Depth", "unit": "Feet", "variable": "ch_depth"},
                    },
                },
            ],
            ["program_key", ""],
        ]

        self.vars = {}

        self.load_config()

        # Make sure paths are valid
        for var in self.var_types:
            if "path" in var[0]:
                self.vars[var[0]] = self.checkPath(self.vars[var[0]])
        self.save_config()

    def setup_logging(self):
        """Setup basic logging"""
        # Create the log folder if it does not exist
        if not os.path.isdir(self._dirs.user_log_dir):
            os.makedirs(self._dirs.user_log_dir)

        logformat = "[%(asctime)s] %(levelname)8s:%(name)-30s %(message)s"

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

        for var_name, default_value in self.var_types:
            self.vars[var_name] = config_file.get(var_name, default_value)

        self.vars["header"] = self.genHeader()
        self.vars["last_save_date"] = datetime.date.fromisoformat(
            config_file.get("last_save_date", datetime.date.today().isoformat())
        )
        self.vars["last_check_for_update"] = datetime.date.fromisoformat(
            config_file.get("last_check_for_update", datetime.date.today().isoformat())
        )

    def genHeader(self):
        if self.vars["dredge_type"] == "pipeline":
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
        elif self.vars["dredge_type"] == "hopper":
            csv_header = [
                "DREDGE_NAME",
                "DATE_TIME",
                "CONTRACT_NUMBER",
                "LOAD_NUMBER",
                "VESSEL_X",
                "VESSEL_Y",
                "PORT_DRAG_X",
                "PORT_DRAG_Y",
                "STBD_DRAG_X",
                "STBD_DRAG_Y",
                "HULL_STATUS",
                "VESSEL_COURSE",
                "VESSEL_SPEED",
                "VESSEL_HEADING",
                "TIDE",
                "DRAFT_FORE",
                "DRAFT_AFT",
                "ULLAGE_FORE",
                "ULLAGE_AFT",
                "HOPPER_VOLUME",
                "DISPLACEMENT",
                "EMPTY_DISPLACEMENT",
                "DRAGHEAD_DEPTH_PORT",
                "DRAGHEAD_DEPTH_STBD",
                "PORT_DENSITY",
                "STBD_DENSITY",
                "PORT_VELOCITY",
                "STBD_VELOCITY",
                "PUMP_RPM_PORT",
                "PUMP_RPM_STBD",
            ]
            for name in self.vars["modbus"]:
                csv_header.append(name)
            for name in self.vars["modbus_bits"]:
                csv_header.append(name)
        else:
            self._logger.error("Unknown dredge type", self.vars["dredge_type"])
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

        try:
            # Open the config file and read the settings
            with open(self._dirs.user_config_dir + "/config.json") as json_data_file:
                config_file = json.load(json_data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            config_file = {}

        # Set all the values in the dictionary to match the current variables
        for var in self.var_types:
            config_file[var[0]] = self.vars[var[0]]

        config_file["last_save_date"] = datetime.datetime.strftime(self.vars["last_save_date"], "%Y-%m-%d")
        config_file["last_check_for_update"] = datetime.datetime.strftime(self.vars["last_check_for_update"], "%Y-%m-%d")

        if not os.path.exists(self._dirs.user_config_dir):
            os.makedirs(self._dirs.user_config_dir)

        # Open the config file and save the variables
        with open(self._dirs.user_config_dir + "/config.json", "w") as f:
            json.dump(config_file, f, indent=4)


config = Config()
