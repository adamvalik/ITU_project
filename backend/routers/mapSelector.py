from fastapi import APIRouter, Depends
from typing import List
from managers.mapCreatorManager import MapCreatorManager
from redisClient import get_redis_client

router = APIRouter()

@router.get("/map/names", response_model=List[str])
async def get_map_names(redis_client = Depends(get_redis_client)):
    mapManager = MapCreatorManager(redis_client)
    return mapManager.get_map_names()

@router.get("/map/type/{map_name}", response_model=str)
async def get_map_type(map_name: str, redis_client = Depends(get_redis_client)):
    mapManager = MapCreatorManager(redis_client)
    return mapManager.get_type(map_name)
