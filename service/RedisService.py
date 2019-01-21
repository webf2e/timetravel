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

def setSetting(key,value):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    r.hset("setting",key,value)

def getSetting(key):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    val = r.hget("setting",key)
    if None != val:
        return val.decode("utf-8")
    return None

def setTongji(key,value):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    r.hset("tongji",key,value)

def getTongji(key):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    val = r.hget("tongji",key)
    if None != val:
        return val.decode("utf-8")
    return None

def getSettings():
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    resultMap = {}
    dataMap = r.hgetall("setting")
    for k,v in dataMap.items():
        resultMap[k.decode("utf-8")] = v.decode("utf-8")
    return resultMap


def isSettingExist(key):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    return r.hexists("setting",key)