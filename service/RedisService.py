import redis

host = "127.0.0.1"
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

def delete(key):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    if r.exists(key):
        return r.delete(key)
    return 0

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

def setMap(key,hash,value):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    r.hset(key,hash,value)

def getMapByKey(key):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    val = r.hgetall(key)
    if None != val:
        result = []
        keys = dict(val).keys()
        for key in keys:
            result.append(key.decode("utf-8"))
        return result
    return None

def getMapByHash(key,hash):
    pool = redis.ConnectionPool(host=host, port=port, password=pwd)
    r = redis.Redis(connection_pool=pool)
    val = r.hget(key,hash)
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