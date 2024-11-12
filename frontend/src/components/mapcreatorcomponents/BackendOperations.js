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

export const addNewImage = async (mapName, image) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/add_new_image`, { map_name: mapName, image });
    return response.data;
  } catch (error) {
    console.error('Error in addNewImage:', error);
  }
};

export const retrieveMap = async (mapName) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/retrieve_map`, { map_name: mapName });
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
