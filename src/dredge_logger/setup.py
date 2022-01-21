import logging
import threading

from dredge_logger.gui import LogGUI


__author__ = "Luke Eltiste"
__copyright__ = "Luke Eltiste"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


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
