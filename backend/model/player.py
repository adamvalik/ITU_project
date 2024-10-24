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

players = [
  Player(name="Aliceeeeeeee", tankType=4, color="#FF0000", armor=1, power=3, speed=1, money=1000, fuel=100, health=100, skillPoints=3, weapon1=3, weapon2=2, weapon3=1),
  Player(name="Bob", tankType=2, color="#00FF00", armor=0, power=3, speed=0, money=1000, fuel=100, health=100, skillPoints=3, weapon1=5, weapon2=4, weapon3=8),
]