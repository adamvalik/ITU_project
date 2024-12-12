<!-- File: SkillSelector.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <div class="flex gap-1 items-center my-1">
    <!-- hint about the meaning of the skill -->
    <SkillHint :name="name" class="pr-2 cursor-pointer">
      <img :src="image" :alt="name" class="w-8 h-8" />
    </SkillHint>
    <!-- 5 levels of skill -->
    <div
      v-for="n in 5"
      :key="n"
      @click="setSkillLevel(n)"
      @mouseenter="hoverSkillLevel(n)"
      @mouseleave="hoverSkillLevel(0)"
      class="w-12 h-12 rounded-2xl border-4 bg-gray-300 border-gray-400 cursor-pointer"
      :class="[
        {'bg-yellow-300 border-yellow-400': n <= currentLevel,
        'bg-yellow-100 border-yellow-200': n <= hoverLevel }]"
    ></div>
  </div>
</template>

<script>
import SkillHint from './SkillHint.vue';

export default {
  components: {
    SkillHint
  },
  props: {
    currentLevel: {
      type: Number,
      required: true
    },
    freePoints: {
      type: Number,
      required: true
    },
    image: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      hoverLevel: 0
    };
  },
  methods: {
    setSkillLevel(level) {
      var setLevel = level;
      // clear the level when setting the same level
      if (setLevel === this.currentLevel) {
        setLevel = 0;
      }
      // set the level to the maximum possible if wanted even more
      if (setLevel > this.hoverLevel) {
        setLevel = this.hoverLevel;
      }
      const pointsToAdd = setLevel - this.currentLevel;

      // check if there are enough free points
      if (this.freePoints - pointsToAdd >= 0) {
        this.$emit('update-skill', setLevel);
        this.$emit('update-free-points', this.freePoints - pointsToAdd);
      }
      // clear the hover level to see clicked level
      this.hoverLevel = 0;
    },
    hoverSkillLevel(level) {
      // show the level that would be set (based on the free skill point)
      const maxLevel = this.currentLevel + this.freePoints;
      this.hoverLevel = (level > maxLevel) ? maxLevel : level;
    }
  }
};
</script>
