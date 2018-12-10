import redis

host = "47.90.32.49"
port = 6379
pwd = "1234asdf.redis"

def set(key, val):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    r.set(key, str(val))

def setWithTtl(key, val, ttl):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    r.set(key, val)
    r.expire(key, ttl)

def get(key):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    val = r.get(key)
    if None != val:
        return r.get(key).decode("utf-8")
    return None

def isExist(key):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    return r.exists(key)