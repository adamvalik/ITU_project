from fastapi import APIRouter, Depends
from redis import Redis
from redisClient import get_redis_client

router = APIRouter()

# debug routes, for seeing the current data in Redis
# just type localhost:8000/debug/satek in your browser to see desired data from Redis
# or implement own debug route

@router.get("/debug/keys")
async def get_all_keys(redis_client: Redis = Depends(get_redis_client)):
    keys = redis_client.keys("*")
    return {"keys": keys}

@router.get("/debug/player/{player_id}")
async def get_player_data(player_id: int, redis_client: Redis = Depends(get_redis_client)):
    key = f"player:{player_id}"
    player_data = redis_client.hgetall(key)
    return player_data

@router.get("/debug/player/{player_id}/field/{field}")
async def get_player_field(player_id: int, field: str, redis_client: Redis = Depends(get_redis_client)):
    key = f"player:{player_id}"
    field_data = redis_client.hget(key, field)
    return field_data

@router.get("/debug/game")
async def get_game_data(redis_client: Redis = Depends(get_redis_client)):
    key = "game"
    game_data = redis_client.hgetall(key)
    return game_data
