from pydantic import BaseModel

class Settings(BaseModel):
  musicVolume: int = 50

settings = Settings()