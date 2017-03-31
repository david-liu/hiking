from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class CrawlingTask(object):

    def __init__(self, task_id, channel_id, saved_on_url, logged_on_url, run_config, batch_id=-1):
        self.batch_id = batch_id
        self.task_id = task_id
        self.saved_on_url = saved_on_url
        self.logged_on_url = logged_on_url
        self.channel_id = channel_id
        self.run_config = run_config