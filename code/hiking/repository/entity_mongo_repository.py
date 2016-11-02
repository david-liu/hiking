from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from hiking.utils import MongoRepository
import datetime

class EntityMongoRepository(MongoRepository):

    def __init__(self, db_name, table_name, unique_query_fn = None, host="localhost",  port=27017):
        super(EntityMongoRepository, self).__init__(
            db_name=db_name,
            table_name=table_name,
            host=host,
            port=port)

        self.unique_check_fn = unique_query_fn

    def add_entity(self, job):
        job['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d')

        query = None
        if self.unique_check_fn is not None:
            query = self.unique_check_fn()

        #query = {"url" : job["url"]}
        if query is None or self._coll.count(query) == 0:
            self.insert(job)
        else:
            self.update(query, job)
