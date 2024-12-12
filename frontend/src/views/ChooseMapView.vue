<!-- File: ChooseMapView.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <div
    class="flex flex-col items-center bg-cover bg-center"
    :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`, backgroundImage: `url(${backgroundImageUrl})`}"
  >

    <!-- default maps -->
    <div class="flex justify-around items-center h-1/3 w-5/6">
      <div
        v-for="(map, index) in defaultMaps"
        :key="index"
        :class="['w-72 border-4 border-gray-300 rounded-xl', { 'border-green-500': selectedMap === map.name }]"
        @click="selectMap(map)"
      >
        <img :src="map.image" alt="Map preview" class="rounded-lg" />
      </div>
    </div>

    <!-- divider -->
    <hr class="w-full border-gray-500" />

    <!-- lower part of the screen -->
    <div class="flex items-center justify-around w-full h-3/5">

      <!-- button to map creator -->
      <div class="w-1/3 flex items-center justify-end pr-10">
        <button @click="createMap" class="px-4 py-4 w-32 h-32 bg-gray-200 font-bold rounded-lg shadow-md hover:bg-gray-300">
          CREATE YOUR MAP
        </button>
      </div>

      <!-- custom maps preview -->
      <div
        :class="['w-1/3 border-4 border-gray-300 rounded-xl', { 'border-green-500': customMapSelected }]"
      >
        <img
          :src="selectedCustomMapImage"
          alt="Custom map"
          id="customMap"
          class="w-full h-full rounded-lg"
          :class="[{'opacity-50' : !anyCustomMap || selectedCustomMap == null}]"/>
      </div>

      <!-- custom map names -->
      <div class="text-left w-1/3 pl-10">
        <h3 class="font-semibold text-gray-900 mb-1">YOUR MAPS:</h3>
        <ul
          v-if="customMapNames.length > 0"
          class="max-h-72 overflow-y-auto"
          >
          <li
            v-for="(mapName, index) in customMapNames"
            :key="index"
            :class="['cursor-pointer', { 'font-bold text-green-600': selectedCustomMap === mapName }]"
            @click="selectCustomMap(mapName)"
          >
            {{ mapName }}
          </li>
        </ul>
        <p v-else>No custom maps created</p>
      </div>
    </div>

    <!-- weather selection -->
    <div class="flex flex-col items-center justify-normal mb-8 z-10 relative">
      <div class="flex items-center space-x-2">
        <span class="font-bold text-lg">WEATHER:</span>
        <!-- tooltip trigger -->
        <div
          class="relative flex items-center justify-center w-6 h-6 bg-gray-700 rounded-full cursor-pointer"
          @mouseover="showTooltip = true"
          @mouseleave="showTooltip = false"
        >
          <span class="font-bold text-sm text-white">?</span>
          <!-- tooltip -->
          <div
            v-show="showTooltip"
            class="absolute mt-2 transform translate-x-2/3 bg-gray-700 text-white text-sm rounded p-2 shadow-lg w-48 transition-opacity duration-300 opacity-0"
            :class="{ 'opacity-100': showTooltip, 'opacity-0': !showTooltip }"
          >
            <p>Changing the weather affects the wind probability in the game!</p>
          </div>
        </div>
      </div>
      <!-- weather  -->
      <span class="font-bold mb-4">{{ selectedWeather }}</span>
      <!-- radio buttons -->
      <div class="flex space-x-2 relative">
        <button
          v-for="(weather, index) in weathers"
          :key="index"
          :class="[
            'w-12 h-12 flex items-center justify-center rounded-lg',
            { 'bg-yellow-400': selectedWeather === weather.label },
            'border-2 border-gray-300',
          ]"
          @click="selectWeather(weather.label)"
        >
          <img :src="weather.icon" :alt="weather.label" class="w-6" />
        </button>
      </div>
    </div>

    <!-- footer buttons -->
    <div class="absolute bottom-4 left-0 right-0 flex justify-between px-8">
      <router-link to="/chooseTanks" class="px-6 py-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
        Back to Tank Selection
      </router-link>

      <router-link to="/game" class="px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-200">
        Start Game
      </router-link>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  props: {
    gameWidth: Number,
    gameHeight: Number,
  },
  data() {
    return {
      defaultMaps: [
        { name: '__forest', image: '/assets/forest.png' },
        { name: '__beach', image: '/assets/beach.png' },
        { name: '__winter', image: '/assets/winter.png' },
      ],
      selectedMap: '__forest',
      selectedCustomMap: null,
      customMapNames: [],
      customMapSelected: false,
      selectedCustomMapImage: '/assets/placeholder.png',

      weathers: [
        { label: 'Sunny', icon: '/assets/sunny-icon.png' },
        { label: 'Cloudy', icon: '/assets/cloudy-icon.png' },
        { label: 'Extreme', icon: '/assets/extreme-icon.png' },
      ],
      selectedWeather: '',
      showTooltip: false,
    };
  },
  computed: {
    backgroundImageUrl() {
      switch (this.selectedWeather) {
        case 'Extreme':
          return '/assets/bg3-extreme.png';
        case 'Sunny':
          return '/assets/bg3-sunny.png';
        default:
          return '/assets/bg3-cloudy.png';
      }
    },
    anyCustomMap() {
      return this.customMapNames.length > 0;
    }
  },
  async mounted() {
    await this.fetchCustomMapNames();
    await this.fetchWeather();
    await this.fetchMap();
  },
  methods: {
    // get & post weather
    async fetchWeather() {
      try {
        const response = await apiClient.get('/weather');
        this.selectedWeather = response.data;
      } catch (error) {
        console.error('Failed to fetch weather:', error);
      }
    },
    async selectWeather(weather) {
      this.selectedWeather = weather;
      try {
        await apiClient.post('/weather', { weather: weather });
      } catch (error) {
        console.error('Failed to set weather:', error);
      }
    },

    // get & post mapName
    async fetchMap() {
      try {
        const response = await apiClient.get('/map/mapName');
        if (response.data === '') {
          return;
        }
        if (response.data !== '__forest' && response.data !== '__beach' && response.data !== '__winter') {
          this.selectCustomMap(response.data);
        } else {
          this.selectMap(this.defaultMaps.find((map) => map.name === response.data));
        }
      } catch (error) {
        console.error('Failed to fetch map:', error);
      }
    },
    async selectMap(map) {
      this.selectedMap = map.name;
      this.customMapSelected = false;
      try {
        await apiClient.post('/map/mapName', { mapName: map.name });
      } catch (error) {
        console.error('Failed to set map:', error);
      }
    },
    async selectCustomMap(map) {
      this.selectedMap = map;
      this.selectedCustomMap = map;
      this.customMapSelected = true;
      try {
        await apiClient.post('/map/mapName', { mapName: map });
        // get the type of the terrain and set the image accordingly
        // (this was intended to be used for the map preview, but it was too complicated to implement)
        const response = await apiClient.get(`/map/type/${map}`);
        if (response.data == 'forest') {
          this.selectedCustomMapImage = '/assets/forest.png';
        } else if (response.data == 'beach') {
          this.selectedCustomMapImage = '/assets/beach.png';
        } else if (response.data == 'winter') {
          this.selectedCustomMapImage = '/assets/winter.png';
        }
      } catch (error) {
        console.error('Failed to fetch custom map:', error);
      }
    },

    // get custom map names
    async fetchCustomMapNames() {
      try {
        const response = await apiClient.get('/map/names');
        this.customMapNames = response.data;
      } catch (error) {
        console.error('Failed to fetch custom map names:', error);
      }
    },

    // into the map creator
    createMap() {
      this.$router.push({ path: '/mapCreator', query: { fromMapSelector: true } });
    },
  },
};
</script>
