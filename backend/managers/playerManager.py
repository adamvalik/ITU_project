from typing import Optional
from redis import Redis
from models.player import Player
from pydantic import ValidationError

class PlayerManager:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.key_prefix = "player"  # prefix for player keys

    def create_player(self, player: Player):
        player_key = f"{self.key_prefix}{player.id}"
        self.redis_client.set(player_key, player.json())

    def initialize_players(self):
        """Initialize the two players' data in Redis."""
        player1 = Player(id=1, name="", tankType=0, color='#06B559')
        player2 = Player(id=2, name="", tankType=1, color='#0D6BBD')
        self.create_player(player1)
        self.create_player(player2)

    def get_player(self, player_id: int) -> Optional[Player]:
        player_key = f"{self.key_prefix}{player_id}"
        player_data = self.redis_client.get(player_key)
        if player_data:
            return Player.parse_raw(player_data)
        return None

    def get_players(self) -> list[Player]:
        players = []
        for player_id in range(1, 3):
            player = self.get_player(player_id)
            if player:
                players.append(player)
        return players

    def update_name(self, player_id: int, name: str):
        player = self.get_player(player_id)
        if player:
            player.name = name
            self.create_player(player)
        else:
            raise ValidationError(f"Player with id {player_id} not found")

    def update_tank(self, player_id: int, tank_type: int):
        player = self.get_player(player_id)
        if player:
            player.tankType = tank_type
            self.create_player(player)
        else:
            raise ValidationError(f"Player with id {player_id} not found")

    def update_color(self, player_id: int, color: str):
        player = self.get_player(player_id)
        if player:
            player.color = color
            self.create_player(player)
        else:
            raise ValidationError(f"Player with id {player_id} not found")

    def update_skill(self, player_id: int, skill: str, value: int):
        player = self.get_player(player_id)
        if player:
            if skill == "armor":
                player.armorSkill = value
            elif skill == "power":
                player.powerSkill = value
            elif skill == "speed":
                player.speedSkill = value
            else:
                raise ValidationError(f"Invalid skill: {skill}")
            self.create_player(player)
        else:
            raise ValidationError(f"Player with id {player_id} not found")

    def update_skill_points(self, player_id: int, skill_points: int):
        player = self.get_player(player_id)
        if player:
            player.skillPoints = skill_points
            self.create_player(player)
        else:
            raise ValidationError(f"Player with id {player_id} not found")

    def increment_skill_points(self, player_id: int):
        player = self.get_player(player_id)
        if player:
            player.skillPoints += 1
            self.create_player(player)
        else:
            raise ValidationError(f"Player with id {player_id} not found")

    def delete_player(self, player_id: int):
        player_key = f"{self.key_prefix}{player_id}"
        self.redis_client.delete(player_key)

    def reset_players(self):
        """Reset the two players' data in Redis."""
        self.delete_player(1)
        self.delete_player(2)
        self.initialize_players()
