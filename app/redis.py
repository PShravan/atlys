import aioredis


# Connect to Redis
async def get_redis():
    redis = await aioredis.create_redis_pool('redis://localhost')
    return redis


def redis_set_key(key, value):
    redis = get_redis()
    redis.set(key, value)


def redis_get_key(key):
    redis = get_redis()
    redis.get(key)
