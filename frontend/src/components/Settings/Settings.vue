<!-- File: Settings.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <div class="bg-white p-8 rounded-lg shadow-lg w-96 text-center">
    <h2 class="text-2xl font-bold mb-4">Settings</h2>

    <div class="mb-4">
      <label class="font-semibold text-lg">Music Volume: {{ musicVolume }}%</label>
      <input
        type="range"
        min="0"
        max="100"
        v-model="musicVolume"
        @input="updateMusicVolume"
        class="w-full mt-2"
      >
    </div>

    <button @click="closeSettings" class="mt-8 px-6 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
      Close
    </button>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  data() {
    return {
      musicVolume: 0,
    };
  },
  async mounted() {
    await this.fetchMusicVolume();
  },
  methods: {
    updateMusicVolume() {
      // emit the event from settings all the way to the app where BackgroundMusic component is
      this.$emit('updateMusicVolume', this.musicVolume / 100);
    },
    async fetchMusicVolume() {
      try {
        const response = await apiClient.get('settings/musicVolume');
        this.musicVolume = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async closeSettings() {
      // store the music volume in the database
      try {
        await apiClient.post('settings/musicVolume', { volume: this.musicVolume });
      } catch (error) {
        console.error(error);
      }
      this.$emit('hideSettings');
    },
  },
};
</script>
