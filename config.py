import logging

json_path = "json"
csv_path = "csv"

remote_server = "fieldops4@192.168.1.111"
remote_server_path = "C:\\Users\\luke3\\Desktop"

email_list = ["frazzercoding+1@gmail.com", "frazzercoding+2@gmail.com"]

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.debug("Start of program")