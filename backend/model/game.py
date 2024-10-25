from pydantic import BaseModel

class Game(BaseModel):
  mode: str = "classic"
  timer: bool = False
  wins: int = 0

game = Game()