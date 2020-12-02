import config

import yagmail
import subprocess
import logging


def backup_files(filename):
    logging.debug("Sending files with the name " + filename)
    send_ssh("C:\\Users\\luke3\\Desktop\\json", "json", filename + ".json")
    send_ssh("C:\\Users\\luke3\\Desktop\\csv", "csv", filename + ".csv")


def send_email(receivers, subject, body, filename):
    yag = yagmail.SMTP("frazzercoding")
    yag.send(
        to=receivers,
        subject=subject,
        contents=body,
        attachments=filename,
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
