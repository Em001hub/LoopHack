import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def get_cache(key):
    return r.get(key)
