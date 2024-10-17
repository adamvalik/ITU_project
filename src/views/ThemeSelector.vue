<template>
  <div class="container">
    <button
        class="icon-button beach"
        :class="{ active: activeButton === 'beach' }"
        @click="setActiveButton('beach')"
    >
      <img src="/assets/beach_icon.svg" alt="Beach Icon" />
    </button>
    <button
        class="icon-button forest"
        :class="{ active: activeButton === 'forest' }"
        @click="setActiveButton('forest')"
    >
      <img src="/assets/forest_icon.svg" alt="Forest Icon" />
    </button>
    <button
        class="icon-button winter"
        :class="{ active: activeButton === 'winter' }"
        @click="setActiveButton('winter')"
    >
      <img src="/assets/winter_icon.svg" alt="Winter Icon" />
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const activeButton = ref('forest');
const emit = defineEmits(['theme-change']);

const setActiveButton = (button) => {
  activeButton.value = button;
};

watch(activeButton, (newVal) => {
  emit('theme-change', newVal);
});
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: auto;
  padding: 5px;
  background-color: #94f4e2; /* Dark background color */
  border-radius: 12px;
  border: 8px solid #000000; /* Dark border color */
}

.icon-button {
  border: 8px solid #cbd5e0; /* Light border color */
  border-radius: 12px;
  padding: 5px;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
  display: flex;
  width: auto;
  margin-left : 5px; /* TODO: or 5? */
  margin-right : 5px;
}

.icon-button img {
  width: 40px;
  height: 40px;
}

.icon-button:hover {
  transform: scale(1.1);
}

.icon-button.beach {
  background-color: #fefcbf; /* Light yellow */
}

.icon-button.forest {
  background-color: #c6f6d5; /* Light green */
}

.icon-button.winter {
  background-color: #bee3f8; /* Light blue */
}

.icon-button.active {
  border-color: #2d3748; /* Darker border color for active button */
}

.icon-button:not(.active) {
  border-color: #e2e8f0; /* Lighter border color for inactive buttons */
}
</style>