from pymongo import MongoClient

class MongoRepository(object):
    
    def __init__(self, database, collection, url=None):

        if url is None:
            url = 'mongodb://localhost:27017/'

        try:
            conn = MongoClient(url)
            coll = conn[database][collection]
        except Exception as e:
            print "Could not connect to MongoDB: %s" % e
        else:
            print "Connected successfully!!!"

        self._coll = coll


    def insert(self, doc):
        self._coll.insert(doc)


    def find(self, query):
        cur = self._coll.find(query)
        return cur

    def list_all(self, query=None):
        if query is None:
            query = {}
        return self._coll.find(query)

    def update(self, query, update_doc):
        self._coll.update(query, {"$set": update_doc})

    def remove(self, query):
        self._coll.remove(query)