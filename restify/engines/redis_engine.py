import redis
from ..interface import Engine
from ..utils import logger


class RedisEngine(Engine):
    def __init__(self):
        self.redis = redis.StrictRedis()

    def list_collections(self):
        try:
            return self.redis.keys()
        except redis.exceptions.ConnectionError, e:
            logger.error(e)
        return []

    def list_objects(self, collection):
        return self.redis.type(name=collection)

    def query_collection(self, collection, query=None):
        if not self.redis.exists(collection):
            return {'result': [], 'message': 'Does not exist.'}
        if query and 'name' not in query:
            return {'result': [], 'message': 'Invalid query.'}
        logger.debug("Querying for: %s" % query)
        # TODO: finish this method
