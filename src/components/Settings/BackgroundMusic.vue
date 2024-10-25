<template>
  <audio ref="backgroundMusic" autoplay loop>
    <source src="/assets/music.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
</template>

<script>
export default {
  data() {
    return {
      currentVolume: 0.5
    };
  },
  methods: {
    play() {
      this.$refs.backgroundMusic.play();
    },
    updateVolume(newVolume) {
      this.currentVolume = newVolume;
      this.$refs.backgroundMusic.volume = this.currentVolume; // Update the audio element's volume
    },
    toggleMute(isMuted) {
      this.$refs.backgroundMusic.muted = isMuted;
    }
  },
  mounted() {
    this.$refs.backgroundMusic.volume = this.currentVolume; // Set initial volume
  },

};
</script>

<style scoped>
</style>
