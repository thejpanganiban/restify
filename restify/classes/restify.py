from bson.objectid import ObjectId
import datetime


class RestifyObject(object):

    id = None
    attrs = ['id']

    def __init__(self, pymongo_object, connection=None, database_name=None,
        collection_name=None):
        self.connection = connection
        self.database_name = database_name
        self.collection_name = collection_name
        self._set_attrs(pymongo_object)

    def _set_attrs(self, pymongo_object):
        for key, value in pymongo_object.iteritems():
            if key == '_id':
                setattr(self, 'id', str(value))
            else:
                setattr(self, key, value)
                self.attrs.append(key)

    @property
    def collection(self):
        if self.connection and self.database_name and self.collection_name:
            return self.connection[self.database_name][self.collection_name]
        else:
            raise Exception('You need to set the connection, database_name, ' +
                ' and collection_name in order for you to access the collection.')

    @classmethod
    def create(cls, connection, database_name, collection_name, data):
        collection = connection[database_name][collection_name]
        data['createdAt'] = datetime.datetime.utcnow().isoformat()
        data['updatedAt'] = ''
        obj_id = collection.insert(data)
        obj = collection.find_one({'_id': obj_id})
        return cls(obj, connection, database_name, collection_name)

    @classmethod
    def get_by_id(cls, connection, database_name, collection_name, object_id):
        collection = connection[database_name][collection_name]
        obj = collection.find_one({'_id': ObjectId(object_id)})
        if obj:
            return cls(obj, connection, database_name, collection_name)
        else:
            return None

    def delete(self):
        self.collection.remove(ObjectId(self.id))
        return None

    def update(self, update_data, **kwargs):
        # FIXME: Perhaps a better solution can be made.
        # We now add an updatedAt attribute to the object.
        if update_data.get('$set'):
            # If update data uses set modifier, we merge the updatedAt with
            # the passed update_data $set modifier.
            set_modifier = update_data.get('$set').items()
            set_modifier.append(
                tuple(['updatedAt', datetime.datetime.utcnow().isoformat()]))
            update_data['$set'] = dict(set_modifier)
        else:
            update_data['$set'] = {'updatedAt': datetime.datetime.utcnow().isoformat()}
        self.collection.update({'_id': ObjectId(self.id)}, update_data, **kwargs)
        new_obj = self.collection.find_one({'_id': ObjectId(self.id)})
        self._set_attrs(new_obj)
        return self

    def to_dict(self):
        data = {}
        for attr in self.attrs:
            data[attr] = getattr(self, attr, '')
        return data


class RestifyCollection(object):

    def __init__(self, collection_data, object_class, connection=None,
        database_name=None, collection_name=None):
        self.result = [
            object_class(data, connection, database_name, collection_name)
                for data in collection_data]

    def to_dict(self):
        return {
            'result': [obj.to_dict() for obj in self.result]
        }

    @classmethod
    def query(cls, connection, database_name, collection_name,
        object_class=RestifyObject, **kwargs):
        collection = connection[database_name][collection_name]
        result = collection.find(**kwargs)
        return cls(result, object_class, connection, database_name, collection_name)
