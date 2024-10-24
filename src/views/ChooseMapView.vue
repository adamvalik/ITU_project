<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <h1 class="text-4xl font-bold mb-8">Choose Map</h1>

    <!-- Default Maps Section -->
    <div class="grid grid-cols-3 gap-6 mb-8">
      <div 
        v-for="(map, index) in defaultMaps" 
        :key="index" 
        @click="selectMap(map)"
        :class="['border-4 p-4 cursor-pointer rounded-lg', selectedMap === map ? 'border-green-500' : 'border-gray-300']"
      >
        <img :src="map.image" :alt="map.name" class="w-full h-40 object-cover rounded-lg">
        <p class="text-center font-semibold mt-2">{{ map.name }}</p>
      </div>
    </div>

    <!-- Custom Maps Section -->
    <h2 class="text-2xl font-bold mb-4">Choose Custom Map</h2>
    <div class="grid grid-cols-3 gap-6 mb-8">
      <div 
        v-for="(map, index) in customMaps" 
        :key="index" 
        @click="selectMap(map)"
        :class="['border-4 p-4 cursor-pointer rounded-lg', selectedMap === map ? 'border-green-500' : 'border-gray-300']"
      >
        <img :src="map.image" :alt="map.name" class="w-full h-40 object-cover rounded-lg">
        <p class="text-center font-semibold mt-2">{{ map.name }}</p>
      </div>
    </div>

    <!-- Footer Buttons -->
    <div class="flex justify-between w-full px-8 mt-8">
      <!-- Back to Choose Tank View Button -->
      <button @click="goBackToChooseTank" class="px-6 py-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
        Back to Choose Tank
      </button>

      <!-- Proceed to Game Button -->
      <button @click="goToGame" :disabled="!selectedMap" class="px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed">
        Start Game
      </button>
    </div>
  </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        selectedMap: null, // Holds the currently selected map
        // Default maps data
        defaultMaps: [
          { name: 'Desert Map', image: '/assets/bg.png' },
          { name: 'Forest Map', image: '/assets/bg.png' },
          { name: 'Mountain Map', image: '/assets/bg.png' }
        ],
        // Custom maps data (you can populate this dynamically later)
        customMaps: [
          { name: 'Custom Map 1', image: '/assets/bg.png' },
          { name: 'Custom Map 2', image: '/assets/bg.png' },
          { name: 'Custom Map 3', image: '/assets/bg.png' }
        ]
      };
    },
    methods: {
      // Select a map from either default or custom maps
      selectMap(map) {
        this.selectedMap = map;
      },
      // Navigate back to the ChooseTankView
      goBackToChooseTank() {
        this.$router.push('/chooseTanks');
      },
      // Proceed to the game, passing the selected map
      goToGame() {
        if (this.selectedMap) {
          this.$router.push({
            path: '/game',
            query: { selectedMap: this.selectedMap.name }
          });
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Additional styling if necessary */
  </style>
  