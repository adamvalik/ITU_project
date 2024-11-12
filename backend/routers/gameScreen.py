from fastapi import APIRouter, HTTPException, Depends
from models.playground import PracticeTarget
from models.player import Player
from models.player import PlayerData
from models.playground import MissileComputationData, MissileComputationResponse
from managers.practiceTargetManager import PracticeTargetManager
from managers.playerManager import PlayerManager
from pydantic import BaseModel
from models.map import Map
from redisClient import get_redis_client
import math
from typing import List, Tuple

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

@router.post("/save-current-player-data")
async def save_current_player_data(currentPlayer: PlayerData, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.delete_player(currentPlayer.player.id)
    player_manager.create_player(currentPlayer.player)
    return {"message": "Successfully saved player data"}


@router.post("/compute-missile-data", response_model=MissileComputationResponse)
async def compute_missile_data(missileData: MissileComputationData, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player = player_manager.get_player(missileData.playerId)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    player_manager.delete_player(player.id)
    
    #Decrement ammunition count
    player.ammunitionCount[missileData.weaponSelected] -= 1

    
    returnModel = MissileComputationResponse(ammunitionCount=player.ammunitionCount[missileData.weaponSelected])
    player_manager.create_player(player)
    return returnModel
