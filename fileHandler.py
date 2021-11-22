import config

import os
import logging
from pathlib import Path
import pandas as pd


def write_file(path, filename, data):
    """Using the paramaters, this function will write a file containing the data"""

    # Check to see if we need to make the folder
    if not os.path.exists(path):
        os.makedirs(path)
        logging.debug("Making directory " + path)

    # Write the file
    with open(Path(path, filename), "a") as f:
        f.write(str(data).replace("'", '"') + "\n")
        logging.debug("Data written to " + filename)

    if ".csv" in filename:
        verify_headers(Path(path, filename), config.header)


def verify_headers(file, header):
    """Checked given file and adds header if one does not exist"""
    logging.debug("Checking " + str(file))
    csv_file = pd.read_csv(file, sep=",", skipinitialspace=True)
    header = [x.strip() for x in header.split(",")]
    csv_headers = list(csv_file.columns)
    if csv_headers != header:
        logging.debug("Adding headers to " + str(file))
        new_cols = []
        i = 0
        j = 0
        while i < len(header) and j < len(csv_headers):
            if header[i] == csv_headers[j] or header[i] in csv_headers[j]:
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
    path = config.csv_path
    verify_headers(Path(path, filename), config.header)
