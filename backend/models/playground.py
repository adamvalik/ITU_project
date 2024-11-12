from pydantic import BaseModel

class PracticeTarget(BaseModel):
    name: str
    xCord: int
    yCord: int
    health: int
    color: str

class MissileComputationData(BaseModel):
    playerId: int
    terrain: list[float]
    angle: float
    power: float
    weaponSelected: int
    radius: int
    damage: int

class MissileComputationResponse(BaseModel):
    ammunitionCount: int