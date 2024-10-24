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

players = []