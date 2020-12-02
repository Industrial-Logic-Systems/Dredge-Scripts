import logging

json_path = "json"
csv_path = "csv"
remote_server = "fieldops4@192.168.1.111"

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.debug("Start of program")