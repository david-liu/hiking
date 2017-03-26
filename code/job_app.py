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
import threading
import json
import requests
import urllib2


from hiking.repository import MySqlConfigRepository
from hiking import HikingApplication
from hiking.utils import parser_helper, url_helper
from hiking.utils import sequence_service
from hiking.utils import WebServiceLoader

logger = logging.getLogger(__name__)

app = Flask(__name__)

@sequence_service(
        noun="crawling_task",
        verb="add",
        description="Start a crawling task.",
        parameters_desc={
            'task_id': {
                'desc':'the id of the task',
                'type':'String'
            },
            'title' : {
                'desc':'the url of the job',
                'type':'String'
            },
            'location' : {
                'desc':'the url of the job',
                'type':'String'
            },
            'url' : {
                'desc':'the url of the job',
                'type':'String'
            },
            'publish_date' : {
                'desc':'the url of the job',
                'type':'String'
            }
        })
def add_crawling_task(task_id, title, url, location, publish_date):
	
  print('=======')
  print(task_id)
  print(title)
  print(url)
  print(location)
  print(publish_date)




if __name__ == "__main__":
  service_loader = WebServiceLoader(app)
  service_loader.register_service_method(add_crawling_task)
  
  service_loader.start(default_port=5010)


  #start_crawling_task('1, 2')




