

<template>
  <div @click="playMusic" class="relative flex flex-col justify-center items-center min-h-screen bg-cover bg-center" style="background-image: url('/assets/bg.png');">

    <!-- Multiple Clouds Moving Across the Background -->
    <img v-for="(cloud, index) in clouds" :key="index" :src="cloud.src" :class="cloud.class" @click="playButtonSound" :style="getCloudStyle(index)" />

    <div>
      <h1 class="relative text-7xl font-bold mb-8 z-10">
        TANKS
        <p class="absolute -bottom-4 -right-6 text-xl">1v1</p>
      </h1>
    </div>

    <!-- Language Flags -->
    <img src="/assets/czech-flag.png" alt="cz" class="w-8 h-8 absolute right-16 top-4 z-10" />
    <img src="/assets/uk-flag.png" alt="uk" class="w-8 h-8 absolute right-4 top-4 z-10" />

    <!-- Menu Buttons -->
    <div class="flex flex-col justify-center gap-3 z-10">
      <button @click="showGameModes" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        START GAME
      </button>
      <router-link to="/game" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        TUTORIAL
      </RouterLink>
      <RouterLink to="/mapCreator" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        CREATE MAP
      </router-link>
      <router-link to="/shop" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        SHOP (temp link)
      </router-link>
      <button @click="showSettings" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        SETTINGS
      </button>
    </div>

    <!-- Game Modes Modal -->
    <div v-if="isGameModesVisible" @click="hideGameModes" class="fixed inset-0 flex items-center justify-center gap-20 bg-black bg-opacity-50 z-50">
      <router-link @click.stop to="/chooseTanks" class="h-200 text-2xl font-bold bg-white p-8 rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-48 flex items-center justify-center">
        Classic mode
      </router-link>
      <router-link @click.stop to="/chooseTanks" class="h-200 text-2xl font-bold bg-white p-8 rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-48 flex items-center justify-center">
        Custom mode
      </router-link>
    </div>

    <!-- Modal Window -->
    <div v-if="isSettingsVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <Settings @hideSettings="hideSettings" @updateMusicVolume="updateMusicVolume" />
    </div>

    <!-- Audio Element for Button Click Sound -->
    <!-- <audio ref="buttonSound" :src="buttonSoundSrc" preload="auto"></audio> -->
  </div>

  <footer class="absolute bottom-4 left-4 text-gray-700 text-sm z-10">© Rogalo 2024</footer>
</template>

<script>
import Settings from '../components/Settings/Settings.vue';

export default {
  name: 'MainPage',
  components: {
    Settings,
  },
  data() {
    return {
      isSettingsVisible: false,   // Controls whether the modal is visible
      isGameModesVisible: false,  // Controls whether the game modes modal is visible
      // soundEffectsVolume: 50,     // Default value for sound effects slider
      // buttonSoundSrc: "/assets/another-one.mp3",  // Path to button click sound
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
  methods: {
    // Play button sound effect
    // playButtonSound() {
    //   this.$refs.buttonSound.currentTime = 0; // Reset sound to start
    //   this.$refs.buttonSound.play();
    // },
    // Play background music
    playMusic() {
      this.$emit('playMusic');
    },
    updateMusicVolume(volume) {
      this.$emit('updateMusicVolume', volume);
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
