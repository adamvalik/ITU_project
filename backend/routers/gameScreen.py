from fastapi import APIRouter, HTTPException, Depends
from models.player import Player
from models.player import PlayersData
from models.missile import Missile, MissileComputationData, MissileComputationResponse, Laser, Movement, MovementResponse
from managers.missileManager import MissileManager
from managers.playerManager import PlayerManager
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
    currentPlayer = player_manager.get_player(movementData.playerId)
    if not currentPlayer:
        raise HTTPException(status_code=404, detail="Player not found")

    responseModel = MovementResponse(aimCircleXCord=movementData.aimCircleXCord, power=movementData.power, angle=movementData.angle, shoot=False, playerXCord=currentPlayer.xCord, playerFuel=currentPlayer.fuel)

    if movementData.key == "d":
        if currentPlayer.fuel > 0 and currentPlayer.xCord <  movementData.canvasWidth - 25:
            currentPlayer.fuel -= 5
            currentPlayer.xCord += 5

            responseModel.aimCircleXCord += 5
            responseModel.playerXCord += 5
            responseModel.playerFuel -= 5
    elif movementData.key == "a":
        if currentPlayer.fuel > 0 and currentPlayer.xCord > 25:
            currentPlayer.fuel -= 5
            currentPlayer.xCord -= 5

            responseModel.aimCircleXCord -= 5
            responseModel.playerXCord -= 5
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

    player_manager.delete_player(movementData.playerId)
    player_manager.create_player(currentPlayer)
    return responseModel

# Generate terrain for the game
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
    playerShooter = player_manager.get_player(missileData.playerId)
    activeMissile = missile_manager.get_missile(missileData.weaponSelected)

    # Obtain target player
    playerTarget = None
    if(missileData.playerId == 1):
        playerTarget = player_manager.get_player(2)
    else:
        playerTarget = player_manager.get_player(1)

    if not playerShooter or not playerTarget:
        raise HTTPException(status_code=404, detail="Player not found")

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
    if missileData.playerId == 2:
        missileData.angle = 180 - missileData.angle
        if missileData.angle > 180:
            missileData.angle -= 360

    # Define missile trajectory using Bezier curve
    startX = playerShooter.xCord
    startY = playerShooter.yCord - 15
    controlX = startX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + missileData.wind * 4
    controlY = startY - math.sin(missileData.angle * (math.pi / 180)) * missileData.power * 12
    endX = controlX + math.cos(missileData.angle * (math.pi / 180)) * missileData.power * 12 + missileData.wind * 8

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
        if 0 <= math.floor(x) < len(missileData.terrain) and y >= missileData.terrain[math.floor(x)]:

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
                        missileData.terrain[pos] = max(missileData.terrain[pos], y + impactDepth)

                        # Leave small portion of terrain at the bottom of the canvas
                        if(missileData.terrain[pos] > missileData.canvasHeight - 10):
                            missileData.terrain[pos] = missileData.canvasHeight - 10

            # Break the loop because the explosion should be calculated for just one point
            break


    # Update return model
    returnModel.newTerrain = missileData.terrain
    returnModel.missileTrajectory = missileTrajectory

    # Update players data
    player_manager.create_player(playerShooter)
    player_manager.create_player(playerTarget)
    return returnModel
