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
      <!-- Conditionally render the TankSelector once data has been fetched -->
      <tank-selector v-if="!loading" @tank-selected="updateTankSelection(1, $event)" @color-selected="updateColorSelection(1, $event)" :defaultColor="player1.color" :defaultTankType="player1.tankType" />
      
    </div>

    <!-- Right Side (Player 2) -->
    <div class="w-1/2 flex flex-col items-center justify-center">

      <!-- Player 2 Name Input -->
      <div class="mb-4">
        <label class="block font-semibold">Enter Name:</label>
        <input v-model="player2.name" type="text" placeholder="Player 2 Name" class="border rounded px-3 py-2 mt-2">
      </div>

      <!-- Player 2 Tank Type -->
      <!-- Conditionally render the TankSelector once data has been fetched -->
      <tank-selector v-if="!loading" @tank-selected="updateTankSelection(2, $event)" @color-selected="updateColorSelection(2, $event)" :is-flipped="true" :defaultColor="player2.color" :defaultTankType="player2.tankType" />
      
    </div>

    <!-- Footer Buttons -->
    <div class="absolute bottom-4 left-0 right-0 flex justify-between px-8">
      <!-- Back to Main Page Button -->
      <router-link to="/" @click="deleteData" class="px-6 py-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
        Back to Main Page
      </router-link>

      <!-- Proceed to Game Button -->
      <router-link to="/chooseMap" @click="submitData" class="px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-200">
        Choose Map
      </router-link>
    </div>
  </div>
</template>

<script>
import TankSelector from '@/components/Selectors/TankSelector.vue';
import axios from 'axios';

export default {
  components: {
    TankSelector,
  },
  data() {
    return {
      loading: true, 
      player1: {
        name: null,
        tankType: 0,
        color: '#06B559',
        armor: 0,
        power: 0,
        speed: 0,
        skillPoints: 6, 
        money: 1000,
        fuel: 250,
        health: 100,
        weapon1: 0,
        weapon2: 0,
        weapon3: 0,
      },
      player2: {
        name: null,
        tankType: 1,
        color: '#0D6BBD',
        armor: 0,
        power: 0,
        speed: 0,
        skillPoints: 6,
        money: 1000,
        fuel: 250,
        health: 100,
        weapon1: 0,
        weapon2: 0,
        weapon3: 0,
      }
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    // Update tank selection for a player
    updateTankSelection(player, selectedTank) {
      if (player === 1) {
        this.player1.tankType = selectedTank;
      } else {
        this.player2.tankType = selectedTank;
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

    updatePoints(player, usedPoints, name) {
      console.log(player, usedPoints, name);
      name = name.toLowerCase();
      if (player === 1) {
        if (name === "armor") {
          this.player1.armor -= usedPoints;
        } else if (name === "power") {
          this.player1.power -= usedPoints;
        } else if (name === "speed") {
          this.player1.speed -= usedPoints;
        }
      } else {
        if (name === "armor") {
          this.player2.armor -= usedPoints;
        } else if (name === "power") {
          this.player2.power -= usedPoints;
        } else if (name === "speed") {
          this.player2.speed -= usedPoints;
        }
      }
    },

    async fetchData() {
      try {
        const response = await axios.get('http://localhost:8000/players');
        console.log('Fetched players:', response.data);
        const players = response.data;

        if (players[0]) {
          console.log('Player 1 color:', players[0].color);
          this.player1 = players[0];
        }
        if (players[1]) {
          console.log('Player 2 color:', players[1].color);
          this.player2 = players[1];
        }
        
        this.loading = false; // Set loading to false after fetching data

      } catch (error) {
        console.error('Error fetching players:', error);
        this.loading = false; // Set loading to false even if there's an error
      }
    },

    async submitData() {
      // Ensure default names if not provided
      if (!this.player1.name) {
        this.player1.name = "Player 1";
      }
      if (!this.player2.name) {
        this.player2.name = "Player 2";
      }

      console.log("Player 1 data:", this.player1);  // Log the data being sent
      console.log("Player 2 data:", this.player2);  // Log the data being sent

      try {
        await axios.post('http://localhost:8000/players/0', this.player1);
        await axios.post('http://localhost:8000/players/1', this.player2);
      } catch (error) {
        console.error('Error submitting player data:', error);
      }
    },

    async deleteData() {
      try {
        await axios.delete('http://localhost:8000/players');
      } catch (error) {
        console.error('Error deleting player data:', error);
      }
    }

  }
}
</script>

<style scoped>
  /* You can add additional styling if needed */
</style>
