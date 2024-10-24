from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import chooseTanks
from routers import mapCreator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chooseTanks.router)
app.include_router(mapCreator.router)

# muzes nastavit spolecny prerix pro vsechny routy v routeru
#app.include_router(user_router, prefix="/api/v1")

players = [1, 1]
