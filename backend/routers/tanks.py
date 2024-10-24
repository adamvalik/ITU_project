from fastapi import APIRouter, Response
from model.svgTemplates import SVG_SELECTOR

router = APIRouter()

@router.get("/selector/{tank_type}")
async def get_selector_tank(tank_type: int):
  svg = SVG_SELECTOR[tank_type]
  return Response(content=svg, media_type="image/svg+xml")