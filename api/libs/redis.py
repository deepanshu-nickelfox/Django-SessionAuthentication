# python imports
import redis
import logging
# import time

# django imports
from django.conf import settings

HOST = settings.REDIS_CONFIG['HOST']
PORT = settings.REDIS_CONFIG['PORT']
DB = settings.REDIS_CONFIG['DB']
PASSWORD = settings.REDIS_CONFIG['PASSWORD']

logger = logging.getLogger(__name__)

class MyRedisClient(object):
    """
    Redis client for Leads app
    """
    def __init__(self, host=HOST, port=PORT, db=DB, password=PASSWORD):
        """
        Init of redis client
        """
        pool = redis.ConnectionPool(
            socket_timeout=10,
            socket_connect_timeout=10,
            host=host,
            port=port,
            db=db,
            password=password,
           decode_responses=True,
        )

        self.client = redis.Redis(connection_pool=pool)

        # print(host,port,self.client)

    def store_data(self, hash_key, data):
        """
        Store data into hash_key - HMSET
        """
        try:
            self.client.hmset(hash_key, data)
        except redis.exceptions.RedisError:
            logger.error("Redis: store_data RedisError ", exc_info=True)

    def remove_data(self, hash_key, field):
        """
        Remove field from hash_key - HDEL
        redisClient.hdel(hashName, key)
        """
        try:
            print(hash_key,field)
            self.client.hdel(hash_key, field)
        except redis.exceptions.RedisError:
            logger.error("Redis: remove_data RedisError ", exc_info=True)

    def get_data(self,hash_key):
        """
        Get all disc from hash_key
        """
        try:
            return self.client.hgetall(hash_key)
        except redis.exceptions.RedisError:
            logger.error("Redis: get_data RedisError ", exc_info=True)

