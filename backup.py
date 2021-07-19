import config

import yagmail
import subprocess
import logging


def backup_files(filename):
    """This function when called will use the filename of the file to send the files to a list of emails"""

    logging.debug("Backing up files with name: " + filename)

    # Email the files to list of receivers
    files = [
        config.json_path + "\\" + filename + ".json",
        config.csv_path + "\\" + filename + ".csv",
    ]
    logging.debug("Sending Email(s) to " + str(config.email_list).strip("[]"))

    subject = f"{config.dredge_name} - {filename} - Log Files"
    body = (
        f"The files with the logged information from {config.dredge_name} on {filename}"
    )

    send_email(
        config.email_list,
        subject,
        body,
        files,
    )


def send_email(receivers, subject, body, files):
    """ Sends an email with the above parameters """
    yag = yagmail.SMTP(config.email)
    yag.send(
        to=receivers,
        subject=subject,
        contents=body,
        attachments=files,
    )
