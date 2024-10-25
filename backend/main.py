from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import players
from routers import tanks
from routers import mapCreator
from routers import settings
from routers import game

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mapCreator.router)
app.include_router(players.router)
app.include_router(tanks.router)
app.include_router(settings.router)
app.include_router(game.router)

# muzes nastavit spolecny prerix pro vsechny routy v routeru
#app.include_router(user_router, prefix="/api/v1")
