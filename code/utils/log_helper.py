import sys
from logging.config import fileConfig
import logging

fileConfig(sys.path[0] + '/utils/logging_config.ini')
#fileConfig('logging_config.ini')
logger = logging.getLogger()

def say(s, stream=sys.stdout):
    stream.write(s)
    stream.flush()

def info(msg, *args, **kwargs):
	logger.info(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
	logger.debug(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
	logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
	logger.error(msg, *args, **kwargs)
