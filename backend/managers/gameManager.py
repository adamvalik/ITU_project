from typing import Optional
from redis import Redis
from models.game import Game
from pydantic import ValidationError

class GameManager:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.key = "game"  # Single key for storing game data

    def create_game(self, game: Game):
        self.redis_client.set(self.key, game.json())

    def initialize_game(self):
        default_game = Game()
        self.create_game(default_game)

    def get_game(self) -> Optional[Game]:
        game_data = self.redis_client.get(self.key)
        if game_data:
            return Game.parse_raw(game_data)
        return None

    def update_game(self, game_data: dict) -> Optional[Game]:
        """Update specific attributes of the game instance."""
        game = self.get_game()
        if game:
            try:
                updated_game = game.copy(update=game_data)
                self.create_game(updated_game)  # overwrite with new data
                return updated_game
            except ValidationError as e:
                print(f"Validation error updating game: {e}")
                return None
        return None

    def delete_game(self):
        self.redis_client.delete(self.key)

    def reset_game(self):
        """Reset the game to default values."""
        self.delete_game()
        self.initialize_game()
