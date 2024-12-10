from pydantic import BaseModel

class UpdateVolume(BaseModel):
    volume: int

class Settings(BaseModel):
    musicVolume: int = 0

settings = Settings()
