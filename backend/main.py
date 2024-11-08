from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redisClient import get_redis_client

from routers import mapCreator, players, tanks, settings, game, gameScreen, debug
from managers import playerManager, gameManager

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
app.include_router(gameScreen.router)
app.include_router(debug.router)

redis_client = get_redis_client()

playerManager = playerManager.PlayerManager(redis_client)
playerManager.initialize_players()

gameManager = gameManager.GameManager(redis_client)
gameManager.initialize_game()



