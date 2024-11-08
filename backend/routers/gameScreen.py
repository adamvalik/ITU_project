from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# class Ammunition(BaseModel):
#     name: str
#     damage: int
#     radius: int
#     cost : int

# class Player(BaseModel):
#     id: int
#     name: str
#     xCord: int
#     yCord: int
#     size: int
#     shellAngle: int
#     shellPower: int
#     tankColor: str
#     health: int
#     wins: int
#     money: int
#     fuel: int
#     fuelMax: int
#     ammunitionCount: list[int] # 0 for no shells, -1 for shell that user does not have 

# class Map(BaseModel):
#     wind: int
#     canvasWidth: int
#     canvasHeight: int
#     time: int