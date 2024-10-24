<template>
  <div :class="['container', activeButton + '-cursor']">
    <button
        class="icon-button pen"
        :class="{ active: activeButton === 'pen' }"
        @click="setActiveButton('pen')"
    >
      <img src="/assets/pen_icon.svg" alt="Pen Icon" />
    </button>
    <button
        class="icon-button eraser"
        :class="{ active: activeButton === 'eraser' }"
        @click="setActiveButton('eraser')"
    >
      <img src="/assets/eraser_icon.svg" alt="Eraser Icon" />
    </button>
    <button
        class="icon-button obstruction"
        :class="{ active: activeButton === 'obstruction' }"
        @click="setActiveButton('obstruction')"
    >
      <img :src="obstructionIcon" alt="Obstruction Icon" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

// eslint-disable-next-line no-undef
const props = defineProps({
  activeTheme: String
});

const activeButton = ref('');
const emit = defineEmits(['cursor-change']);

const setActiveButton = (button) => {
  if (activeButton.value === button) {
    activeButton.value = ''; // Unclick the button if it's already active
  } else {
    activeButton.value = button; // Set the button as active
  }
  console.log(`Active button set to: ${activeButton.value}`); // Debug log
};

watch(activeButton, (newVal) => {
  emit('cursor-change', newVal);
});

const obstructionIcon = computed(() => {
  switch (props.activeTheme) {
    case 'beach':
      return '/assets/cactus_icon.svg'; // Cactus for beach theme
    case 'winter':
      return '/assets/snowman_icon.svg'; // Snowman for winter theme
    case 'forest':
    default:
      return '/assets/tree_icon.svg'; // Tree for forest theme (default)
  }
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column; /* Makes buttons stack vertically */
  align-items: center;
  width: auto; /* Auto width to hug the content */
  padding: 5px;
  background-color: #1ae4ff; /* Dark background color */
  border-radius: 12px;
  border: 8px solid #000000; /* Dark border color */
}

.icon-button {
  border: 8px solid #cbd5e0; /* Light border color */
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  margin-bottom: 10px; /* Adds space between buttons */
  transition: transform 0.2s, border-color 0.2s;
  width: auto; /* Remove fixed width so the buttons aren't too big */
  display: flex;
}

.icon-button img {
  width: 50px;
  height: 50px;
}

.icon-button:hover {
  transform: scale(1.1);
}

.icon-button.pen {
  background-color: #f44141; /* Light yellow */
}

.icon-button.eraser {
  background-color: #0ef6b8; /* Light green */
}

.icon-button.obstruction {
  background-color: #fd7e15; /* Light blue */
}

.icon-button.active {
  border-color: #2d3748; /* Darker border color for active button */
}

.icon-button:not(.active) {
  border-color: #e2e8f0; /* Lighter border color for inactive buttons */
}

</style>