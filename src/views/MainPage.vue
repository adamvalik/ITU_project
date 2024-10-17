<template>
  <div class="min-h-screen bg-gray-900 flex flex-col justify-center items-center">
    <!-- Game Title -->
    <h1 class="text-6xl text-white font-bold mb-8">TANK BATTLE</h1>

    <!-- Menu Buttons -->
    <div class="space-y-4">
      <button @click="startGame" class="menu-button bg-green-500 hover:bg-green-700">
        Start Game
      </button>
      <button @click="goTo('tutorial')" class="menu-button bg-blue-500 hover:bg-blue-700">
        Tutorial
      </button>
      <button @click="goTo('sandbox')" class="menu-button bg-yellow-500 hover:bg-yellow-700">
        Sandbox Mode
      </button>
      <button @click="goTo('settings')" class="menu-button bg-gray-500 hover:bg-gray-700">
        Settings
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    // Navigation functions for buttons
    startGame() {
      this.$router.push({ path: '/game' });
    },
    goTo(page) {
      this.$router.push({ path: `/${page}` });
    }
  }
};
</script>

<style scoped>
/* Tailwind CSS utility classes for layout and styling */
.menu-button {
  width: 200px;
  padding: 12px;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.menu-button:focus {
  outline: none;
}

/* Background animation (optional) */
body {
  background-color: #1a202c;
}
</style>
