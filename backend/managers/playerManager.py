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
        player1 = Player(id=1, name="Player 1", tankType=0, color='#06B559')
        player2 = Player(id=2, name="Player 2", tankType=1, color='#0D6BBD')
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

    def update_player(self, player_id: int, player_data: dict):
        player = self.get_player(player_id)
        if player:
            try:
                updated_player = player.copy(update=player_data)
                self.create_player(updated_player.id, updated_player.dict())  # overwrite with new data
                return updated_player
            except ValidationError as e:
                print(f"Validation error updating player {player_id}: {e}")
                return None
        return None

    def delete_player(self, player_id: int):
        player_key = f"{self.key_prefix}{player_id}"
        self.redis_client.delete(player_key)

    def reset_players(self):
        """Reset the two players' data in Redis."""
        self.delete_player(1)
        self.delete_player(2)
