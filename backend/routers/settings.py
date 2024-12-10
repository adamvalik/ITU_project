from fastapi import APIRouter
from models.settings import settings, UpdateVolume

router = APIRouter()

@router.get("/settings/musicVolume")
async def get_music_volume():
  return settings.musicVolume

@router.post("/settings/musicVolume")
async def set_music_volume(volume: UpdateVolume):
  settings.musicVolume = volume.volume
