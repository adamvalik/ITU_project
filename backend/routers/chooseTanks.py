from fastapi import APIRouter
import main

router = APIRouter()

@router.post("/createplayer/player")
async def create():
  main.players.append("player")
    

@router.get("/users/{user_id}")
async def read_user(user_id: int):
  return main.players[0].name
