from pydantic import BaseModel

class Player(BaseModel):
  name: str
  age: int
  position: str
  club: str
  country: str
  foot: str
  value: int
  wage: int
  rating: int
  potential: int
  image: str
  
class Game(BaseModel):
  tackle: int
  tackle_success: int
  tackle_fail: int
  foul: int
  foul_suffered: int
  yellow_card: int
  red_card: int
  
class Settings(BaseModel):
  difficulty: str
  volume: int
  commentary: str
  music: str
  sfx: str
  controller: str
  camera: str