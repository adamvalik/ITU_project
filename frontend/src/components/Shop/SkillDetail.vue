<script setup>
import {defineProps} from 'vue';

const props = defineProps({
  skillName:{
    type: String,
    default: "Skill"
  },
  description:{
    type: String,
    default: "Description"
  },
  isVisible: {
    type: Boolean
  }
})
</script>

<template>
<div
    class="absolute -top-32 left-1 flex flex-col justify-center items-center border-2 bg-gray-100 border-gray-500 p-2 rounded-lg transition-opacity duration-300 z-50"
    :class="{ 'opacity-100': props.isVisible, 'opacity-0': !props.isVisible }"
  >
    <h1>{{ props.skillName }}</h1>
    <p>{{ props.description }}</p>
  </div>
</template>