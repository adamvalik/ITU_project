from pydantic import BaseModel

class PracticeTarget(BaseModel):
    name: str
    xCord: int
    yCord: int
    health: int
    color: str