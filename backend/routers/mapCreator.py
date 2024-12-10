from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Tuple
from managers.mapCreatorManager import MapCreatorManager
from redisClient import get_redis_client
import numpy as np

router = APIRouter()

class PathRequest(BaseModel):
    map_name: str
    path: List[Tuple[float, float]]
    bottomY: int  # Bottommost y-coordinate of the canvas

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

@router.post("/process-path")
def process_path(request: PathRequest, redis_client = Depends(get_redis_client)):

  path = request.path
  bottom_y = request.bottomY

  green_area = compute_green_area(path, bottom_y)

  mapManager = MapCreatorManager(redis_client)
  map_name = request.map_name

  mapManager.add_new_data(map_name, "greenCoordinates", {"data": green_area})

  return {"greenCoordinates": green_area}

def interpolate_points(start, end):
  start = np.array(start)
  end = np.array(end)
  distance = np.linalg.norm(end - start)
  steps = int(distance)  # Number of steps based on distance

  if steps == 0:
    return [tuple(start)]

  t_values = np.linspace(0, 1, steps + 1)
  points = start + t_values[:, None] * (end - start)
  return [tuple(point) for point in points]

def compute_green_area(path, bottom_y):
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
  path = request.path
  map_name = request.map_name
  mapManager = MapCreatorManager(redis_client)
  mapManager.add_new_data(map_name, "eraserArray", {"data": path})

  return {"message": "Eraser path added to the map"}

@router.post("/add_new_image")
def add_new_image(request: ImageRequest, redis_client = Depends(get_redis_client)):
  map_name = request.map_name
  image = request.image
  mapManager = MapCreatorManager(redis_client)
  mapManager.add_new_data(map_name, "imageArray", {"data": image})

  return {"message": "Image added to the map"}

@router.post("/retrieve_map")
def retrieve_map(request: CreateMapRequest, redis_client = Depends(get_redis_client)):
    mapManager = MapCreatorManager(redis_client)
    map_data = mapManager.get_map(request.map_name)
    if map_data:
        return map_data
    else:
        raise HTTPException(status_code=404, detail="Map not found")

@router.post("/set_type")
def set_map_type(request: TypeRequest, redis_client = Depends(get_redis_client)):
    mapManager = MapCreatorManager(redis_client)
    try:
        mapManager.set_type(request.map_name, request.type)
        return {"message": "Map type updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create_map")
def create_map(request: CreateMapRequest, redis_client = Depends(get_redis_client)):
    mapManager = MapCreatorManager(redis_client)
    mapManager.create_map(request.map_name)
    return {"message": "Map created"}

class DeleteMapRequest(BaseModel):
    map_name: str

@router.post("/delete_map")
def delete_map(request: DeleteMapRequest, redis_client = Depends(get_redis_client)):
    mapManager = MapCreatorManager(redis_client)
    try:
        mapManager.delete_map(request.map_name)
        return {"message": "Map deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
