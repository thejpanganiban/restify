from datetime import datetime
import pymongo
from bson.objectid import ObjectId

from ..interface import Engine
from ..utils import logger


class MongodbEngine(Engine):
    def __init__(self):
        self.db_name = 'restify'
        self.mongodb = pymongo.Connection()[self.db_name]

    def create(self, collection_name, raw_object):
        mongo_obj = MongodbObject(self.mongodb[collection_name], raw_object)
        mongo_obj.save()
        return mongo_obj

    def list_collections(self):
        return self.mongodb.collection_names()

    def query_collection(self, collection_name, lookup=None):
        logger.debug(lookup)
        result = self.mongodb[collection_name].find(lookup)
        if result:
            return [
                MongodbObject(self.mongodb[collection_name], raw_obj).to_dict()
                    for raw_obj in result]
        return None

    def get_by_id(self, collection_name, obj_id):
        return MongodbObject.get_by_id(self.mongodb[collection_name], obj_id)

    def update(self, collection_name, new_raw_data, obj_id):
        self.mongodb[collection_name].update({'_id': ObjectId(obj_id)},
                                             {'$set': new_raw_data})
        return self.get_by_id(collection_name, obj_id)


class MongodbObject(object):

    id = None
    attrs = ['id']

    def __init__(self, collection, pymongo_object):
        self.collection = collection
        self._set_attrs(pymongo_object)

    def _set_attrs(self, pymongo_object):
        for key, value in pymongo_object.iteritems():
            if key == '_id':
                setattr(self, 'id', str(value))
            else:
                setattr(self, key, value)
                self.attrs.append(key)

    def save(self):
        self.attrs.extend(['createdAt', 'updatedAt'])
        setattr(self, 'createdAt', datetime.utcnow().isoformat())
        data = self.to_dict(exclude_fields=['id'])
        data.update({'createdAt': self.createdAt,
                     'updatedAt': ''})
        print data
        self.id = str(self.collection.insert(data))

    @classmethod
    def get_by_id(cls, collection, object_id):
        obj = collection.find_one({'_id': ObjectId(object_id)})
        if obj:
            return cls(collection, obj)
        else:
            return None

    def delete(self):
        return self.collection.remove(ObjectId(self.id))

    def to_dict(self, exclude_fields=None):
        data = {}
        for attr in self.attrs:
            if exclude_fields and attr not in exclude_fields \
                or not exclude_fields:
                data[attr] = getattr(self, attr, '')
        return data
