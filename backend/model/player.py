from pydantic import BaseModel

class Player(BaseModel):
  name: str
  tankType: int
  color: str
  armour: int = 0
  power: int = 0
  speed: int = 0
  skillPoints: int = 0 
  money: int = 1000
  fuel: int = 250
  health: int = 100
  weapon1: int = 0
  weapon2: int = 0
  weapon3: int = 0
  
  
# class Game(BaseModel):
#   tackle: int
#   tackle_success: int
#   tackle_fail: int
#   foul: int
#   foul_suffered: int
#   yellow_card: int
#   red_card: int
  
# class Settings(BaseModel):
#   soundEffectsVolume: int


