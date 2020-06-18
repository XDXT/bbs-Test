import json
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


class Cache(object):
    """
    java 接口，python应该不用这么写，有其他风格
    """
    def get(self, key):
        pass

    def set(self, key, value):
        pass


class RedisCache(Cache):
    """
    缓存数据库(内存)，待探究
    """
    redis_db = redis_client  # type: redis.Redis

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)

    def to_json(self, fields, obj):
        d = dict()
        for k in fields:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(obj, key)
        return json.dumps(d)

    def from_json(self, obj, j):
        d = json.loads(j)
        for k, v in d.items():
            setattr(obj, k, v)
        return obj
