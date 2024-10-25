from fastapi import APIRouter
from model.game import game

router = APIRouter()

@router.post("/game/mode")
async def set_game_mode(mode: str, timer: bool = False, wins: int = 0):
  game.mode = mode
  # when the game mode is set to "classic", the timer and wins are not used
  game.timer = timer
  game.wins = wins

