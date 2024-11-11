<template>
  <div
    class="flex flex-col items-center bg-white"
    :style="{ width: `${gameWidth}px`, height: `${gameHeight}px` }"
  >
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

    <hr class="w-full border-gray-500" />

    <div class="flex items-center justify-around w-full h-3/5">
      <div class="w-1/3 flex items-center justify-end pr-10">
        <button @click="createMap" class="px-4 py-4 w-32 h-32 bg-gray-200 font-bold rounded-lg shadow-md hover:bg-gray-300">
          CREATE YOUR MAP
        </button>
      </div>

      <div
        :class="['w-1/3 border-4 border-gray-300 rounded-xl', { 'border-green-500': customMapSelected }]"
        @click="selectCustomMap"
      >
        <img src="/assets/bg.png" alt="Custom map" class="w-full h-full rounded-lg" />
      </div>

      <div class="text-left w-1/3 pl-10">
        <h3 class="font-semibold text-gray-700 mb-1">YOUR MAPS:</h3>
        <ul>
          <li
            v-for="(mapName, index) in customMapNames"
            :key="index"
            :class="['cursor-pointer', { 'font-bold text-green-600': selectedMap === mapName }]"
            @click="selectCustomMap(mapName)"
          >
            {{ mapName }}
          </li>
        </ul>
      </div>
    </div>

    <!-- weather selection -->
    <div class="flex flex-col items-center justify-normal mb-8">
      <div class="flex gap-8">
        <span class="font-bold text-lg">WEATHER:</span>
        <span class="font-bold">{{ selectedWeather }}</span>
      </div>
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
  data() {
    return {
      defaultMaps: [
        { name: '__forest', image: '/assets/bg.png' },
        { name: '__desert', image: '/assets/bg.png' },
        { name: '__mountains', image: '/assets/bg.png' },
      ],
      selectedMap: '__forest',
      customMapNames: ['map1', 'map2', 'map3', 'map4'],
      customMapSelected: false,

      weathers: [
        { label: 'Sunny', icon: '/assets/sunny-icon.png' },
        { label: 'Cloudy', icon: '/assets/cloudy-icon.png' },
        { label: 'Extreme', icon: '/assets/extreme-icon.png' },
      ],
      selectedWeather: 'Extreme',
    };
  },
  methods: {
    selectWeather(weather) {
      this.selectedWeather = weather;
    },
    selectMap(map) {
      this.selectedMap = map.name;
      this.customMapSelected = false;
    },
    selectCustomMap(map) {
      this.selectedMap = map;
      this.customMapSelected = true;
    },
    createMap() {
      this.$router.push({ path: '/mapCreator', query: { fromMapSelector: true } });
    },
  },
};
</script>
