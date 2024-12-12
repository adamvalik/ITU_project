<!--
  File: SaveMap.vue
  Author: Marek Effenberger (xeffen00)
-->
<template>
  <!-- A popup that allows the user to save the map. Allowing to add name. Closed when clicked Outside.-->
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center" @click="handleOverlayClick">
    <div class="bg-white p-6 rounded-lg shadow-lg w-96" @click.stop>
      <h2 class="text-2xl font-bold mb-4">Save Map</h2>
      <label for="mapName" class="block text-lg mb-2">Map Name:</label>
      <input v-model="mapName" id="mapName" type="text" class="w-full p-2 border border-gray-300 rounded mb-4" />
      <div class="flex justify-between">
        <button @click="saveMap" class="bg-green-300 hover:bg-green-400 text-green-700 font-bold py-2 px-4 rounded">
          Save and Return
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  visible: Boolean,
  onSave: Function,
  onClose: Function,
});

const mapName = ref('');

// Save the map and close the popup (the name is stored in mapName)
const saveMap = () => {
  props.onSave(mapName.value);
  props.onClose();
};

// Close the popup when clicked outside
const handleOverlayClick = () => {
  props.onClose();
};
</script>
