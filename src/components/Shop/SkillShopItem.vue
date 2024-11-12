<script setup>
import { defineProps, defineEmits, ref, computed } from 'vue';
import SkillDetail from './SkillDetail.vue';

// Props
const props = defineProps({
  image: {
    type: String,
    default: ""
  },
  name: {
    type: String,
    default: ""
  },
  level: {
    type: Number,
    default: 0
  },

  availablePoints:{
    type: Number,
    default: 0,
  }
});

// Reactive current level, initialized from props.level
const currentLevel = ref(props.level);

const emit = defineEmits(['updatePoints']); // Define custom event


// Functions to upgrade/downgrade the level
function upgradeSkill() {
  if (currentLevel.value < maxLevel && props.availablePoints > 0) {
    currentLevel.value += 1;
    emit('updatePoints', -1, props.name);
  }
}

function downgradeSkill() {
  if (currentLevel.value > 0) {
    currentLevel.value -= 1;
    emit('updatePoints', 1, props.name);

  }
}

const showDetail = ref(false);


// Max level
const maxLevel = 5;

// Computed property for effectiveLevel
const effectiveLevel = computed(() => {
  return Math.max(0, Math.min(currentLevel.value, maxLevel));
});
</script>

<template>
  <div class="flex items-start">
    <!-- Armor Label and Icon -->
    
    <!-- Armor Status Bars -->
    <div class="flex items-center">
      
        <div class="relative">
        <SkillDetail
          :isVisible="showDetail"
          skillName="Skill Name"
          description="Skill description"
        />
        </div>
        <img
          :src="props.image"
          class="w-9 h-9 mr-4"
          @mouseover="showDetail = true"
          @mouseleave="showDetail = false"
        />
     
      

      <!-- Active armor bars -->
      <div
        v-for="index in effectiveLevel"
        :key="index"
        class="w-12 h-12 rounded-2xl border-4 bg-yellow-300 border-yellow-400 ml-3"
      ></div>

      <!-- Inactive armor slots -->
      <div
        v-for="index in (maxLevel - effectiveLevel)"
        :key="`inactive-${index}`"
        class="w-12 h-12 rounded-2xl border-4 bg-gray-300 border-gray-400 ml-3"
      >
      </div>

      <!-- Upgrade/ Downgrade Buttons -->
      <div
        class="w-12 h-12 rounded-3xl border-4 bg-green-500 border-green-600 ml-8 flex justify-center items-center cursor-pointer
         hover:bg-green-600 hover:border-green-700 
         active:bg-green-700 active:border-green-800"
  @click="upgradeSkill"
        >
  <p class="text-white font-black text-2xl">+</p>
    </div>

    <div
      class="w-12 h-12 rounded-3xl border-4 bg-red-500 border-red-600 ml-2 flex justify-center items-center cursor-pointer
         hover:bg-red-600 hover:border-red-700 
         active:bg-red-700 active:border-red-800"
        @click="downgradeSkill"
    >
        <p class="text-white font-black text-2xl">-</p>
      </div>

    </div>
  </div>
</template>
