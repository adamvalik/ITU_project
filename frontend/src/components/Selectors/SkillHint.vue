<!-- File: SkillHint.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <div class="relative">
    <div class="group">
      <slot></slot>

      <div
        v-if="text"
        class="absolute bottom-full transform -translate-x-full w-40 p-2 text-white bg-gray-700
        rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
      >
        <h3 class="text-xl font-semibold uppercase text-center">{{ name }}</h3>
        <p>{{ text }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  computed: {
    text() {
      if (this.name === "Armor") {
        return "Increasing armor will give you more health points";
      } else if (this.name === "Power") {
        return "Increasing power will give you more damage";
      } else if (this.name === "Speed") {
        return "Increasing speed will make your tank move faster";
      } else {
        return null;
      }
    },
  },
};
</script>
