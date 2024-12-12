from fastapi import APIRouter, Depends
from typing import List
from managers.mapCreatorManager import MapCreatorManager
from managers.gameManager import GameManager
from models.game import SetMap, SetWeather
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

@router.get("/weather", response_model=str)
async def get_weather(redis_client = Depends(get_redis_client)):
    gameManager = GameManager(redis_client)
    return gameManager.get_weather()

@router.post("/weather")
async def set_weather(weather: SetWeather, redis_client = Depends(get_redis_client)):
    gameManager = GameManager(redis_client)
    gameManager.set_weather(weather.weather)

@router.post("/map/mapName")
async def set_map(map: SetMap, redis_client = Depends(get_redis_client)):
    gameManager = GameManager(redis_client)
    gameManager.set_map(map.mapName)

@router.get("/map/mapName", response_model=str)
async def get_map(redis_client = Depends(get_redis_client)):
    gameManager = GameManager(redis_client)
    return gameManager.get_map()
