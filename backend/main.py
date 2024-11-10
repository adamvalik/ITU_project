from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redisClient import get_redis_client

from routers import mapCreator, players, tanks, settings, game, gameScreen, debug
from managers import playerManager, gameManager

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:8080",  # Your frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow requests from this list of origins
    allow_credentials=True,            # Allow cookies to be included in requests
    allow_methods=["*"],               # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],               # Allow all headers
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



