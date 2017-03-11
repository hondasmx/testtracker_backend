import json

from pymongo import MongoClient


class MongoLoader:
    _DOCUMENT_NAME_FIELD = 'document_name'
    _DATA_FIELD = 'data'
    _MONGO_HOST = 'localhost'
    _MONGO_PORT = 27017

    def __init__(self, collection_name, database):
        self.client = MongoClient(self._MONGO_HOST, self._MONGO_PORT)
        self.db = self.client[database]
        self.database = database
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

    def get_document_names(self):
        return [dict[self._DOCUMENT_NAME_FIELD] for dict in self.collection.find()]

    def get_collections(self):
        return self.client[self.database].collection_names()

    def update_document(self, document_name, field, new_value):
        return self.collection.update_one({
            'document_name': document_name
            },
            {
                '$set': {
                    'data.{}'.format(field): new_value
                }
            })


def get_collection(collection, database):
    return MongoLoader(collection, database)
