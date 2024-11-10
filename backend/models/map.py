from pydantic import BaseModel

class Map(BaseModel):
  name: str
  type: str = "forest" # , "snow", "desert"
  # ...
