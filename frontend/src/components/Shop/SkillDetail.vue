<!-- File: SkillDetail.vue -->
<!-- Author: Dominik Horut (xhorut01) -->

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
})

</script>

<template>

  <div class="absolute -top-10 rounded-lg right-0 border-2 bg-gray-100 border-gray-500 p-2 w-48">

    <!-- Skill description -->
    <div class="flex flex-col items-center ">

      <h1 class="font-bold text-lg">{{ props.skillName.charAt(0).toUpperCase() + props.skillName.slice(1)}}</h1>
      <p class="text-sm text-center">{{ props.description }}</p>

    </div>

  </div>

</template>