# File: map.py
# Description: Base model for the game map
# Author: Samuel Hejnicek (xhejni00)


from pydantic import BaseModel
class Map(BaseModel):
  name: str
  type: str = "forest"
  background: str = "#D5EFF4"
  data: list[float]
