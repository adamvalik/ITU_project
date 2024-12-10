<!-- File: App.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <background-music ref="backgroundMusic"/>
  <div class="flex justify-center items-center h-screen bg-gray-600">
    <div
      class="bg-zinc-400 shadow-lg"
      :style="{
        width: `${gameWidth}px`,
        height: `${gameHeight}px`,
        transform: `scale(${scaleFactor})`,
        transformOrigin: 'center center'
      }"
    >
      <router-view
        @playMusic="playMusic"
        @updateMusicVolume="updateMusicVolume"
        @toggleMute="toggleMute"
        :gameWidth="gameWidth"
        :gameHeight="gameHeight"
        :scaleFactor="scaleFactor"
      />
    </div>
  </div>
</template>

<script>
import BackgroundMusic from './components/Settings/BackgroundMusic.vue';
export default {
  components: {
    BackgroundMusic
  },
  data() {
    return {
      scaleFactor: 1,
      gameWidth: 1440,
      gameHeight: 796,
    };
  },
  mounted() {
    this.calculateScale();
    window.addEventListener("resize", this.calculateScale);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.calculateScale);
  },
  methods: {
    playMusic() {
      this.$refs.backgroundMusic.play();
    },
    updateMusicVolume(volume) {
      this.$refs.backgroundMusic.updateVolume(volume);
    },
    toggleMute(isMuted) {
      this.$refs.backgroundMusic.toggleMute(isMuted);
    },
    calculateScale() {
      const scaleWidth = window.innerWidth / this.gameWidth;
      const scaleHeight = window.innerHeight / this.gameHeight;
      this.scaleFactor = Math.min(scaleWidth, scaleHeight);
    },
  }
};
</script>

