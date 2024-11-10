<template>
  <div
    class="flex flex-col items-center bg-white"
    :style="{ width: `${gameWidth}px`, height: `${gameHeight}px` }"
  >
    <div class="flex justify-around items-center mb-6 h-1/3 w-5/6">
      <div
        v-for="(map, index) in maps"
        :key="index"
        :class="['w-72 border-4 border-gray-300 rounded-lg', { 'border-green-500': selectedMap === map }]"
        @click="selectMap(map)"
      >
        <img :src="map.image" alt="Map preview" />
      </div>
    </div>

    <hr class="w-full border-gray-500" />

    <div class="flex items-center justify-center space-x-8 mb-4">
      <!-- Create Map Button -->
      <button @click="createMap" class="px-4 py-2 bg-gray-200 rounded-lg shadow-md hover:bg-gray-300">
        CREATE YOUR MAP
      </button>

      <!-- Large Map Preview -->
      <div class="border-4 border-green-500 w-80 h-48 flex items-center justify-center">
        <img :src="selectedMap.image" alt="Selected map" class="w-full h-full rounded-lg" />
      </div>

      <!-- Your Maps List -->
      <div class="text-left">
        <h3 class="font-semibold text-gray-700 mb-2">YOUR MAPS:</h3>
        <ul>
          <li
            v-for="(map, index) in customMaps"
            :key="index"
            :class="['cursor-pointer', { 'font-bold text-green-600': selectedMap === map }]"
            @click="selectMap(map)"
          >
            {{ map.name }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Weather Selection Section -->
    <div class="flex items-center space-x-4 mb-8">
      <span class="font-bold text-lg">WEATHER:</span>
      <span class="font-bold">{{ selectedWeather }}</span>
      <div class="flex space-x-2">
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
          <img :src="weather.icon" :alt="weather.label" class="w-6 h-6" />
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
export default {
  props: {
    gameWidth: Number,
    gameHeight: Number,
  },
  mounted() {
    this.selectedMap = this.maps[0];
  },
  data() {
    return {
      maps: [
        { name: 'default', image: '/assets/map1.png' },
        { name: 'desert', image: '/assets/map2.png' },
        { name: 'arctic', image: '/assets/map3.png' },
      ],
      customMaps: [
        { name: 'desert_madness', image: '/assets/map1.png' },
        { name: 'my_map', image: '/assets/map2.png' },
        { name: 'mountainss', image: '/assets/map3.png' },
      ],
      selectedMap: { name: 'default', image: '/assets/map1.png' },
      weathers: [
        { label: 'Sunny', icon: '/assets/sunny-icon.png' },
        { label: 'Cloudy', icon: '/assets/cloudy-icon.png' },
        { label: 'Extreme', icon: '/assets/extreme-icon.png' },
      ],
      selectedWeather: 'Extreme',
    };
  },
  methods: {
    selectMap(map) {
      this.selectedMap = map;
    },
    createMap() {
      console.log('Create your map button clicked');
    },
    selectWeather(weather) {
      this.selectedWeather = weather;
    },
    chooseTank() {
      console.log('Choose tank button clicked');
    },
    playGame() {
      console.log('Play button clicked');
    },
  },
};
</script>
