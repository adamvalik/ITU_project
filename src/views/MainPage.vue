<template>
  <div @click="playMusic" class="relative flex flex-col justify-center items-center min-h-screen bg-cover bg-center" style="background-image: url('/assets/bg.png');">

     <!-- Mute Button Icon in the Corner -->
     <button 
      @click="toggleMute" 
      class="absolute top-4 right-4 bg-sky-300 rounded-full p-2 shadow-lg z-50 hover:bg-sky-400 transition"
    >
      <img 
        :src="isMuted ? '/assets/mute.png' : '/assets/unmute.png'" 
        alt="Mute Toggle" 
        class="w-6 h-6"
      />
    </button>

    <!-- Multiple Clouds Moving Across the Background -->
    <img v-for="(cloud, index) in clouds" :key="index" :src="cloud.src" :class="cloud.class" @click="playButtonSound" :style="getCloudStyle(index)" />

    <div>
      <h1 class="relative text-7xl font-bold mb-8 z-10">
        TANKS
        <p class="absolute -bottom-4 -right-6 text-xl">1v1</p>
      </h1>
    </div>

    <!-- Language Flags -->
    <!-- <img src="/assets/czech-flag.png" alt="cz" class="w-8 h-8 absolute right-16 top-4 z-10" />
    <img src="/assets/uk-flag.png" alt="uk" class="w-8 h-8 absolute right-4 top-4 z-10" /> -->

    <!-- Menu Buttons -->
    <div class="flex flex-col justify-center gap-3 z-10">
      <button @click="showGameModes" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        START GAME
      </button>
      <router-link to="/game" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        TUTORIAL
      </router-link>
      <router-link to="/mapCreator" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        CREATE MAP
      </router-link>
      <button @click="showSettings" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        SETTINGS
      </button>
    </div>

    <!-- Game Modes Modal -->
    <div v-if="isGameModesVisible" @click="hideGameModes" class="fixed inset-0 flex items-center justify-center gap-20 bg-black bg-opacity-50 z-50">
      <router-link @click.stop="submitClassicMode" to="/chooseTanks" class="text-3xl font-bold bg-white p-8 rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-48 flex items-center justify-center">
        Classic mode
      </router-link>
      <div 
        v-if="!customModeSetting"
        @click.stop
        @mouseenter="customModeSetting = true"
        class="text-3xl font-bold bg-white rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-48 flex items-center justify-center"
        key="mode1"
      >
        Custom mode
      </div>
      <div 
        v-else 
        @click.stop 
        class="relative h-48 w-96 bg-white p-8 rounded-lg shadow-2xl flex flex-col gap-2 items-center justify-center hover:bg-gray-100"
        key="mode2"
      >
        <p class="absolute top-4 left-1/4 text-3xl font-bold">Custom mode</p>

        <div class="flex self-start items-center px-4 mt-10 gap-8">
          <label for="timer" class="text-xl font-semibold pr-10">Timer</label>
          <input 
            id="timer" 
            type="checkbox" 
            class="form-checkbox h-6 w-6 text-blue-600 border-gray-300 rounded focus:ring focus:ring-blue-200 focus:ring-opacity-50 hover:border-blue-500" 
            v-model="timer" 
          />
        </div>

        <div class="flex self-start items-center px-4 mb-4 gap-2">
          <label for="wins" class="text-xl font-semibold pr-8">Wins</label>
          
          <!-- Left Button to Decrease -->
          <button 
            @click="decreaseWins" 
            class="bg-gray-300 hover:bg-gray-400 text-gray-700 font-bold py-1 px-2 rounded-lg"
          >
            &#9664;
          </button>

          <!-- Display Number of Wins -->
          <div class="text-2xl font-bold w-8 text-center">
            {{ wins }}
          </div>

          <!-- Right Button to Increase -->
          <button 
            @click="increaseWins" 
            class="bg-gray-300 hover:bg-gray-400 text-gray-700 font-bold py-1 px-2 rounded-lg"
          >
            &#9654;
          </button>
        </div>

        <!-- Go Button -->
        <router-link 
          to="/chooseTanks" 
          @click="submitCustomMode"
          class="absolute bottom-1 right-1 font-bold border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 text-xl py-2 px-6 rounded-2xl mt-4 transition duration-300"
        >
          GO!
        </router-link>
      </div>
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
import axios from 'axios';

export default {
  name: 'MainPage',
  components: {
    Settings,
  },
  data() {
    return {
      wins: 5,
      timer: false,               // Timer setting for custom mode
      customModeSetting: false,
      isSettingsVisible: false,   // Controls whether the modal is visible
      isGameModesVisible: false,  // Controls whether the game modes modal is visible
      isMuted: true,             // Controls whether the background music is muted
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
  async mounted() {
    // set initial music volume to 50%
    try {
      await axios.post(`http://localhost:8000/settings/musicVolume?volume=50`);
    } catch (error) {
      console.error(error);
    }
    // emit the initial mute state
    this.emitMute(); 
  },
  methods: {
    // background music
    playMusic() {
      if (!this.isMuted) 
      this.$emit('playMusic');
    },
    updateMusicVolume(volume) {
      this.isMuted = volume === 0;
      this.emitMute();
      this.$emit('updateMusicVolume', volume);
    },
    toggleMute() {
      this.isMuted = !this.isMuted;
      this.emitMute();
    },
    emitMute() {
      this.$emit('toggleMute', this.isMuted);
    },

    decreaseWins() {
      if (this.wins > 1) {
        this.wins--;
      }
    },    
    increaseWins() {
      this.wins++;
    },
    showSettings() {
      this.isSettingsVisible = true;
    },
    hideSettings() {
      this.isSettingsVisible = false;
    },
    showGameModes() {
      this.isGameModesVisible = true;
    },
    hideGameModes() {
      this.customModeSetting = false;
      this.isGameModesVisible = false;
    },

    async submitClassicMode() {
      try {
        await axios.post('http://localhost:8000/game/mode?mode=classic');
      } catch (error) {
        console.error(error);
      }
    },
    async submitCustomMode() {
      try {
        await axios.post(`http://localhost:8000/game/mode?mode=custom&timer=${this.timer}&wins=${this.wins}`);
      } catch (error) {
        console.error(error);
      }
    },

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