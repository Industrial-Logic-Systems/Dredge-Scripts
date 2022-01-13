import logging
import os
import logging


from dredge_logger import __version__

from dredge_logger.config import config

__author__ = "Luke Eltiste"
__copyright__ = "Luke Eltiste"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def main():
    _logger.debug("Starting crazy calculations...")
    # Start the log loop
    # Start the GUI
    _logger.info("Script ends here")


if __name__ == "__main__":
    main()
    _logger.info(config._dirs.user_log_dir)
