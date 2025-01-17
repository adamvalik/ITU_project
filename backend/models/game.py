from pydantic import BaseModel

# toWins = 0 is indicating classic mode (also without timer)

class Game(BaseModel):
  isTimer: bool = False
  timePerTurn: int = 3000 # initial time for the timer
  toWins: int = 0
  wind: int = 0
  mapName: str = "" # "__forest", "__beach", "__winter"
  weather: str = "Cloudy" # "Sunny", "Cloudy", "Extreme"
  p1Turn: bool = True
  aimCircleRadius: int = 200

class CustomMode(BaseModel):
  isTimer: bool
  timePerTurn: int
  toWins: int

class SetWeather(BaseModel):
  weather: str

class SetMap(BaseModel):
  mapName: str
