from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class CrawlingTask(object):

	def __init__(self, task_id, channel_id, reset_url, run_config):
		self.task_id = task_id
		self.reset_url = reset_url
		self.channel_id = channel_id
		self.run_config = run_config