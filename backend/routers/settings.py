from fastapi import APIRouter
from model.settings import settings

router = APIRouter()

@router.get("/settings/musicVolume")
async def get_music_volume():
  return settings.musicVolume

@router.post("/settings/musicVolume")
async def set_music_volume(volume: int):
  settings.musicVolume = volume