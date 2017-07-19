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
      run_config_id = '%s-%s' % (task.batch_id, task.task_id)
      self.task_save_config[run_config_id] = task


  def add_entity(self, entity, primary_fields=[], run_config_id=None):
    if run_config_id not in self.task_save_config:
      logger.error('can not find the task with url: %s' % entity['_url'])
    else:
      task = self.task_save_config[run_config_id]

      entity['batch_id'] = task.batch_id
      entity['task_id'] = task.task_id
      content = json.loads(json.dumps(entity, ensure_ascii=True, default=date_handler))

      logger.info(json.dumps(content, ensure_ascii=False, default=date_handler))

      response = requests.post(task.saved_on_url, json=content)



  def add_log(self, status, run_config_id, url, message):

    if run_config_id not in self.task_save_config:
      logger.error('can not find the task with id: %s' % run_config_id)
    else:
      task = self.task_save_config[run_config_id]

      log = {
        'batch_id' : task.batch_id,
        'task_id'  : task.task_id,
        'status' : status,
        'url' : url,
        'message' : message
      }

      logger.info(json.dumps(log, ensure_ascii=False, default=date_handler))

      response = requests.post(task.logged_on_url, json=log)

class CrawlingTaskApplication(object):

  def __init__(self, host, user, password, db, phantomjs_path=None):
    self.configRepository = TaskConfigurationRepository(host=host, user=user, password=password, db=db)
    self.phantomjs_path=phantomjs_path

  @sequence_service(
          noun="crawling_task",
          verb="start",
          description="Start a crawling task.",
          parameters_desc={
              'task_ids': {
                  'desc':'the id of the task to be analyzed, for example \'1 1\' or [\'1\', \'1\']',
                  'type':'String | List'
              },
              'task_batched' : {
                  'desc':'whether the tasked id is contains the batch id',
                  'type':'Boolean'
              }
          })
  def start_crawling_task(self, task_ids, task_batched=False):
    logger.info('begin to start crawling task: [%s]' % task_ids)

    if not task_ids or len(task_ids) == 0:
      raise ValueError("the task id shoud be provided.")


    task_ids = [id.strip() for id in task_ids.split(",")]
    task_ids_set = set(task_ids)

    if len(task_ids) == 0:
      raise ValueError("the task id shoud be provided.")


    task_batch_ids = []
    if task_batched:
      new_task_ids = []
      for composed_id in task_ids_set:
        try:
          batch_id, task_id = composed_id.split('_')

          batch_id = batch_id.strip()
          task_id = task_id.strip()

          if task_id not in new_task_ids:
            task_batch_ids.append(batch_id)
            new_task_ids.append(task_id)

        except:
          raise ValueError("fail to parse batch id and task id with '_'.")
      task_ids = new_task_ids
    else:
      task_ids = list(task_ids_set)
      task_batch_ids = ["-1"] * len(task_ids)

    tasks = self.configRepository.get_crawling_task_config(task_ids)

    if tasks is None or len(tasks) == 0:
      logger.error("can not find task with id [%s]" % task_ids)
      raise ValueError('the task ids [%s] does not existed' % ', '.join(task_ids))
    else:
      logger.info("start #%s crawling tasks" % len(tasks))

      run_config_fns = []
      for ix, task in enumerate(tasks):
        task.batch_id = task_batch_ids[ix]
        def create_run_config_fn(run_config):
          def fn():
            return run_config

          return fn

        task.run_config.config_id = '%s-%s' % (task.batch_id, task.task_id)

        run_config_fns.append(create_run_config_fn(task.run_config))

      repository = EntityRestRepostory(tasks)

      app = HikingApplication(run_config_fns,
        repository=repository,
        phantomjs_path=self.phantomjs_path,
        run_in_command_line=False,
        )

      t = threading.Thread(target=app.start)
      t.start()

      return repository._entities

if __name__ == "__main__":
#   datasource_host=139.196.193.120
# datasource_db=cfdb
# datasource_user=cfdev
# datasource_password=cfdev
  application = CrawlingTaskApplication(
    host='127.0.0.1',
    user='cfdev',
    password='tongji2016',
    db='cfdb',
    # host='localhost',
    # user='root',
    # password='root',
    # db='crawling_task',
    phantomjs_path='/Users/zhouy/.nvm/versions/node/v6.10.0/bin/phantomjs')
    # phantomjs_path='/Users/gbsc.ibm/pyproject/hiking/plugins/phantomjs/mac/phantomjs')

  application.start_crawling_task('1418,1318,5303,5304,5305,5306,5307,5308,5309,5310', task_batched=False)
  # ,5303,5304,5305,5306,5307,5308,5309,5310
  # 1418,1318,5303,5304,5305,5306,5307,5308,5309,5310
