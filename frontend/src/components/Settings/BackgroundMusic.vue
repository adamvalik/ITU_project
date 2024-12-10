<!-- File: BackgroundMusic.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <!-- audio element for the background music -->
  <audio ref="backgroundMusic" autoplay loop>
    <source src="/assets/music.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
</template>

<script>
export default {
  methods: {
    play() {
      this.$refs.backgroundMusic.play();
    },
    updateVolume(newVolume) {
      this.$refs.backgroundMusic.volume = newVolume;
    },
    toggleMute(isMuted) {
      this.$refs.backgroundMusic.muted = isMuted;
    }
  },
  mounted() {
    this.$refs.backgroundMusic.volume = 0;
  },
};
</script>

<style scoped>
</style>
