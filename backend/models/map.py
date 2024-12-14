from pydantic import BaseModel
class Map(BaseModel):
  name: str
  type: str = "forest" # , "snow", "desert"
  background: str = "#D5EFF4"
  data: list[float]
  # ...
