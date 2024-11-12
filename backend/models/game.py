from pydantic import BaseModel

# toWins = 0 is indicating classic mode (also without timer)

class Game(BaseModel):
  isTimer: bool = False
  timePerTurn: int = 3000 # initial time for the timer
  toWins: int = 0
  wind: int = 0
  mapName: str = ""

class CustomMode(BaseModel):
  isTimer: bool
  timePerTurn: int
  toWins: int
