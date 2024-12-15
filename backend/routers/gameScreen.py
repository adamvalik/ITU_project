# File: gameScreen.py
# Description: API endpoints for the game screen
# Author: Samuel Hejnicek (xhejni00)

from fastapi import APIRouter, HTTPException, Depends
from models.player import Player
from models.player import PlayersData
from models.missile import Missile, MissileComputationData, MissileComputationResponse, Laser, Movement, MovementResponse
from managers.missileManager import MissileManager
from managers.playerManager import PlayerManager
from managers.gameManager import GameManager
from managers.mapCreatorManager import MapCreatorManager
from managers.mapManager import MapManager
from pydantic import BaseModel
from models.map import Map
from redisClient import get_redis_client
import math
from typing import List, Tuple

router = APIRouter()

# Return all missiles from the database
@router.get("/missiles", response_model=List[Missile])
async def get_missiles():
    missile_manager = MissileManager(get_redis_client())
    missiles = missile_manager.get_missiles()
    if not missiles:
        raise HTTPException(status_code=404, detail="Missiles not found")
    return missiles

@router.post("/calculate-laser-pos", response_model=Tuple[float, float])
async def calculate_laser_pos(laserData: Laser):

    distance = (laserData.power / 100) * laserData.aimCircleRadius

    angleInRadians = 0
    if laserData.p1Turn:
        angleInRadians = (-laserData.angle * math.pi) / 180
    else:
        angleInRadians = (-(180 - laserData.angle) * math.pi) / 180

    aimLaserXCord = laserData.playerXCord + distance * math.cos(angleInRadians)
    aimLaserYCord = laserData.playerYCord + distance * math.sin(angleInRadians)

    return (aimLaserXCord, aimLaserYCord)

