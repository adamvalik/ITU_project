<!--
  File: OperationSelector.vue
  Author: Marek Effenberger (xeffen00)
-->
<template>
  <!-- A button group that allows the user to select an operation for the map. -->
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
      draggable="true"
      @dragstart="onDragStart"
    >
      <img :src="obstructionIcon" alt="Obstruction Icon" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineEmits } from 'vue';

// eslint-disable-next-line no-undef
const props = defineProps({
  activeTheme: String
});

// The currently active button (operation)
const activeButton = ref('');
const emit = defineEmits(['cursor-change']);

// Drag start event handler
const onDragStart = (event) => {
  setActiveButton('obstruction');
  event.dataTransfer.setData('text/plain', obstructionIcon.value);
};

// Set the active button
const setActiveButton = (button) => {
  if (activeButton.value === button) {
    activeButton.value = '';
  } else {
    activeButton.value = button;
  }
};

// Watch the active button and emit the cursor change event
watch(activeButton, (newVal) => {
  emit('cursor-change', newVal);
});

// Computed property for the obstruction icon
const obstructionIcon = computed(() => {
  switch (props.activeTheme) {
    case 'beach':
      return '/assets/cactus_icon.svg';
    case 'winter':
      return '/assets/snowman_icon.svg';
    case 'forest':
    default:
      return '/assets/tree_icon.svg';
  }
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: auto;
  padding: 5px;
  background-color: #1ae4ff;
  border-radius: 12px;
  border: 8px solid #000000;
}

.icon-button {
  border: 8px solid #cbd5e0;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  margin-bottom: 10px;
  transition: transform 0.2s, border-color 0.2s;
  width: auto;
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
  background-color: #f44141;
}

.icon-button.eraser {
  background-color: #0ef6b8;
}

.icon-button.obstruction {
  background-color: #fd7e15;
}

.icon-button.active {
  border-color: #2d3748;
}

.icon-button:not(.active) {
  border-color: #e2e8f0;
}

</style>
