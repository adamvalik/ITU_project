from pydantic import BaseModel

class Map(BaseModel):
  name: str
  type: str = "forrest" # , "snow", "desert"
  # ...
