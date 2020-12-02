import os
import logging
import glob
from pathlib import Path


def write_file(path, filename, data):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.debug("Making directory " + path)

    with open(Path(path, filename), "a") as f:
        f.write(str(data) + "\n")
        logging.debug("Data written to " + filename)


def add_headers(path, header):
    logging.debug("Getting filenames")
    filenames = glob.glob(path + "/*.csv")
    for filename in filenames:
        logging.debug("Checking " + filename)
        with open(filename, "r") as f:
            line = f.readline().strip('\n')
            #logging.debug("The line is {}, the header is {}".format(line, header))
            if line == header:
                continue
        logging.debug("Adding header to " + filename)
        line_prepender(filename, header)


def line_prepender(filename, line):
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)
