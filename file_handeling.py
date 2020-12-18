import os
import logging
import glob
from pathlib import Path


def write_file(path, filename, data):
    """ Using the paramaters, this function will write a file containing the data """

    # Check to see if we need to make the folder
    if not os.path.exists(path):
        os.makedirs(path)
        logging.debug("Making directory " + path)

    # Write the file
    with open(Path(path, filename), "a") as f:
        f.write(str(data).replace("'", '"') + "\n")
        logging.debug("Data written to " + filename)


def add_headers(path, header):
    """ Goes though the folder pointed at by path, and adds the header if it doesn't have it already """
    logging.debug("Getting filenames")
    filenames = glob.glob(path + "/*.csv")
    for filename in filenames:
        logging.debug("Checking " + filename)
        with open(filename, "r") as f:
            line = f.readline().strip("\n")
            # logging.debug("The line is {}, the header is {}".format(line, header))
            if line == header:
                continue
        logging.debug("Adding header to " + filename)
        line_prepender(filename, header)


def line_prepender(filename, line):
    """ Used by add_headers() to put a line at the begining of the file """
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)
