from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple
import numpy as np


router = APIRouter()

class PathRequest(BaseModel):
    path: List[Tuple[float, float]]
    bottomY: int  # Bottommost y-coordinate of the canvas

@router.post("/process-path")
def process_path(request: PathRequest):
  path = request.path
  bottom_y = request.bottomY
  green_area = compute_green_area(path, bottom_y)
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

  first_point = path[0]
  last_point = path[-1]

  path = path[::10]
  path.insert(0, first_point)
  path.append(last_point)

  green_coordinates = []
  for i in range(len(path) - 1):
    start = path[i]
    end = path[i + 1]
    interpolated_points = interpolate_points(start, end)
    print(f"Interpolated points between {start} and {end}: {interpolated_points}")  # Debug print
    for x, y in interpolated_points:
      for j in range(int(y), bottom_y):
        green_coordinates.append((x, j))
        print(f"Adding green coordinate: ({x}, {j})")  # Debug print

  print(f"Final green coordinates: {green_coordinates}")  # Debug print
  return green_coordinates

