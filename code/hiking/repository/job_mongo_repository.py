from hiking.utils.mongo_repository import MongoRepository
import datetime

class JobMongoRepository(MongoRepository):

    def __init__(self, host="localhost", port=27017):
        super(JobMongoRepository, self).__init__(
            db_name = 'jobs_db',
            table_name = 'jobs',
            host=host,
            port=port)

    def add_job(self, job):
        job['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d')

        query = {"url" : job["url"]}
        if self._coll.count(query) == 0:
            self.insert(job)
        else:
            self.update(query, job)
