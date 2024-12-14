from fastapi import APIRouter, HTTPException, Depends, Response
from models.svgTemplates import SVG_TEMPLATES

from models.player import Player, UpdateName, UpdateTankType, UpdateColor, UpdateSkill, UpdateSkillPoints, IncreaseSkillPoints, BuyAmmo
from managers.playerManager import PlayerManager
from redisClient import get_redis_client

router = APIRouter()

@router.post("/player/name")
async def update_player_name(data: UpdateName, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.update_name(data.player, data.name)

@router.post("/player/tankType")
async def update_player_tank(data: UpdateTankType, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.update_tank(data.player, data.tankType)

@router.post("/player/color")
async def update_player_color(data: UpdateColor, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.update_color(data.player, data.color)

@router.post("/player/skill")
async def update_player_skill(data: UpdateSkill, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.update_skill(data.player, data.skill, data.value)

@router.post("/player/skillPoints")
async def update_player_skill_points(data: UpdateSkillPoints, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.update_skill_points(data.player, data.skillPoints)

@router.post("/player/skillPointsInc")
async def increment_player_skill_points(data: IncreaseSkillPoints, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.increment_skill_points(data.player)

@router.post("/players/{player_id}")
async def update_player(player_id: int, player: Player, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.create_player(player)
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

@router.delete("/players/reset")
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

@router.delete("/players/reset-health")
async def reset_health(redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.reset_health()
    return {"message": "Health reset"}

@router.post("/player/buyAmmo")
async def buy_ammo(data: BuyAmmo, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.buy_ammo(data.player, data.ammo_type, data.price)

@router.post("/player/upgradeSkill")
async def upgrade_skill(data: UpdateSkill, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.upgrade_skill(data.player, data.skill)

@router.post("/player/downgradeSkill")
async def upgrade_skill(data: UpdateSkill, redis_client = Depends(get_redis_client)):
    player_manager = PlayerManager(redis_client)
    player_manager.downgrade_skill(data.player, data.skill)