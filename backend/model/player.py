from pydantic import BaseModel

class Player(BaseModel):
  name: str
  tankType: int
  color: str
  armor: int
  power: int
  speed: int
  skillPoints: int
  money: int
  fuel: int
  health: int 
  weapon1: int
  weapon2: int
  weapon3: int

players = []