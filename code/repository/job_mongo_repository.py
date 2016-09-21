from utils.mongo_repository import MongoRepository
import datetime

class JobMongoRepostory(MongoRepository):

	def __init__(self, url=None):
		super(JobMongoRepostory, self).__init__(
			database = 'jobs', 
			collection = 'job',
			url=url)

	def add_job(self, job):
		job['updated_ts'] = datetime.datetime.utcnow()
		
		query = {"url" : job["url"]}
		if self._coll.count(query) == 0:
			self.insert(job)
		else:
			self.update(query, job)