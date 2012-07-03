import abc


class Engine(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self):
        """ create new object and return it. """
        return

    @abc.abstractmethod
    def list_collections(self):
        """ return list of collections. """
        return

    @abc.abstractmethod
    def query_collection(self, collection_name, lookup=None):
        """
        return list of objects on the specified collection,
        and filter by lookup if specified.
        """
        return

    @abc.abstractmethod
    def get_by_id(self, collection_name, obj_id):
        """ get object by its id. """
        return

    @abc.abstractmethod
    def update(self, collection_name, new_raw_data, obj_id):
        """
        update object matching obj_id under collection_name
        using new_raw_data.
        """
        return
