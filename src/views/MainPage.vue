<template>
  <div @click="playMusic" class="relative flex flex-col justify-center items-center min-h-screen bg-cover bg-center" style="background-image: url('/assets/bg.png');">
    
    <!-- Multiple Clouds Moving Across the Background -->
    <img v-for="(cloud, index) in clouds" :key="index" :src="cloud.src" :class="cloud.class" @click="playButtonSound" :style="getCloudStyle(index)" />

    <!-- Game Title -->
    <h1 class="text-7xl font-bold mb-8 z-10">TANKS</h1>

    <!-- Language Flags -->
    <img src="/assets/czech-flag.png" alt="cz" class="w-8 h-8 absolute right-16 top-4 z-10" />
    <img src="/assets/uk-flag.png" alt="uk" class="w-8 h-8 absolute right-4 top-4 z-10" />

    <!-- Menu Buttons -->
    <div class="flex flex-col justify-center gap-3 z-10">
      <button @click="showGameModes" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        START GAME
      </button>
      <RouterLink to="/tutorial" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        TUTORIAL
      </RouterLink>
      <RouterLink to="/mapCreator" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        CREATE MAP
      </RouterLink>
      <button @click="showSettings" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        SETTINGS
      </button>
    </div>

    <!-- Game Modes Modal -->
    <div v-if="isGameModesVisible" @click="hideGameModes" class="fixed inset-0 flex items-center justify-center gap-20 bg-black bg-opacity-50 z-50">
      <RouterLink @click.stop to="/chooseTanks" class="h-200 text-2xl font-bold bg-white p-8 rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-48 flex items-center justify-center">
        Classic mode
      </RouterLink>
      <RouterLink @click.stop to="/chooseTanks" class="h-200 text-2xl font-bold bg-white p-8 rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-48 flex items-center justify-center">
        Custom mode
      </RouterLink>
    </div>

    <!-- Modal Window -->
    <div v-if="isSettingsVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="bg-white p-8 rounded-lg shadow-lg w-96 text-center">
        <h2 class="text-2xl font-bold mb-4">Settings</h2>

        <!-- Sound Effects Slider -->
        <div class="mb-4">
          <label class="font-semibold text-lg">Sound Effects: {{ soundEffectsVolume }}%</label>
          <input 
            type="range" 
            min="0" 
            max="100" 
            v-model="soundEffectsVolume"
            class="w-full mt-2"
          >
        </div>

        <!-- Music Volume Slider -->
        <div class="mb-4">
          <label class="font-semibold text-lg">Music Volume: {{ musicVolume }}%</label>
          <input 
            type="range" 
            min="0" 
            max="100" 
            v-model="musicVolume"
            class="w-full mt-2"
          >
        </div>

        <!-- Close button -->
        <button @click="hideSettings" class="mt-8 px-6 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
          Close
        </button>
      </div>
    </div>

    <!-- Audio Element for Button Click Sound -->
    <audio ref="buttonSound" :src="buttonSoundSrc" preload="auto"></audio>

    <!-- Audio Element (Invisible) -->
    <audio ref="backgroundMusic" autoplay loop>
      <source src="../assets/music.mp3" type="audio/mpeg">
    </audio>
  </div>

  <footer class="absolute bottom-4 left-4 text-gray-700 text-sm z-10">© Rogalo 2024</footer>
</template>

<script>
export default {
  name: 'MainPage',
  data() {
    return {
      isSettingsVisible: false,   // Controls whether the modal is visible
      isGameModesVisible: false,  // Controls whether the game modes modal is visible
      soundEffectsVolume: 50,     // Default value for sound effects slider
      musicVolume: 0,            // Default value for music slider
      buttonSoundSrc: "/assets/another-one.mp3",  // Path to button click sound
      // Array of cloud properties for dynamic rendering
      clouds: [
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 70px; animation-duration: 20s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: -10px; animation-duration: 30s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 150px; animation-duration: 35s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 170px; animation-duration: 25s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 50px; animation-duration: 40s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 120px; animation-duration: 27s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 180px; animation-duration: 23s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 80px; animation-duration: 22s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 60px; animation-duration: 34s;' },
        { src: '/assets/cloud.png', class: 'cloud', style: 'top: 130px; animation-duration: 28s;' },
      ],
    };
  },
  mounted() {
    // Set initial volume when component mounts
    this.$refs.backgroundMusic.volume = this.musicVolume / 100;
  },
  watch: {
    // Watch for changes to the music volume slider and update audio element volume
    musicVolume(newValue) {
      this.$refs.backgroundMusic.volume = newValue / 100;
    },
    // Watch for changes to the sound effects volume slider and update button sound volume
    soundEffectsVolume(newValue) {
      this.$refs.buttonSound.volume = newValue / 100;
    }
  },
  methods: {
    // Play button sound effect
    playButtonSound() {
      this.$refs.buttonSound.currentTime = 0; // Reset sound to start
      this.$refs.buttonSound.play();
    },
    // Play background music
    playMusic() {
      this.$refs.backgroundMusic.play();
    },
    // Show the settings modal
    showSettings() {
      this.isSettingsVisible = true;
    },
    // Hide the settings modal
    hideSettings() {
      this.isSettingsVisible = false;
    },
    // Show the game modes modal
    showGameModes() {
      this.isGameModesVisible = true;
    },
    // Hide the game modes modal
    hideGameModes() {
      this.isGameModesVisible = false;
    },
    // Get cloud style dynamically based on the index
    getCloudStyle(index) {
      const baseStyle = this.clouds[index].style;
      const zIndex = index % 2 === 0 ? 1 : 40;  // Set z-index based on even or odd index
      return `${baseStyle} z-index: ${zIndex};`;
    }
  },
};
</script>

<style scoped>
/* Cloud Animation */
.cloud {
  position: absolute;
  width: 200px; /* Adjust size */
  left: -150px; /* Start off-screen on the left */
  animation: moveCloud linear infinite;
  opacity: 85%;
}

@keyframes moveCloud {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(120vw); /* Move to the right, off-screen */
  }
}
</style>
