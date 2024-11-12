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
    returnModel = MissileComputationResponse()
    
    #Decrement ammunition count
    player.ammunitionCount[missileData.weaponSelected] -= 1
    returnModel.ammunitionCount = player.ammunitionCount[missileData.weaponSelected]

    #Set missile data
    startX = player.xCord
    startY = player.yCord - 15
    controlX = startX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + missileData.wind * 4
    controlY = startY - math.sin(missileData.angle * (math.pi / 180)) * missileData.power * 12
    endX = controlX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + missileData.wind * 8
    endY = missileData.canvasHeight


    # missile["endX"] = missile["controlX"] + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 16 + missileData.wind * 2
    missileTrajectory = []

    t = 0.00

    while t <= 1:
        x = (1 - t) * (1 - t) * startX + 2 * (1 - t) * t * controlX + t * t * endX
        y = (1 - t) * (1 - t) * startY + 2 * (1 - t) * t * controlY + t * t * endY
        t += 0.01
        missileTrajectory.append((x, y))

        if 0 <= math.floor(x) < len(missileData.terrain) and y >= missileData.terrain[math.floor(x)]:
            returnModel.hitTerrain = True

            dx = missileData.targetXCord - x
            dy = missileData.targetYCord - y
            distance = math.sqrt(dx * dx + dy * dy)

            #Player hit
            if distance <= missileData.radius + 20:
                returnModel.hitPlayer = True
                player.money += 200
                returnModel.playerMoney = 200
                missileData.targetHealth -= missileData.damage
                if(missileData.targetHealth < 0):
                    returnModel.targetHealth = 0
                else:
                    returnModel.targetHealth = missileData.targetHealth
            
                if missileData.targetHealth <= 0:
                    returnModel.gameOver = True


            explosionRadius = missileData.radius
            for i in range(-explosionRadius, explosionRadius):
                pos = math.floor(x) + i
                if pos >= 0 and pos < missileData.canvasWidth:
                    distance = math.sqrt(i * i)
                    if distance <= explosionRadius:
                        impactDepth = math.sqrt(explosionRadius * explosionRadius - distance * distance)
                        missileData.terrain[pos] = max(missileData.terrain[pos], y + impactDepth)
        
            break

        
    
    returnModel.newTerrain = missileData.terrain
    returnModel.missileTrajectory = missileTrajectory
    player_manager.create_player(player)
    return returnModel