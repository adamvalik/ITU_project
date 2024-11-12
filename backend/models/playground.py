from pydantic import BaseModel

class PracticeTarget(BaseModel):
    name: str
    xCord: int
    yCord: int
    health: int
    color: str

class MissileComputationData(BaseModel):
    canvasWidth: int
    canvasHeight: int
    playerId: int
    terrain: list[float]
    angle: float
    power: float
    wind: int
    weaponSelected: int
    radius: int
    damage: int
    targetHealth: int
    targetXCord: float
    targetYCord: float

class MissileComputationResponse(BaseModel):
    ammunitionCount: int = 0
    hitTerrain: bool = False
    hitPlayer: bool = False
    newTerrain: list[float] = []
    missileTrajectory: list[tuple[float, float]] = []
    gameOver: bool = False
    targetHealth: int = 0
    playerMoney: int = 0