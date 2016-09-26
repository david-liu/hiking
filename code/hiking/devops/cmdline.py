"""Helper functions to initializer Websauna framework for command line applications."""
import logging
import os
from logging.config import fileConfig
import sys

from rainbow_logging_handler import RainbowLoggingHandler


def setup_logging(config_uri):
    """Include-aware Python logging setup from INI config file.
    """
    fileConfig(config_uri)

def setup_console_logging(log_level=None):
    """Setup console logging.

    Aimed to give easy sane defaults for loggig in command line applications.

    Don't use logging settings from INI, but use hardcoded defaults.
    """

    formatter = logging.Formatter("[%(asctime)s] [%(name)s %(funcName)s:%(lineno)d] %(message)s")  # same as default

    # setup `RainbowLoggingHandler`
    # and quiet some logs for the test output
    handler = RainbowLoggingHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.handlers = [handler]

    env_level = os.environ.get("LOG_LEVEL", "info")
    log_level = log_level or getattr(logging, env_level.upper())
    logger.setLevel(log_level)

    # logger = logging.getLogger("requests.packages.urllib3.connectionpool")
    # logger.setLevel(logging.ERROR)

    # # SQL Alchemy transactions
    # logger = logging.getLogger("txn")
    # logger.setLevel(logging.ERROR)

