import json
from bson import json_util

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise obj

class JobConsoleRepository(object):

	def add_job(self, job):
		print(json.dumps(job, ensure_ascii=False, default=date_handler))