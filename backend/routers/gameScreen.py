from fastapi import APIRouter, HTTPException, Depends
from models.practicetarget import PracticeTarget
from managers.practiceTargetManager import PracticeTargetManager
from pydantic import BaseModel
from models.map import Map
from redisClient import get_redis_client
import math

router = APIRouter()


@router.get("/practice-target", response_model=PracticeTarget)
async def get_practice_target(redis_client = Depends(get_redis_client)):
    practice_target_manager = PracticeTargetManager(redis_client)
    practice_target = practice_target_manager.get_practice_target()
    if not practice_target:
        raise HTTPException(status_code=404, detail="Practice targets not found")
    return practice_target


@router.get("/generate-terrain", response_model=Map)
async def generate_terrain(canvasWidth: int, canvasHeight: int):
    maxTerrainHeight = (canvasHeight * 2) / 3
    terrain = []
    for x in range(canvasWidth):
        baseHeight = maxTerrainHeight
        variation = (math.sin(x * 0.06) * 15 + math.sin(x * 0.1) * 10 + math.sin(x * 0.01) * 50)
        terrain.append(baseHeight + variation)
    newMap = Map(name="mapka", type="mud", data=terrain)
    return newMap