@router.post("/keyboard-movement", response_model=MovementResponse)
async def keyboard_movement(movementData: Movement, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    game_manager = GameManager(redis_client)
    currentGame = game_manager.get_game()
    currentPlayer = None
    if currentGame.p1Turn:
        currentPlayer = player_manager.get_player(1)
    else:
        currentPlayer = player_manager.get_player(2)
    if not currentPlayer:
        raise HTTPException(status_code=404, detail="Player not found")

    responseModel = MovementResponse(aimLaserXCord=movementData.aimLaserXCord, power=movementData.power, angle=movementData.angle, shoot=False, playerXCord=currentPlayer.xCord, playerFuel=currentPlayer.fuel)
    moveConstant = 5
    if currentPlayer.speedSkill > 0:
        moveConstant = 7
    elif currentPlayer.speedSkill > 1:
        moveConstant = 9
    elif currentPlayer.speedSkill > 2:
        moveConstant = 11

    if movementData.key == "d":
        if currentPlayer.fuel > 0 and currentPlayer.xCord <  movementData.canvasWidth - 25:
            currentPlayer.fuel -= 5
            currentPlayer.xCord += moveConstant

            responseModel.aimLaserXCord += 5
            responseModel.playerXCord += moveConstant
            responseModel.playerFuel -= 5
    elif movementData.key == "a":
        if currentPlayer.fuel > 0 and currentPlayer.xCord > 25:
            currentPlayer.fuel -= 5
            currentPlayer.xCord -= moveConstant

            responseModel.aimLaserXCord -= 5
            responseModel.playerXCord -= moveConstant
            responseModel.playerFuel -= 5
    elif movementData.key == "ArrowRight":
        responseModel.power = min(100, responseModel.power + 1)
    elif movementData.key == "ArrowLeft":
        responseModel.power = max(1, responseModel.power - 1)
    elif movementData.key == "ArrowUp":
        responseModel.angle += 1
    elif movementData.key == "ArrowDown":
        responseModel.angle -= 1
    elif movementData.key == " ":
        responseModel.shoot = True

    player_manager.delete_player(currentPlayer.id)
    player_manager.create_player(currentPlayer)
    return responseModel

# Generate terrain for the game
@router.get("/obtain-terrain-data", response_model=Map)
async def generate_terrain(canvasWidth: int, canvasHeight: int, redis_client = Depends(get_redis_client)):
    
    gameManager = GameManager(redis_client)
    mapCreatorManager = MapCreatorManager(redis_client)
    mapManager = MapManager(redis_client)

    game = gameManager.get_game()

    # Default color
    mapColor = "#0D8747"
    mapBackground = "#D5EFF4"

    if game.weather == "Cloudy:":
        mapBackground = "#CCCCCC"
    elif game.weather == "Extreme":
        mapBackground = "#545454"

    if game.mapName == "__forest":
        mapColor = "#0D8747"
    elif game.mapName == "__beach":
        mapColor = "#E8BD3A"
    elif game.mapName =="__winter":
        mapColor = "#9EDFFA"
    else:
        savedMap = mapCreatorManager.get_map(game.mapName)
        if savedMap:
            if savedMap.type == "forest":
                mapColor = "#0D8747"
            elif savedMap.type  == "beach":
                mapColor = "#E8BD3A"
            else:
                mapColor = "#9EDFFA"
                
    maxTerrainHeight = (canvasHeight * 2) / 3
    
    terrain = []
    for x in range(canvasWidth):
        baseHeight = maxTerrainHeight
        variation = (math.sin(x * 0.06) * 15 + math.sin(x * 0.1) * 10 + math.sin(x * 0.01) * 50)
        terrain.append(baseHeight + variation)
    newMap = Map(name=game.mapName, type=mapColor, data=terrain, background=mapBackground)
    mapManager.delete_map()
    mapManager.create_map(newMap)
    return newMap

@router.get("/obtain-updated-map")
async def obtain_updated_map(redis_client = Depends(get_redis_client)):
    mapManager = MapManager(redis_client)
    currentMap = mapManager.get_map()
    return currentMap

# Save both players data to the database
@router.post("/save-current-players-data")
async def save_current_player_data(players: PlayersData, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.delete_player(players.player1.id)
    player_manager.create_player(players.player1)
    player_manager.delete_player(players.player2.id)
    player_manager.create_player(players.player2)
    return {"message": "Successfully saved player data"}


# Compute missile data
@router.post("/compute-missile-data", response_model=MissileComputationResponse)
async def compute_missile_data(missileData: MissileComputationData, redis_client = Depends(get_redis_client)):

    # Obtain shooting player model and active missile from the database
    player_manager = PlayerManager(redis_client)
    missile_manager = MissileManager(redis_client)
    map_manager = MapManager(redis_client)
    game_manager = GameManager(redis_client)
    p1Turn = game_manager.get_game().p1Turn

    playerShooter = None
    playerTarget = None

    if p1Turn:
        playerShooter = player_manager.get_player(1)
        playerTarget = player_manager.get_player(2)
    else:
        playerShooter = player_manager.get_player(2)
        playerTarget = player_manager.get_player(1)

    activeMissile = missile_manager.get_missile(missileData.weaponSelected)
    currentMap = map_manager.get_map()
    mapData = currentMap.data

    # Delete players from the database, so they are added later with updated data
    player_manager.delete_player(playerShooter.id)
    player_manager.delete_player(playerTarget.id)

    # Create return model
    returnModel = MissileComputationResponse()

    # Decrement ammunition count
    playerShooter.ammunitionCount[missileData.weaponSelected] -= 1
    returnModel.ammunitionCount = playerShooter.ammunitionCount[missileData.weaponSelected]

    if playerShooter.ammunitionCount[missileData.weaponSelected] < 0:
        returnModel.noAmmunition = True
        return returnModel

    # Recalculate angle for player 2
    if not p1Turn:
        missileData.angle = 180 - missileData.angle
        if missileData.angle > 180:
            missileData.angle -= 360


    wind = game_manager.get_game().wind

    # Define missile trajectory using Bezier curve
    startX = playerShooter.xCord
    startY = playerShooter.yCord - 15
    controlX = startX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + wind * 4
    controlY = startY - math.sin(missileData.angle * (math.pi / 180)) * missileData.power * 12
    endX = controlX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + wind * 8

    # + 20 pixels to be able to have the y size to reach the size of canvas height
    endY = missileData.canvasHeight + 20

    missileTrajectory = []

    t = 0.00

    # Calculate missile trajectory
    while t <= 1:
        x = (1 - t) * (1 - t) * startX + 2 * (1 - t) * t * controlX + t * t * endX
        y = (1 - t) * (1 - t) * startY + 2 * (1 - t) * t * controlY + t * t * endY
        t += 0.01
        missileTrajectory.append((x, y))

        # Check if missile hit terrain
        if 0 <= math.floor(x) < len(mapData) and y >= mapData[math.floor(x)]:

            dx = playerTarget.xCord - x
            dy = playerTarget.yCord - y
            distance = math.sqrt(dx * dx + dy * dy)

            # Check if missile hit player
            if distance <= activeMissile.radius + 20:
                playerShooter.money += 200
                playerTarget.health -= activeMissile.damage

                if playerTarget.health <= 0:
                    returnModel.gameOver = True
                    playerShooter.wins += 1


            # Create explosion
            explosionRadius = activeMissile.radius
            for i in range(-explosionRadius, explosionRadius):
                pos = math.floor(x) + i
                if pos >= 0 and pos < missileData.canvasWidth:
                    distance = math.sqrt(i * i)
                    if distance <= explosionRadius:
                        impactDepth = math.sqrt(explosionRadius * explosionRadius - distance * distance)
                        mapData[pos] = max(mapData[pos], y + impactDepth)

                        # Leave small portion of terrain at the bottom of the canvas
                        if(mapData[pos] > missileData.canvasHeight - 10):
                            mapData[pos] = missileData.canvasHeight - 10

            # Break the loop because the explosion should be calculated for just one point
            break


    # Update return model
    returnModel.missileTrajectory = missileTrajectory

    # Switch turns
    p1Turn = not p1Turn
    game_manager.update_game({"p1Turn": p1Turn})


    map_manager.delete_map()
    newMap = Map(name=currentMap.name, type=currentMap.type, data=mapData, background=currentMap.background)
    map_manager.create_map(newMap)

    # Update players data
    player_manager.create_player(playerShooter)
    player_manager.create_player(playerTarget)
    return returnModel
