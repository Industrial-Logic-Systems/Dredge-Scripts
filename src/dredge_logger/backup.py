import logging

import yagmail
from dredge_logger import generateImages
from dredge_logger.config import config

_logger = logging.getLogger(__name__)


def backup_files(filename, extra_csv=False):
    """This function when called will use the filename of the file to send the files to a list of emails"""

    _logger.debug("Backing up files with name: " + filename)
    if extra_csv:
        try:
            files = [
                config.vars["csv_path"] + "\\" + filename + ".csv",
            ]
            _logger.debug("Sending Email(s) to " + str(config.vars["email_list"]).strip("[]"))
            subject = f"{config.vars['dredge_name']} - {filename} - Log Files - CSV_0600"
            body = f"The files with the logged information from {config.vars['dredge_name']} on {filename.strip('_0600')}"
            send_email(
                config.vars["email_list"],
                subject,
                body,
                files,
            )
        except Exception as e:
            _logger.debug("Error sending email")
            _logger.debug(e, exc_info=True)
    else:
        sendImage = True
        try:
            filenames = generateImages.generateGraph(filename + ".csv")
        except Exception as e:
            _logger.debug("Error generating graph: " + str(e), exc_info=True)
            sendImage = False
        finally:
            try:
                # Email the files to list of receivers
                files = [
                    config.vars["json_path"] + "\\" + filename + ".json",
                    config.vars["csv_path"] + "\\" + filename + ".csv",
                ]
                if sendImage:
                    for fn in filenames:
                        files.append(fn)

                _logger.debug("Sending Email(s) to " + str(config.vars["email_list"]).strip("[]"))

                subject = f"{config.vars['dredge_name']} - {filename} - Log Files"
                body = f"The files with the logged information from {config.vars['dredge_name']} on {filename}"

                send_email(
                    config.vars["email_list"],
                    subject,
                    body,
                    files,
                )
            except Exception as e:
                _logger.debug("Error sending email")
                _logger.debug(e, exc_info=True)


def send_email(receivers, subject, body, files):
    """Sends an email with the above parameters"""
    yag = yagmail.SMTP(config.vars["email"])
    yag.send(
        to=receivers,
        subject=subject,
        contents=body,
        attachments=files,
    )
