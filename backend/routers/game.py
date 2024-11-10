from fastapi import APIRouter, HTTPException, Depends

from models.game import Game, CustomMode
from managers.gameManager import GameManager
from redisClient import get_redis_client

router = APIRouter()

@router.post("/game/custom_mode")
async def set_game_mode(custom_mode: CustomMode, redis_client = Depends(get_redis_client)):
    game_manager = GameManager(redis_client)
    game_data = {
        "isTimer": custom_mode.isTimer,
        "timePerTurn": custom_mode.timePerTurn,
        "toWins": custom_mode.toWins,
    }
    updated_game = game_manager.update_game(game_data)
    if updated_game is None:
        raise HTTPException(status_code=404, detail="Game not found or invalid data")
    return {"message": "Game mode updated"}

@router.delete("/game/reset")
async def reset_game(redis_client = Depends(get_redis_client)):
    game_manager = GameManager(redis_client)
    game_manager.reset_game()
    return {"message": "Game reset"}

@router.get("/game", response_model=Game)
async def get_game(redis_client = Depends(get_redis_client)):
    game_manager = GameManager(redis_client)
    game = game_manager.get_game()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.put("/game/map_name")
async def set_map_name(map_name: str, redis_client = Depends(get_redis_client)):
    game_manager = GameManager(redis_client)
    game_data = {"mapName": map_name}
    updated_game = game_manager.update_game(game_data)
    if updated_game is None:
        raise HTTPException(status_code=404, detail="Game not found or invalid data")
    return {"message": "Map name updated"}
