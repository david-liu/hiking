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


from hiking.repository import TaskConfigurationRepository
from hiking import HikingApplication
from hiking.utils import parser_helper, url_helper
from hiking.utils import sequence_service

logger = logging.getLogger(__name__)


configRepository = TaskConfigurationRepository()

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError ("Type not serializable")

class EntityRestRepostory(object):
  def __init__(self, tasks):
    self._entities = []

    self.task_save_config = {}
    for task in tasks:
      self.task_save_config[task.task_id] = task
  

  def add_entity(self, entity, primary_fields=[], run_config_id=None):
    if run_config_id not in self.task_save_config:
      logger.error('can not find the task wit url: %s' % entity['_url'])
    else:
      task = self.task_save_config[run_config_id]
      
      entity['task_id'] = task.task_id
      content = json.loads(json.dumps(entity, ensure_ascii=True, default=date_handler))

      print(json.dumps(entity, ensure_ascii=False, default=date_handler))

      #response = requests.post(task.reset_url, json=content)


@sequence_service(
        noun="crawling_task",
        verb="start",
        description="Start a crawling task.",
        parameters_desc={
            'task_ids': {
                'desc':'the id of the task to be analyzed, for example \'1 1\' or [\'1\', \'1\']',
                'type':'String | List'
            }
        })
def start_crawling_task(task_ids):
  if not task_ids or len(task_ids) == 0:
    raise ValueError("the task id shoud be provided.")  

  task_ids = task_ids.split(",")

  
  if len(task_ids) == 0:
    raise ValueError("the task id shoud be provided.")

  tasks = configRepository.get_crawling_task_config(task_ids)

  if tasks is None or len(tasks) == 0:
    logger.error("can not find task with id [%s]" % task_ids)
  else:
    logger.info("start #%s crawling tasks" % len(tasks))

    run_config_fns = []
    for ix, task in enumerate(tasks):
      def create_run_config_fn(run_config):
        def fn():
          return run_config

        return fn

      run_config_fns.append(create_run_config_fn(task.run_config))
    
    repository = EntityRestRepostory(tasks)

    app = HikingApplication(run_config_fns, repository)
    
    t = threading.Thread(target=app.start)
    t.start()

    return repository._entities

if __name__ == "__main__":
  start_crawling_task('4')




