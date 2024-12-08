from pydantic import BaseModel


# Input data for missile computation
class MissileComputationData(BaseModel):
    canvasWidth: int
    canvasHeight: int
    playerId: int
    terrain: list[float]
    angle: float
    power: float
    wind: int
    weaponSelected: int

# Response data for missile computation
class MissileComputationResponse(BaseModel):
    ammunitionCount: int = 0
    newTerrain: list[float] = []
    missileTrajectory: list[tuple[float, float]] = []
    gameOver: bool = False

# Missile model
class Missile(BaseModel):
    id: int
    name: str
    damage: int
    radius: int
    price: int
    picture: str
