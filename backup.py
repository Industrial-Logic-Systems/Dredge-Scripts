import config

import yagmail
import subprocess
import logging


def backup_files(filename):
    """This function when called will use the filename of the file to first backup
    the file to a remote computer with SCP, and then send the files to a list of emails"""
    logging.debug("Backing up files with name: " + filename)

    if config.enable_ssh:
        # Backing up JSON file
        try:
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
        except subprocess.TimeoutExpired:  # Watch for Timeouts
            logging.error(
                "SSH Timedout, File was not backed up to remote server")

    if config.enable_email:
        # Email the files to list of receivers
        files = [
            config.json_path + "\\" + filename + ".json",
            config.csv_path + "\\" + filename + ".csv",
        ]
        logging.debug("Sending Email(s) to " +
                      str(config.email_list).strip("[]"))
        send_email(
            config.email_list,
            "Dredge Files for " + filename,
            "Dredge Files for " + filename,
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


def send_ssh(destination, path, filename):
    # Make the directory that the files will be going into
    logging.debug("Making sure the path {} exists".format(destination))
    subprocess.Popen(
        ["ssh", config.remote_server, "mkdir", destination],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).wait(10)

    # Send the files to the remote server
    logging.debug("Sending File {}".format(destination + "\\" + filename))
    subprocess.Popen(
        [
            "scp",
            path + "/" + filename,
            "{}:{}\\{}".format(config.remote_server, destination, filename),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).wait(10)
