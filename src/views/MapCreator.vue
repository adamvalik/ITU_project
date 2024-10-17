<script setup>
import ThemeSelector from './ThemeSelector.vue';
import OperationSelector from './OperationSelector.vue';
import {ref} from "vue";

const activeTheme = ref('forest'); // Default theme

const updateTheme = (theme) => {
  activeTheme.value = theme;
};
</script>

<template>
  <div class="min-h-screen bg-gray-900 flex flex-col justify-center items-center">
    <h1 class="text-4xl text-white font-bold mb-4">Map Creator</h1>
    <p class="text-white">Welcome to the Map Creator. Here you can create and customize your own maps.</p>
    <ThemeSelector :activeTheme="activeTheme" @theme-change="updateTheme" />
    <OperationSelector :activeTheme="activeTheme" />
  </div>
</template>

<style scoped>

</style>