from fastapi import APIRouter
from main import players

router = APIRouter()

@router.post("/createplayer/player")
async def create():
  players.append("player")
    

@router.get("/users/{user_id}")
async def read_user(user_id: int):
  return players[0].name
