# File: missile.py
# Description: Models for missile, laser and movement computation
# Author: Samuel Hejnicek (xhejni00)

from pydantic import BaseModel

# Input data for missile computation
class MissileComputationData(BaseModel):
    canvasWidth: int
    canvasHeight: int

# Response data for missile computation
class MissileComputationResponse(BaseModel):
    ammunitionCount: int = 0
    missileTrajectory: list[tuple[float, float]] = []
    gameOver: bool = False
    noAmmunition: bool = False

# Missile model
class Missile(BaseModel):
    id: int
    name: str
    damage: int
    radius: int
    price: int
    picture: str

# Input data for laser computation
class Laser(BaseModel):
    power: float
    angle: float
    p1Turn: bool
    playerXCord: float
    playerYCord: float
    aimCircleRadius: int

# Input data for movement computation
class Movement(BaseModel):
    key: str
    canvasWidth: int
    canvasHeight: int
    power: float
    angle: float

# Response data for movement computation
class MovementResponse(BaseModel):
    aimLaserXCord: float
    power: float
    angle: float
    shoot: bool
    playerXCord: float
    playerFuel: int

# Input data for current missile
class CurrentMissile(BaseModel):
    id: int
