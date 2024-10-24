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
export default {
  data() {
    return {
      musicVolume: 50,
    };
  },
  methods: {
    updateMusicVolume() {
      this.$emit('updateMusicVolume', this.musicVolume / 100);
    },
    closeSettings() {
      this.$emit('hideSettings');
    },
  },
};
</script>