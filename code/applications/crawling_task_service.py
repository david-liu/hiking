#! ENV/bin/python
### -*- coding: utf-8 -*-
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import datetime
from flask import Flask
import logging

from hiking.devops import setup_console_logging

from crawling_task_app import CrawlingTaskApplication
from hiking.utils import WebServiceLoader, helper

logger = logging.getLogger(__name__)
setup_console_logging()


app = Flask(__name__)


def initialize_app(cfg_file, section=None):
  logger.info('begin to initialize app')

  conf = helper.loadConfiguration(cfg_file, section)

  host = conf.get('datasource_host')
  db = conf.get('datasource_db')
  user = conf.get('datasource_user')
  password = conf.get('datasource_password')
  phantomjs_path=conf.get('phantomjs_path')


  try:
      application = CrawlingTaskApplication(host=host,
        user=user,
        password=password,
        db=db,
        phantomjs_path=phantomjs_path)
  except Exception as e:
      logger.error(e)

  # application = CrawlingTaskApplication(host=host,
  #   user=user,
  #   password=password,
  #   db=db,
  #   phantomjs_path=phantomjs_path,
  #   batch_size=10)


  logger.info(application)
  service_loader = WebServiceLoader(app)
  service_loader.register_service_method(application.start_crawling_task)

  return service_loader



if __name__ == "__main__":

  service_loader = initialize_app(helper.convert_to_abspath(__file__, 'APP.INI'), 'crawling_task')

  service_loader.start()
