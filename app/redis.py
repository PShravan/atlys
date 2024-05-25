class DummyRedis:
    def __init__(self) -> None:
        self.store = {}

    def set(self, key, value):
        self.store[key] = value
        return True

    def get(self, key):
        return self.store.get(key)


# Connect to Redis
# import aioredis
# async def get_redis():
#     redis = await aioredis.create_redis_pool('redis://localhost')
#     return redis

def get_redis():
    redis = DummyRedis()
    return redis


def redis_set_key(key, value):
    redis = get_redis()
    redis.set(key, value)


def redis_get_key(key):
    redis = get_redis()
    return redis.get(key)
