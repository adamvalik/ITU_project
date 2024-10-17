<template>
    <div class="flex h-screen">
      <!-- Left Side (Player 1) -->
      <div class="w-1/2 flex flex-col items-center justify-center border-r-2 border-gray-300">
        <h2 class="text-2xl font-bold mb-4">Player 1</h2>
  
        <!-- Player 1 Name Input -->
        <div class="mb-4">
          <label class="block font-semibold">Enter Name:</label>
          <input v-model="player1.name" type="text" placeholder="Player 1 Name" class="border rounded px-3 py-2 mt-2">
        </div>
  
        <!-- Player 1 Tank Type -->
        <div class="mb-4">
          <label class="block font-semibold">Choose Tank Type:</label>
          <select v-model="player1.tankType" class="border rounded px-3 py-2 mt-2">
            <option disabled value="">Select a tank type</option>
            <option>Heavy Tank</option>
            <option>Light Tank</option>
            <option>Medium Tank</option>
          </select>
        </div>
  
        <!-- Player 1 Color Picker -->
        <div class="mb-4">
          <label class="block font-semibold">Choose Tank Color:</label>
          <input v-model="player1.tankColor" type="color" class="mt-2 w-16 h-16">
        </div>
      </div>
  
      <!-- Right Side (Player 2) -->
      <div class="w-1/2 flex flex-col items-center justify-center">
        <h2 class="text-2xl font-bold mb-4">Player 2</h2>
  
        <!-- Player 2 Name Input -->
        <div class="mb-4">
          <label class="block font-semibold">Enter Name:</label>
          <input v-model="player2.name" type="text" placeholder="Player 2 Name" class="border rounded px-3 py-2 mt-2">
        </div>
  
        <!-- Player 2 Tank Type -->
        <div class="mb-4">
          <label class="block font-semibold">Choose Tank Type:</label>
          <select v-model="player2.tankType" class="border rounded px-3 py-2 mt-2">
            <option disabled value="">Select a tank type</option>
            <option>Heavy Tank</option>
            <option>Light Tank</option>
            <option>Medium Tank</option>
          </select>
        </div>
  
        <!-- Player 2 Color Picker -->
        <div class="mb-4">
          <label class="block font-semibold">Choose Tank Color:</label>
          <input v-model="player2.tankColor" type="color" class="mt-2 w-16 h-16">
        </div>
      </div>
  
      <!-- Footer Buttons -->
      <div class="absolute bottom-4 left-0 right-0 flex justify-between px-8">
        <!-- Back to Main Page Button -->
        <button @click="goBack" class="px-6 py-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
          Back to Main Page
        </button>
  
        <!-- Proceed to Game Button -->
        <button @click="goToMap" class="px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-200">
          Choose Map
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        player1: {
          name: '',
          tankType: '',
          tankColor: '#ff0000',
        },
        player2: {
          name: '',
          tankType: '',
          tankColor: '#0000ff',
        }
      };
    },
    methods: {
      goBack() {
        this.$router.push('/');
      },
      goToMap() {
        // Proceed to the game with the selected settings
        // You can pass player1 and player2 data to the game route via query params or state
        this.$router.push('/chooseMap');
      }
    }
  };
  </script>
  
  <style scoped>
  /* You can add additional styling if needed */
  </style>
  