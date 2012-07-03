import logging


FORMAT = '%(asctime)s:%(filename)s(%(lineno)s):%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('Restify')
