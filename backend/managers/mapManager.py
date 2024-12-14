from typing import Optional
from redis import Redis
from models.map import Map
from pydantic import ValidationError

class MapManager:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.key = "map"

    def create_map(self, map: Map):
        self.redis_client.set(self.key, map.json())
    
    def initialize_map(self):
        default_map = Map(name="default", type="forest", background="#D5EFF4", data=[])
        self.create_map(default_map)
    
    def get_map(self) -> Optional[Map]:
        map_data = self.redis_client.get(self.key)
        if map_data:
            return Map.parse_raw(map_data)
        return None
    
    def delete_map(self):
        self.redis_client.delete(self.key)