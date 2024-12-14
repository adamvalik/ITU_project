from pydantic import BaseModel


# Input data for missile computation
class MissileComputationData(BaseModel):
    canvasWidth: int
    canvasHeight: int
    angle: float
    power: float
    wind: int
    weaponSelected: int

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

class Laser(BaseModel):
    power: float
    angle: float
    p1Turn: bool
    playerXCord: float
    playerYCord: float
    aimCircleRadius: int

class Movement(BaseModel):
    key: str
    canvasWidth: int
    canvasHeight: int
    aimCircleXCord: float
    power: float
    angle: float

class MovementResponse(BaseModel):
    aimCircleXCord: float
    power: float
    angle: float
    shoot: bool
    playerXCord: float
    playerFuel: int
