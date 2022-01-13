import logging
import threading

from dredge_logger.config import config
from dredge_logger.gui import LogGUI


__author__ = "Luke Eltiste"
__copyright__ = "Luke Eltiste"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def main():
    app = LogGUI()

    # Start the log loop
    logging.info("Starting Log Loop")
    threading.Thread(target=app.log_loop, daemon=True).start()

    # Start the GUI
    logging.info("Starting GUI")
    app.mainloop()

    _logger.info("Script ends here")


if __name__ == "__main__":
    main()
    _logger.info(config._dirs.user_log_dir)
