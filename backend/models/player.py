from pydantic import BaseModel

class Player(BaseModel):
  id: int
  name: str
  tankType: int
  color: str
  armorSkill: int = 0
  powerSkill: int = 0
  speedSkill: int = 0
  skillPoints: int = 6
  wins: int = 0
  money: int = 2000
  fuel: int = 250
  fuelMax: int = 250
  health: int = 100
  healthMax: int = 100
  ammunitionCount: list[int] = [30,-1, 20]
  xCord: float = 0
  yCord: float = 0
  activeMissileId: int = 0
  angle: float = 45
  power: float = 50
  aimLaserXCord: float = 0
  aimLaserYCord: float = 0

class PlayersData(BaseModel):
  player1: Player
  player2: Player

class UpdateName(BaseModel):
  player: int
  name: str

class UpdateTankType(BaseModel):
  player: int
  tankType: int

class UpdateColor(BaseModel):
  player: int
  color: str

class UpdateSkill(BaseModel):
  player: int
  skill: str
  value: int

class UpdateSkillPoints(BaseModel):
  player: int
  skillPoints: int

class IncreaseSkillPoints(BaseModel):
  player: int

class BuyAmmo(BaseModel):
  player: int
  ammo_type: int
  price: int