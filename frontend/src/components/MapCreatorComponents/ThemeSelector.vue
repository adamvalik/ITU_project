<!--
  File: ThemeSelector.vue
  Author: Marek Effenberger (xeffen00)
-->
<template>
<!--  A button group that allows the user to select a theme for the map.-->
  <div class="flex justify-around items-center w-auto bg-teal-200 rounded-lg border-8 border-black">
    <button
      class="icon-button beach border-8 rounded-lg p-1 transition-transform transform hover:scale-110"
      :class="{
        'border-gray-900': activeButton === 'beach',
        'border-gray-300': activeButton !== 'beach',
      }"
      @click="setActiveButton('beach')"
    >
      <img src="/assets/beach_icon.svg" alt="Beach Icon" class="w-10 h-10" />
    </button>
    <button
      class="icon-button forest border-8 rounded-lg p-1 transition-transform transform hover:scale-110"
      :class="{
        'border-gray-900': activeButton === 'forest',
        'border-gray-300': activeButton !== 'forest',
      }"
      @click="setActiveButton('forest')"
    >
      <img src="/assets/forest_icon.svg" alt="Forest Icon" class="w-10 h-10" />
    </button>
    <button
      class="icon-button winter border-8 rounded-lg p-1 transition-transform transform hover:scale-110"
      :class="{
        'border-gray-900': activeButton === 'winter',
        'border-gray-300': activeButton !== 'winter',
      }"
      @click="setActiveButton('winter')"
    >
      <img src="/assets/winter_icon.svg" alt="Winter Icon" class="w-10 h-10" />
    </button>
  </div>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';

// The currently active button (theme)
const activeButton = ref('forest');
// Emit the theme change event
const emit = defineEmits(['theme-change']);

// Set the active button
const setActiveButton = (button) => {
  activeButton.value = button;
};

// Watch the active button and emit the theme change event
watch(activeButton, (newVal) => {
  emit('theme-change', newVal);
});
</script>

<style scoped>

.icon-button {
  margin: 10px;
}

.icon-button.beach {
  @apply bg-yellow-100;
}

.icon-button.forest {
  @apply bg-green-100;
}

.icon-button.winter {
  @apply bg-blue-100;
}
</style>
