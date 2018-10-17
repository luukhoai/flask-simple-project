from redis import Redis
import pickle
from settings.settings import redis_pool


class RedisManager(object):

    def __init__(self):
        self.redis = Redis(connection_pool=redis_pool)

    def set(self, key, value, ex=None):
        """
        Set data into Redis
        :param key: eg: 'user_1', 'histories_1', ...
        :param value: eg: 'User name', ...
        :param ex: Timeout. default = None
        :return:
        """
        self.redis.set(key, pickle.dumps(value), ex=ex)
        return True

    def get(self, key):
        """
        Get value from Redis
        :param key: eg: 'user_1', 'histories_1'
        :return:
        """
        value = self.redis.get(key)
        if value:
            return pickle.loads(value)
        return None

    def scan(self, key):
        """
        Get list ordered key from Redis
        :param key: 'user_*', 'histories_*'
        :return: eg: ['user_1', 'user_2', ...]
        """
        bytes = self.redis.scan_iter(key)
        return sorted([byte.decode('utf-8') for byte in bytes])

    def close(self):
        pass