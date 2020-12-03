import config

import yagmail
import subprocess
import logging


def backup_files(filename):
    logging.debug("Backing up files with name: " + filename)

    # Backing up JSON file
    logging.debug("Sending JSON over SSH")
    send_ssh(
        config.remote_server_path + "\\" + config.json_path,
        config.json_path,
        filename + ".json",
    )
    # Backing up CSV file
    logging.debug("Sending CSV over SSH")
    send_ssh(
        config.remote_server_path + "\\" + config.csv_path,
        config.csv_path,
        filename + ".csv",
    )

    # Email the files to list of receivers
    files = [
        config.json_path + "\\" + filename + ".json",
        config.csv_path + "\\" + filename + ".csv",
    ]
    logging.debug("Sending Email")
    send_email(
        config.email_list,
        "Dredge Files for " + filename,
        "Dredge Files for " + filename,
        files,
    )


def send_email(receivers, subject, body, files):
    yag = yagmail.SMTP("frazzercoding")
    yag.send(
        to=receivers,
        subject=subject,
        contents=body,
        attachments=files,
    )


def send_ssh(destination, path, filename):
    logging.debug("Making sure the path {} exists".format(destination))
    subprocess.Popen(
        ["ssh", config.remote_server, "mkdir", destination],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    logging.debug("Sending File {}".format(destination + "\\" + filename))
    subprocess.Popen(
        [
            "scp",
            path + "/" + filename,
            "{}:{}\\{}".format(config.remote_server, destination, filename),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
