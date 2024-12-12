# File: mapcreator.py
# Description: Base model for the map creator module.
# Author: Marek Effenberger (xeffen00)

from pydantic import BaseModel
from typing import Tuple, List

class Map(BaseModel):

    name: str
    type: str = "forest"
    saved: bool = False

    tank1pos : Tuple[int, int] = (0, 0)
    tank2pos : Tuple[int, int] = (0, 0)

    imageArray : List[Tuple[int, int]] = []
    eraserArray : List[List[Tuple[int, int]]] = [[]]
    groundArray : List[List[Tuple[int, int]]] = [[]]

    # Array of the previous three lists
    arrayArray: List[dict] = []



