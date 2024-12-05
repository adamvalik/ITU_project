from fastapi import APIRouter, HTTPException, Depends
from models.player import Player
from models.player import PlayersData
from models.missile import Missile, MissileComputationData, MissileComputationResponse
from managers.missileManager import MissileManager
from managers.playerManager import PlayerManager
from pydantic import BaseModel
from models.map import Map
from redisClient import get_redis_client
import math
from typing import List, Tuple

router = APIRouter()


@router.get("/missiles", response_model=List[Missile])
async def get_missiles():
    missile_manager = MissileManager(get_redis_client())
    missiles = missile_manager.get_missiles()
    if not missiles:
        raise HTTPException(status_code=404, detail="Missiles not found")
    return missiles


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
async def save_current_player_data(players: PlayersData, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.delete_player(players.player1.id)
    player_manager.create_player(players.player1)
    player_manager.delete_player(players.player2.id)
    player_manager.create_player(players.player2)
    return {"message": "Successfully saved player data"}


@router.post("/compute-missile-data", response_model=MissileComputationResponse)
async def compute_missile_data(missileData: MissileComputationData, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    missile_manager = MissileManager(redis_client)

    playerShooter = player_manager.get_player(missileData.playerId)
    playerTarget = None
    activeMissile = missile_manager.get_missile(missileData.weaponSelected)

    if(missileData.playerId == 1):
        playerTarget = player_manager.get_player(2)
    else:
        playerTarget = player_manager.get_player(1)

    if not playerShooter or not playerTarget:
        raise HTTPException(status_code=404, detail="Player not found")
    
    player_manager.delete_player(playerShooter.id)
    player_manager.delete_player(playerTarget.id)
    returnModel = MissileComputationResponse()
    
    #Decrement ammunition count
    playerShooter.ammunitionCount[missileData.weaponSelected] -= 1
    returnModel.ammunitionCount = playerShooter.ammunitionCount[missileData.weaponSelected]

    # if playerShooter.ammunitionCount[missileData.weaponSelected] < 0:
    #     return

    if missileData.playerId == 2:
        missileData.angle = 180 - missileData.angle
        if missileData.angle > 180:
            missileData.angle -= 360

    #Set missile data
    startX = playerShooter.xCord
    startY = playerShooter.yCord - 15
    controlX = startX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + missileData.wind * 4
    controlY = startY - math.sin(missileData.angle * (math.pi / 180)) * missileData.power * 12
    endX = controlX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + missileData.wind * 8
    endY = missileData.canvasHeight

    missileTrajectory = []

    t = 0.00

    while t <= 1:
        x = (1 - t) * (1 - t) * startX + 2 * (1 - t) * t * controlX + t * t * endX
        y = (1 - t) * (1 - t) * startY + 2 * (1 - t) * t * controlY + t * t * endY
        t += 0.01
        missileTrajectory.append((x, y))

        if 0 <= math.floor(x) < len(missileData.terrain) and y >= missileData.terrain[math.floor(x)]:
            returnModel.hitTerrain = True

            dx = playerTarget.xCord - x
            dy = playerTarget.yCord - y
            distance = math.sqrt(dx * dx + dy * dy)

            #Player hit
            if distance <= activeMissile.radius + 20:
                returnModel.hitPlayer = True
                playerShooter.money += 200
                returnModel.playerMoney = 200
                playerTarget.health -= activeMissile.damage
                if(playerTarget.health < 0):
                    returnModel.targetHealth = 0
                else:
                    returnModel.targetHealth = playerTarget.health
            
                if playerTarget.health <= 0:
                    returnModel.gameOver = True


            explosionRadius = activeMissile.radius
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
    player_manager.create_player(playerShooter)
    player_manager.create_player(playerTarget)
    return returnModel