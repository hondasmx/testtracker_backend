from pymongo import MongoClient


class MongoLoader:
    _DOCUMENT_NAME_FIELD = 'document_name'
    _DATA_FIELD = 'data'
    _MONGO_HOST = 'localhost'
    _MONGO_PORT = 27017
    _DEFAULT_DATABASE = 'testcases'

    def __init__(self, collection_name, db=_DEFAULT_DATABASE):
        self.client = MongoClient(self._MONGO_HOST, self._MONGO_PORT)
        self.db = self.client[db]
        self.collection = self.db[collection_name]

    def add_dict(self, document_name, dictionary):
        result = self.get_dict(document_name)
        if result:
            self.delete_dict(document_name)
        return self.collection.insert({self._DOCUMENT_NAME_FIELD: document_name,
                                       self._DATA_FIELD: dictionary})

    def delete_dict(self, template_name):
        return self.collection.remove({self._DOCUMENT_NAME_FIELD: template_name})

    def get_dict(self, document_name):
        document = self.collection.find_one({self._DOCUMENT_NAME_FIELD: document_name})
        if document:
            return document[self._DATA_FIELD]


def get_collection(collection):
    return MongoLoader(collection)
