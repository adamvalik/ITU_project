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
  wins: int = 1
  money: int = 2000
  fuel: int = 250
  fuelMax: int = 250
  health: int = 100
  ammunitionCount: list[int] = [20,-1, 10]
  xCord: int = 120
  yCord: int = 140
