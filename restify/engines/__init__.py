from flask import jsonify
from .mongodb_engine import MongodbEngine
from .redis_engine import RedisEngine
from ..utils import logger


ENGINES = {
    'redis': RedisEngine,
    'mongodb': MongodbEngine
}


def _get_engine(engine_name):
    engine = ENGINES.get(engine_name, None)
    if not engine:
        logger.error("Invalid engine: %s" % engine_name)
    return engine()


def get_engine_or_fail(engine_name):
    engine = _get_engine(engine_name)
    if not engine:
        return False, 'Invalid engine.'
    return True, engine
