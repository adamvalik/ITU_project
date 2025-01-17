<!-- File: MainPage.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <div
    @click="playMusic"
    class="relative flex flex-col justify-center items-center overflow-hidden bg-cover bg-center"
    :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`, backgroundImage: `url('/assets/bg.png')` }"
  >
     <!-- mute button-->
     <button
      @click="toggleMute"
      class="absolute top-4 right-4 bg-sky-300 rounded-full p-2 shadow-lg z-50 hover:bg-sky-400"
    >
      <img
        :src="isMuted ? '/assets/mute.png' : '/assets/unmute.png'"
        alt="Mute"
        class="w-6 h-6"
      />
    </button>

    <!-- clouds -->
    <img
      v-for="(cloud, index) in clouds"
      :key="index"
      src="/assets/cloud.png"
      class="cloud absolute w-52 opacity-80"
      :style="getCloudStyle(index)"
    />

    <!-- header Tanks 1v1 -->
    <div>
      <h1 class="relative text-7xl font-bold mb-8 z-10">
        TANKS
        <p class="absolute -bottom-4 -right-6 text-xl">1v1</p>
      </h1>
    </div>

    <!-- menu buttons -->
    <div class="flex flex-col justify-center gap-3 z-10">
      <button @click="showGameModes" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        START GAME
      </button>
      <button @click="createMap" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        CREATE MAP
      </button>
      <button @click="showSettings" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl">
        SETTINGS
      </button>
    </div>

    <!-- game modes modal -->
    <div v-if="isGameModesVisible" @click="hideGameModes" class="fixed inset-0 flex items-center justify-center gap-20 bg-black bg-opacity-50 z-50">
      <!-- classic mode tile -->
      <router-link @click.stop="submitClassicMode" to="/chooseTanks" class="text-3xl font-bold bg-white p-8 rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-52 flex items-center justify-center">
        Classic mode
      </router-link>

      <!-- custom mode tile -->
      <div
        v-if="!customModeSetting"
        @click.stop
        @mouseenter="customModeSetting = true"
        class="text-3xl font-bold bg-white rounded-lg shadow-2xl hover:bg-gray-100 w-96 h-52 flex items-center justify-center"
      >
        Custom mode
      </div>

      <!-- custom mode tile - expand on mouseenter -->
      <div
        v-else
        @click.stop
        class="relative h-52 w-96 bg-white p-8 rounded-lg shadow-2xl flex flex-col gap-2 items-center justify-center hover:bg-gray-100"
      >
        <p class="absolute top-4 left-1/4 text-3xl font-bold">Custom mode</p>

        <!-- checkbox, whether to use timer -->
        <div class="flex self-start items-center mt-12 px-2 gap-8">
          <label for="isTimer" class="text-xl font-semibold pr-10">Timer</label>
          <input
            id="isTimes"
            type="checkbox"
            class="form-checkbox h-6 w-6 text-blue-600 border-gray-300 rounded focus:ring focus:ring-blue-200 focus:ring-opacity-50 hover:border-blue-500"
            v-model="isTimer"
          />
        </div>

        <!-- if timer is checked, choose seconds per turn -->
        <div class="flex self-start items-center px-2 gap-1">
          <label for="timePerTurn" class="text-xl font-semibold pr-8">Per turn</label>
          <input
            type="number"
            v-model="timePerTurn"
            class="w-16 h-8 text-xl text-center border-2 border-gray-300 rounded-lg"
            :disabled="!isTimer"
            :class="{ 'bg-gray-200, opacity-70': !isTimer }"
          />
          <p class="text-xl">sec</p>
        </div>

        <!-- choose number of wins to end the game -->
        <div class="flex self-start items-center mb-4 px-2 gap-2">
          <label for="toWins" class="text-xl font-semibold pr-8">Wins</label>

          <!-- decrease -->
          <button
            @click="decreaseWins"
            class="bg-gray-300 hover:bg-gray-400 text-gray-700 font-bold py-1 px-2 rounded-lg"
          >
            &#9664;
          </button>

          <!-- number of wins -->
          <div class="text-xl w-8 text-center">
            {{ toWins }}
          </div>

          <!-- increase -->
          <button
            @click="increaseWins"
            class="bg-gray-300 hover:bg-gray-400 text-gray-700 font-bold py-1 px-2 rounded-lg"
          >
            &#9654;
          </button>
        </div>

        <!-- go button -->
        <router-link
          to="/chooseTanks"
          @click="submitCustomMode"
          class="absolute bottom-1 right-1 font-bold border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 text-xl py-2 px-6 rounded-2xl mt-4 transition duration-300"
        >
          GO!
        </router-link>
      </div>
    </div>

    <!-- settings -->
    <div v-if="isSettingsVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <Settings @hideSettings="hideSettings" @updateMusicVolume="updateMusicVolume" />
    </div>

    <!-- footer with the copyright -->
    <footer class="absolute bottom-4 left-4 text-gray-700 text-sm z-10">© Rogalo 2024</footer>
  </div>

</template>

<script>
import Settings from '../components/Settings/Settings.vue';
import apiClient from '@/api';

export default {
  components: {
    Settings,
  },
  props: {
    gameWidth: Number,
    gameHeight: Number,
  },
  data() {
    return {
      cloudCount: 10,
      // initial custom mode settings
      toWins: 5,
      isTimer: false,
      timePerTurn: 30,
      // visibility controls
      customModeSetting: false,
      isSettingsVisible: false,
      isGameModesVisible: false,
      isMuted: true,
    };
  },
  computed: {
    clouds() {
      return Array.from({ length: this.cloudCount });
    },
  },
  created() {
    this.initializeCloudStyles();
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
      // re-emit to the App.vue
      this.$emit('updateMusicVolume', volume);
    },
    toggleMute() {
      this.isMuted = !this.isMuted;
      this.emitMute();
    },
    emitMute() {
      this.$emit('toggleMute', this.isMuted);
    },

    // custom mode settings
    decreaseWins() {
      if (this.toWins > 1) {
        this.toWins--;
      }
    },
    increaseWins() {
      this.toWins++;
    },

    // change visibility of modals
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

    // open map creator
    createMap() {
      this.$router.push({ path: '/mapCreator', query: { fromMapSelector: false } });
    },

    // game mode submit also means to clear (reset) previous game&players settings
    async submitClassicMode() {
      try {
          await apiClient.delete('/players/reset');
          await apiClient.delete('/game/reset');
        } catch (error) {
          console.error(error);
        }
    },
    async submitCustomMode() {
      try {
          await apiClient.delete('/players/reset');
          await apiClient.delete('/game/reset');
          await apiClient.post('/game/custom_mode', {
            isTimer: this.isTimer,
            timePerTurn: this.timePerTurn,
            toWins: this.toWins,
          });
        } catch (error) {
          console.error(error);
        }
    },

    // cloud animation
    getPredefinedValue(array, index) {
      return array[index % array.length];
    },
    getCloudStyle(index) {
      const topValues = [-10, 30, 60, 90, 120, 150, 180];
      const durationValues = [20, 25, 30, 35, 40];
      const zIndexValues = [1, 40];
      const leftOffsets = [-300, -250, -200, -150];

      const top = this.getPredefinedValue(topValues, index);
      const animDuration = this.getPredefinedValue(durationValues, index);
      const zIndex = this.getPredefinedValue(zIndexValues, index);
      const leftOffset = this.getPredefinedValue(leftOffsets, index);

      return `top: ${top}px; animation-duration: ${animDuration}s; z-index: ${zIndex}; left: ${leftOffset}px;`;
    },
    initializeCloudStyles() {
    this.cloudStyles = Array.from(
        { length: this.cloudCount },
        (_, index) => this.getCloudStyle(index)
      );
    },
  },
};
</script>

<style scoped>
.cloud {
  animation: moveCloud linear infinite;
}

@keyframes moveCloud {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(120vw); /* move off-screen */
  }
}
</style>
