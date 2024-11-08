from fastapi import APIRouter, HTTPException, Depends, Response
from models.svgTemplates import SVG_TEMPLATES

from models.player import Player
from managers.playerManager import PlayerManager
from redisClient import get_redis_client

router = APIRouter()

@router.post("/players/{player_id}")
async def update_player(player_id: int, player: dict, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    updated_player = player_manager.update_player(player_id, player)
    if updated_player is None:
        raise HTTPException(status_code=404, detail="Player not found or invalid data")
    return {"message": "Player updated"}

@router.get("/players", response_model=list[Player])
async def get_players(redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    players = player_manager.get_players()
    if not players or len(players) < 2:
        raise HTTPException(status_code=404, detail="Players not found")
    return players

@router.get("/players/{player_id}", response_model=Player)
async def get_player(player_id: int):
    player_manager = PlayerManager(get_redis_client())
    player = player_manager.get_player(player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.delete("/players")
async def delete_players(redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.reset_players()
    return {"message": "Players reset"}

# get svg of player's tank
@router.get("/players/{player_id}/tank")
async def get_tank(player_id: int, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player = player_manager.get_player(player_id)
    svg_template = SVG_TEMPLATES[player.tankType]
    modified_svg = svg_template.replace("#123456", player.color)
    return Response(content=modified_svg, media_type="image/svg+xml")
