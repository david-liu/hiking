#! ENV/bin/python
### -*- coding: utf-8 -*-
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import datetime
from flask import Flask

from crawling_task_app import start_crawling_task
from hiking.utils import WebServiceLoader

app = Flask(__name__)


if __name__ == "__main__":
  service_loader = WebServiceLoader(app)
  service_loader.register_service_method(start_crawling_task)
  
  service_loader.start()




