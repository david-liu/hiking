from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from hiking.utils import MongoRepository
import datetime

class EntityMongoRepository(MongoRepository):

    def __init__(self, db_name, table_name, host="localhost",  port=27017):
        super(EntityMongoRepository, self).__init__(
            db_name=db_name,
            table_name=table_name,
            host=host,
            port=port)

    def add_entity(self, entity, primary_fields=[]):
        entity['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d')

        query = None
        if len(primary_fields) > 0:
            query = {}
            for primary_field in primary_fields:
                query[primary_field] = entity[primary_field]

        print(query)
        print(self._coll.count(query))

        #query = {"url" : job["url"]}
        if query is None or self._coll.count(query) == 0:
            self.insert(entity)
        else:
            self.update(query, entity)
