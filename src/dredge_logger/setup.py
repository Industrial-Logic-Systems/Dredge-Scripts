import logging
import os
import shutil
import threading

from dredge_logger.gui import LogGUI


__author__ = "Luke Eltiste"
__copyright__ = "Luke Eltiste"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def initialize():
    from dredge_logger.config import config

    _logger.info("Initializing")
    desktop = os.environ["USERPROFILE"] + "\\Desktop"
    startup = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

    os.startfile(desktop)
    os.startfile(startup)
    shutil.copyfile(config._proj_dir + "\\resources\\StartLogger.bat", desktop + "\\StartLogger.bat")
    shutil.copyfile(config._proj_dir + "\\resources\\StartLogger.bat", startup + "\\StartLogger.bat")


def main():
    app = LogGUI()

    # Start the log loop
    _logger.info("Starting Log Loop")
    threading.Thread(target=app.log_loop, daemon=True).start()

    # Start the GUI
    _logger.info("Starting GUI")
    app.mainloop()

    _logger.info("Script ends here")


if __name__ == "__main__":
    _logger.info("Logger Ran manually")
    main()
    _logger.info("Manual End")
