import redis
from django.conf import settings

redis_pool = redis.ConnectionPool(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    db=getattr(settings, 'REDIS_DB', 0),
)


def get_redis():
    return redis.StrictRedis(connection_pool=redis_pool)
