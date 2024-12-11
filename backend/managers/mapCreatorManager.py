from typing import Optional, List, Tuple, Union
from redis import Redis
from models.mapcreator import Map
import json

class MapCreatorManager:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def create_map(self, map_name: str):
        map_key = f"{map_name}"
        if not self.redis_client.exists(map_key):
            new_map = Map(name=map_name)
            self.redis_client.set(map_key, new_map.json())

    def get_map(self, map_name: str) -> Optional[Map]:
        map_key = f"{map_name}"
        map_data = self.redis_client.get(map_key)
        if map_data:
            return Map.parse_raw(map_data)
        return None

    def get_current_map(self) -> Optional[Map]:
        map_data = self.redis_client.get("arrayArray")
        if map_data:
            return Map.parse_raw(map_data)
        return None

    def add_new_data(self, map_name: str, type: str, data: dict):
        mapa = self.get_map(map_name)
        if mapa:
            mapa.arrayArray.append({"type": type, "data": data})
            self.redis_client.set(map_name, mapa.json())
        else:
            raise ValueError(f"Map '{map_name}' not found")

    # New Methods

    def get_map_attribute(self, map_name: str, attribute: str) -> Optional[Union[List, str]]:
        """Retrieve a specific attribute (e.g., imageArray) from a map."""
        mapa = self.get_map(map_name)
        if mapa:
            return getattr(mapa, attribute, None)
        return None

    def update_map_attribute(self, map_name: str, attribute: str, data: Union[List, Tuple]):
        """Update a specific array attribute in the map."""
        mapa = self.get_map(map_name)
        if mapa:
            setattr(mapa, attribute, data)
            self.redis_client.set(map_name, mapa.json())
        else:
            return None

    def save_array_data(self, map_name: str, array_type: str, new_data: List[Tuple[int, int]]):
        """Append data to a specified array type (e.g., `imageArray`, `eraserArray`)."""
        mapa = self.get_map(map_name)
        if mapa:
            array = getattr(mapa, array_type, None)
            if array is not None:
                array.append(new_data)
                self.redis_client.set(map_name, mapa.json())
            else:
                return None
        else:
            return None

    def delete_map(self, map_name: str):
        """Delete a map from Redis."""
        self.redis_client.delete(map_name)

    def clear_map(self, map_name: str):
        """Clear the map's array attributes."""
        mapa = self.get_map(map_name)
        if mapa:
            mapa.imageArray = []
            mapa.eraserArray = []
            mapa.groundArray = []
            mapa.tank1pos = (0, 0)
            mapa.tank2pos = (0, 0)
            mapa.saved = False
            self.redis_client.set(map_name, mapa.json())
        else:
            return None

    def set_type(self, map_name: str, type: str):
        mapa = self.get_map(map_name)
        if mapa:
            mapa.type = type
            self.redis_client.set(map_name, mapa.json())
        else:
            return None

    def add_player_position(self, map_name: str, player: int, position: Tuple[float, float]):
        """Add a player's position to the map."""
        mapa = self.get_map(map_name)
        position = (int(position[0]), int(position[1]))
        if mapa:
            if player == 1:
                mapa.tank1pos = position
            elif player == 2:
                mapa.tank2pos = position
            self.redis_client.set(map_name, mapa.json())
        else:
            return None


# # function which copies the contents of map1 to map with given name
# class CopyMapRequest(BaseModel):
#     map_name: str
#     map1: str
#
# @router.post("/copy_map")
# def copy_map(request: CopyMapRequest, redis_client = Depends(get_redis_client)):
#     mapManager = MapCreatorManager(redis_client)
#     try:
#         mapManager.copy_map(request.map_name, request.map1)
#         return {"message": "Map copied successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

    def copy_map(self, map_name: str, map1: str):
        """Create new map with the same data as an existing map."""
        mapa = self.get_map(map1)
        if mapa:
            mapa.name = map_name
            self.redis_client.set(map_name, mapa.json())
        else:
            return None

    def retrieve_num_of_maps(self):
        """Retrieve the number of maps stored in Redis."""
        return len(self.redis_client.keys())
