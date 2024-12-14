from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redisClient import get_redis_client

from routers import mapCreator, players, tanks, settings, game, gameScreen, debug, mapSelector
from managers import playerManager, gameManager, missileManager
from managers.mapCreatorManager import MapCreatorManager
from managers.mapManager import MapManager

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(mapCreator.router)
app.include_router(players.router)
app.include_router(tanks.router)
app.include_router(settings.router)
app.include_router(game.router)
app.include_router(gameScreen.router)
app.include_router(debug.router)
app.include_router(mapSelector.router)

redis_client = get_redis_client()

playerManager = playerManager.PlayerManager(redis_client)
playerManager.initialize_players()

gameManager = gameManager.GameManager(redis_client)
gameManager.initialize_game()

missileManager = missileManager.MissileManager(redis_client)
missileManager.initialize_missile()

mapCreatorManager = MapCreatorManager(redis_client)

MapManager = MapManager(redis_client)
MapManager.initialize_map()


