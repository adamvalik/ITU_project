from fastapi import APIRouter
from fastapi.responses import Response
from model.svgTemplates import SVG_TEMPLATES
<<<<<<< HEAD
from main import players
=======
from model.player import Player
>>>>>>> 8088d38167ddfa00e737cc24a19e5ef2a6223aeb

router = APIRouter()

players = [None] * 2

@router.post("/players/{player_id}")
async def set_player(player_id: int, player: Player):
    # Ensure the list is large enough to accommodate the player_id
    if player_id >= len(players):
        players.extend([None] * (player_id + 1 - len(players)))

    # Set the player at the specified index
    players[player_id] = player

    print(f"Player {player_id} set. Current players: {players}")

    return {"message": f"Player {player_id} set successfully", "player": player}

# get player's data
@router.get("/players")
async def get_players():
  print(players)
  return players

@router.delete("/players")
async def delete_players():
  players.clear()
  return {"message": "All players deleted"}



# get svg of player's tank
@router.get("/players/{player_id}/tank")
async def get_tank(player_id: int):
  svg_template = SVG_TEMPLATES[players[player_id].tankType]
  modified_svg = svg_template.replace("#123456", players[player_id].color)
  return Response(content=modified_svg, media_type="image/svg+xml")

if __name__ == "__main__":
  print(players)

@router.get("/player/{player_id}")
async def get_player(player_id: int):
  player = players[player_id]
  return player