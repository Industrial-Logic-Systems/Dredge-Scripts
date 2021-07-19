import config

import os
import logging
from pathlib import Path


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
        add_headers(Path(path, filename), config.header)


def add_headers(file, header):
    """Checked given file and adds header if one does not exist"""
    logging.debug("Checking " + str(file))
    with open(file, "r") as f:
        line = f.readline().strip("\n")
        # logging.debug("The line is {}, the header is {}".format(line, header))
        if line == header:
            return
        logging.debug("Adding header to " + str(file))
        line_prepender(file, header)


def line_prepender(filename, line):
    """Used by add_headers() to put a line at the begining of the file"""
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)
