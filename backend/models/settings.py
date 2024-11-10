from pydantic import BaseModel

class Settings(BaseModel):
  musicVolume: int = 0

settings = Settings()
