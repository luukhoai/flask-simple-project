import os
import logging
from flask import Flask
from redis import ConnectionPool

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
redis_pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = Flask(__name__)

