from fastapi import APIRouter
from fastapi.responses import Response
from svg_templates import SVG_TEMPLATES
from main import players

router = APIRouter()

@router.get("/player/{player_id}/tank")
async def get_tank(player_id: int):
  svg_template = SVG_TEMPLATES[players[player_id].tankType]
  modified_svg = svg_template.replace("#123456", players[player_id].color)
  return Response(content=modified_svg, media_type="image/svg+xml")