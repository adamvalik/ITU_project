from pydantic import BaseModel

class Map(BaseModel):
  satek: str

class Game(BaseModel):
  # timer false and wins 0 for the classic mode, custom mode will set these
  timer: bool = False
  time: int = 30 # initial time for the timer
  wins: int = 0
  wind: int = 0
  map: Map

class Ammunition(BaseModel):
  name: str
  damage: int
  radius: int
  cost: int

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

  # toto nekde jinde jak se bude strilet
  # shellAngle: int
  # shellPower: int

class Settings(BaseModel):
  musicVolume: int = 50
