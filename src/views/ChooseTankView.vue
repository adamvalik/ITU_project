<template>
  <div class="flex h-screen">
    <!-- Left Side (Player 1) -->
    <div class="w-1/2 flex flex-col items-center justify-center border-r-2 border-gray-300">

      <!-- Player 1 Name Input -->
      <div class="mb-4">
        <label class="block font-semibold">Enter Name:</label>
        <input v-model="player1.name" type="text" placeholder="Player 1 Name" class="border rounded px-3 py-2 mt-2">
      </div>

      <!-- Player 1 Tank Type -->
      <tank-selector @tank-selected="updateTankSelection(1, $event)" @color-selected="updateColorSelection(1, $event)" />

    </div>

    <!-- Right Side (Player 2) -->
    <div class="w-1/2 flex flex-col items-center justify-center">

      <!-- Player 2 Name Input -->
      <div class="mb-4">
        <label class="block font-semibold">Enter Name:</label>
        <input v-model="player2.name" type="text" placeholder="Player 2 Name" class="border rounded px-3 py-2 mt-2">
      </div>

      <!-- Player 2 Tank Type -->
      <tank-selector @tank-selected="updateTankSelection(2, $event)" @color-selected="updateColorSelection(2, $event)" :is-flipped="true" :default-color="'#0D6BBD'" />
    </div>

    <!-- Footer Buttons -->
    <div class="absolute bottom-4 left-0 right-0 flex justify-between px-8">
      <!-- Back to Main Page Button -->
      <button @click="goBack" class="px-6 py-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
        Back to Main Page
      </button>

      <!-- Proceed to Game Button -->
      <button @click="goToMapEditor" class="px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-200">
        Choose Map
      </button>
    </div>
  </div>
</template>
  
  <script>
  import TankSelector from '@/components/TankSelector.vue';

  export default {
    components: {
      TankSelector
    },
    data() {
      return {
        player1: {
          name: '',
          tank: '',
          color: '#ff0000',
        },
        player2: {
          name: '',
          tank: '',
          color: '#0000ff',
        }
      };
    },
    methods: {
    // Update tank selection for a player
    updateTankSelection(player, selectedTank) {
      if (player === 1) {
        this.player1.tank = selectedTank;
      } else {
        this.player2.tank = selectedTank;
      }
    },

    // Update color selection for a player
    updateColorSelection(player, selectedColor) {
      if (player === 1) {
        this.player1.color = selectedColor;
      } else {
        this.player2.color = selectedColor;
      }
    },

    // Proceed to the map editor

    ///// TODO: jeste se spravne neemitujou barvy
    goToMapEditor() {
      console.log('Player 1 Tank:', this.player1.tank);
      console.log('Player 1 Color:', this.player1.color);
      console.log('Player 2 Tank:', this.player2.tank);
      console.log('Player 2 Color:', this.player2.color);
    }
  }
}
  </script>
  
  <style scoped>
  /* You can add additional styling if needed */
  </style>
  