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
  money: int = 0
  fuel: int = 250
  fuelMax: int = 250
  health: int = 100
  ammunitionCount: list[int] = [0,0,0]
  xCord: int = 0
  yCord: int = 0
