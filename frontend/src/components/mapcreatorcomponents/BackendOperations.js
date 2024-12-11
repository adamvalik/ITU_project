import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const processPath = async (mapName, path, bottomY) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/process-path`, {
      map_name: mapName,
      path,
      bottomY,
    });
    return response.data;
  } catch (error) {
    console.error('Error in processPath:', error);
  }
};

export const erasePath = async (mapName, path) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/erase-path`, { map_name: mapName, path });
    return response.data;
  } catch (error) {
    console.error('Error in erasePath:', error);
  }
};

export const addNewImage = async (mapName, startX, y) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/add_new_image`, { map_name: mapName, image: [startX, y] });
    return response.data;
  } catch (error) {
    console.error('Error in addNewImage:', error);
  }
};

export const retrieveMap = async (mapName) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/retrieve_map`, { map_name: mapName });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error in retrieveMap:', error);
  }
};

export const setMapType = async (mapName, type) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/set_type`, { map_name: mapName, type });
    return response.data;
  } catch (error) {
    console.error('Error in setMapType:', error);
  }
};

export const createMap = async (mapName) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/create_map`, { map_name: mapName});
    return response.data;
  } catch (error) {
    console.error('Error in createMap:', error);
  }
}

export const deleteMap = async (mapName) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/delete_map`, { map_name: mapName});
    return response.data;
  } catch (error) {
    console.error('Error in deleteMap:', error);
  }
}

export const addPlayerPosition = async (mapName, player, position) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/add_player_position`, { map_name: mapName, player, position });
    return response.data;
  } catch (error) {
    console.error('Error in addPlayerPosition:', error);
  }
}

export const retrievePlayerPosition = async (mapName, player) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/retrieve_player_position`, { map_name: mapName, player });
    return response.data;
  } catch (error) {
    console.error('Error in retrievePlayerPosition:', error);
  }
}

//# function which copies the contents of map1 to map with given name
// class CopyMapRequest(BaseModel):
//     map_name: str
//     map1: str
//
// @router.post("/copy_map")
// def copy_map(request: CopyMapRequest, redis_client = Depends(get_redis_client)):
//     mapManager = MapCreatorManager(redis_client)
//     try:
//         mapManager.copy_map(request.map_name, request.map1)
//         return {"message": "Map copied successfully"}
//     except Exception as e:
//         raise HTTPException(status_code=500, detail=str(e))
//
// # function which returns the number of maps in the redis database
// @router.get("/retrieve_num_of_maps")
// def retrieve_num_of_maps(redis_client = Depends(get_redis_client)):
//     mapManager = MapCreatorManager(redis_client)
//     return {"numOfMaps": mapManager.retrieve_num_of_maps()}

export const copyMap = async (mapName, map1) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/copy_map`, { map_name: mapName, map1 });
    return response.data;
  } catch (error) {
    console.error('Error in copyMap:', error);
  }
}

export const retrieveNumOfMaps = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/retrieve_num_of_maps`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error in retrieveNumOfMaps:', error);
  }
}
