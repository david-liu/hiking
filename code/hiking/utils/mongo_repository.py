from pymongo import MongoClient
import pymongo
import json
import logging
from bson import BSON
from bson import json_util

logger = logging.getLogger(__name__)


class MongoRepository(object):
    
    def __init__(self, db_name, table_name, host="localhost", port=27017, username='', password=''):

        try:
            client = MongoClient(host, port)
            db = client[db_name]
            #db.authenticate(username, password)
            coll = db[table_name]
        except Exception as e:
            logger.error("Could not connect to MongoDB: %s" % e)
            raise e
        else:
            logger.info("Connected [mongodb://%s:%s/%s:%s] successfully!!!", host, port, db_name, table_name)

        self._coll = coll


    def insert(self, doc):
        self._coll.insert(doc)


    def find(self, conditions):
        single_doc = self._coll.find_one(conditions)
        json_doc = json.dumps(single_doc,default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(json_doc)

    def list_all(self, conditions=None, sort_index ='_id', limit=100):
        if conditions is None:
            conditions = {}

        all_docs =  self._coll.find(conditions).sort(sort_index, pymongo.DESCENDING).limit(limit)

        json_doc = json.dumps(list(all_docs),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(str(json_doc))

    def update(self, where, update_doc):
        self._coll.update(where, {"$set": update_doc})

    def remove(self, where):
        self._coll.remove(where)