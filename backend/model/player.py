from pydantic import BaseModel

class Ammunition(BaseModel):
  name: str
  damage: int
  radius: int
  cost : int

class GameMap(BaseModel):
    wind: int
    canvasWidth: int
    canvasHeight: int
    time: int

class Player(BaseModel):
  name: str
  tankType: int
  color: str
  armorSkill: int
  powerSkill: int
  speedSkill: int
  skillPoints: int
  wins: int
  money: int
  fuel: int
  fuelMax: int
  health: int 
  ammunitionCount: list[int] # 0 for no shells, -1 for shell that user does not have 

  xCord: int
  yCord: int
  shellAngle: int
  shellPower: int

players = []