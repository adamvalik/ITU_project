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
        "timePerRound": custom_mode.timePerRound,
        "toWins": custom_mode.toWins,
    }
    updated_game = game_manager.update_game(game_data)
    if updated_game is None:
        raise HTTPException(status_code=404, detail="Game not found or invalid data")
    return {"message": "Game mode updated"}
