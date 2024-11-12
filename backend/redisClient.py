from redis import Redis

redis_client = Redis(host="itu_redis", port=6379, db=0, decode_responses=True)

def get_redis_client():
    return redis_client
