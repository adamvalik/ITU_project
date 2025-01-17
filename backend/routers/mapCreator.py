# File: mapCreator.py
# Description: This file contains the API endpoints for the map creator module.
# Author: Marek Effenberger (xeffen00)

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Tuple
from managers.mapCreatorManager import MapCreatorManager
from redisClient import get_redis_client
import numpy as np

router = APIRouter()

# Classes for the request body of the API endpoints

class PathRequest(BaseModel):
    map_name: str
    path: List[Tuple[float, float]]
    bottomY: int

class EraserRequest(BaseModel):
    map_name: str
    path: List[Tuple[float, float]]

class ImageRequest(BaseModel):
    map_name: str
    image: Tuple[float, float]

class TypeRequest(BaseModel):
    map_name: str
    type: str

class CreateMapRequest(BaseModel):
    map_name: str

class PlayerPositionRequest(BaseModel):
    map_name: str
    player: int
    position: Tuple[float, float]

class DeleteMapRequest(BaseModel):
    map_name: str

class PlayerPositionRetrieveRequest(BaseModel):
    map_name: str
    player: int

class CopyMapRequest(BaseModel):
    map_name: str
    map1: str

@router.post("/process-path")
def process_path(request: PathRequest, redis_client = Depends(get_redis_client)):
    # Function which processes the path and adds the green area to the map
  path = request.path
  bottom_y = request.bottomY

  green_area = compute_green_area(path, bottom_y)

  mapManager = MapCreatorManager(redis_client)
  map_name = request.map_name

  mapManager.add_new_data(map_name, "greenCoordinates", {"data": green_area})

  return {"greenCoordinates": green_area}

def interpolate_points(start, end):
    # Function which interpolates the points between the start and end point
    # to create a smooth line, using numpy as it is much faster
  start = np.array(start)
  end = np.array(end)
  distance = np.linalg.norm(end - start)
  steps = int(distance)

  if steps == 0:
    return [tuple(start)]

  t_values = np.linspace(0, 1, steps + 1)
  points = start + t_values[:, None] * (end - start)
  return [tuple(point) for point in points]

def compute_green_area(path, bottom_y):
    # Helping function calling interpolation on the path as the amount of data points is too low
    # and the green area would be too small (would create a sort of zebra pattern)
  green_coordinates = []
  for i in range(len(path) - 1):
    start = path[i]
    end = path[i + 1]
    interpolated_points = interpolate_points(start, end)
    for x, y in interpolated_points:
      for j in range(int(y), bottom_y):
        green_coordinates.append((x, j))
  return green_coordinates

@router.post("/erase-path")
def erase_path(request: EraserRequest, redis_client = Depends(get_redis_client)):
    # Function which adds the eraser path to the map
  path = request.path
  map_name = request.map_name
  mapManager = MapCreatorManager(redis_client)
  mapManager.add_new_data(map_name, "eraserArray", {"data": path})

  return {"message": "Eraser path added to the map"}

@router.post("/add_new_image")
def add_new_image(request: ImageRequest, redis_client = Depends(get_redis_client)):
    # Function which adds the image to the map
  map_name = request.map_name
  image = request.image
  mapManager = MapCreatorManager(redis_client)
  mapManager.add_new_data(map_name, "imageArray", {"data": image})

  return {"message": "Image added to the map"}

@router.post("/retrieve_map")
def retrieve_map(request: CreateMapRequest, redis_client = Depends(get_redis_client)):
    # Function which retrieves the map from the redis database
    mapManager = MapCreatorManager(redis_client)
    map_data = mapManager.get_map(request.map_name)
    if map_data:
        return map_data
    else:
        raise HTTPException(status_code=404, detail="Map not found")

@router.post("/set_type")
def set_map_type(request: TypeRequest, redis_client = Depends(get_redis_client)):
    # Function which sets the type of the map
    mapManager = MapCreatorManager(redis_client)
    try:
        mapManager.set_type(request.map_name, request.type)
        return {"message": "Map type updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create_map")
def create_map(request: CreateMapRequest, redis_client = Depends(get_redis_client)):
    # Function which creates the map in the redis database
    mapManager = MapCreatorManager(redis_client)
    mapManager.create_map(request.map_name)
    return {"message": "Map created"}

@router.post("/delete_map")
def delete_map(request: DeleteMapRequest, redis_client = Depends(get_redis_client)):
    # Function which deletes the map from the redis database
    mapManager = MapCreatorManager(redis_client)
    try:
        mapManager.delete_map(request.map_name)
        return {"message": "Map deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add_player_position")
def add_player_position(request: PlayerPositionRequest, redis_client = Depends(get_redis_client)):
    # Function which adds the position of the player on the map
    mapManager = MapCreatorManager(redis_client)
    print(request.player)
    try:
        mapManager.add_player_position(request.map_name, request.player, request.position)
        return {"message": "Player position added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrieve_player_position")
def retrieve_player_position(request: PlayerPositionRetrieveRequest, redis_client = Depends(get_redis_client)):
    # Function which retrieves the position of the player on the map
    mapManager = MapCreatorManager(redis_client)
    try:
        position = mapManager.get_map_attribute(request.map_name, f"tank{request.player}pos")
        return {"position": position}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/copy_map")
def copy_map(request: CopyMapRequest, redis_client = Depends(get_redis_client)):
    # Function which copies the dummy map to some new one, saved in DB
    mapManager = MapCreatorManager(redis_client)
    try:
        mapManager.copy_map(request.map_name, request.map1)
        return {"message": "Map copied successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# function which returns the number of maps in the redis database
@router.get("/retrieve_num_of_maps")
def retrieve_num_of_maps(redis_client = Depends(get_redis_client)):
    mapManager = MapCreatorManager(redis_client)
    return {"numOfMaps": mapManager.retrieve_num_of_maps()}
