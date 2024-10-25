<template>
  <background-music ref="backgroundMusic"/>
  <router-view @playMusic="playMusic" @updateMusicVolume="updateMusicVolume" @toggleMute="toggleMute" />
</template>

<script>
import BackgroundMusic from './components/Settings/BackgroundMusic.vue';
export default {
  components: {
    BackgroundMusic
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
    }
  }
};
</script>