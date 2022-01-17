from dredge_logger.config import config

from pathlib import Path
import csv
import logging
import os
import pandas as pd

_logger = logging.getLogger(__name__)


def check_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        _logger.debug(f"Making directory {str(path)}")


def csv_write(filepath, data):
    """Write data to a csv file"""
    filepath = Path(filepath)
    check_path_exists(filepath.parent)
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def write_file(path, filename, data):
    """Using the paramaters, this function will write a file containing the data"""

    # Check to see if we need to make the folder
    check_path_exists(path)
    fileExists = os.path.exists(Path(path, filename))
    filepath = Path(path, filename)

    if ".csv" in filename:
        if not fileExists:
            csv_write(filepath, config.vars["header"])
        verify_headers(filepath, config.vars["header"])
        csv_write(filepath, data)
        _logger.debug("Data written to " + filename)

    elif ".json" in filename:
        with open(Path(path, filename), "a") as f:
            f.write(str(data).replace("'", '"') + "\n")
        _logger.debug("Data written to " + filename)

    elif ".txt" in filename:
        with open(Path(path, filename), "a") as f:
            f.write(str(data))
        _logger.debug("Data written to " + filename)

    else:
        _logger.error(f"Unknown File Type trying to save {filename}")


def verify_headers(file, header):
    """Checked given file and adds header if one does not exist"""
    _logger.debug("Checking " + str(file))
    csv_file = pd.read_csv(file, sep=",", skipinitialspace=True)
    csv_headers = list(csv_file.columns)
    if csv_headers != header:
        _logger.debug("Adding headers to " + str(file))
        new_cols = []
        i = 0
        j = 0
        while i < len(header) or j < len(csv_headers):
            if i < len(header) and j < len(csv_headers) and (header[i] == csv_headers[j] or header[i] in csv_headers[j]):
                i += 1
                j += 1
            elif i < len(header):
                new_cols.append((i, header[i]))
                i += 1
            else:
                j += 1
        for item in new_cols:
            csv_file.insert(item[0], item[1], None, True)
        csv_file.to_csv(file, index=False, na_rep="")


if __name__ == "__main__":
    filename = "2021-10-13.csv"
    path = config.vars["csv_path"]
    verify_headers(Path(path, filename), config.vars["header"])
