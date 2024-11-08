from pydantic import BaseModel

class Game(BaseModel):
  isTimer: bool = False
  timePerRound: int = 30 # initial time for the timer
  toWins: int = 0
  wind: int = 0
  mapName: str = ""

class CustomMode(BaseModel):
  isTimer: bool
  timePerRound: int
  toWins: int
