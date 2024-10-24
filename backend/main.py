from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.player import Player

from routers import chooseTanks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],
)

app.include_router(chooseTanks.router)

# muzes nastavit spolecny prerix pro vsechny routy v routeru
#app.include_router(user_router, prefix="/api/v1")

players = [
  Player(name="Alice", tankType=0, color="#FF0000", armour=1, power=3, speed=1, money=100, fuel=100, health=100, skillPoints=3, weapon1=0, weapon2=0, weapon3=0),
  Player(name="Bob", tankType=1, color="#00FF00", armour=0, power=3, speed=0, money=100, fuel=100, health=100, skillPoints=3, weapon1=0, weapon2=0, weapon3=0),
]