<!-- File: SkillShopItem.vue -->
<!-- Author: Dominik Horut (xhorut01) -->

<script setup>

import { defineProps, defineEmits, computed, ref} from 'vue';
import SkillDetail from './SkillDetail.vue';

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


const emit = defineEmits(['upgrade', 'downgrade']); 

// error explanation flags
const showMaxUpgrade = ref(false);
const showNoPoints = ref(false);
const showSkillIsZero = ref(false);

// functio to trigger skill upgrade
const upgradeSkill = () => {

  // check that user will not cross max level or upgrade with 0 free skill points
  if (props.level < maxLevel && props.availablePoints > 0) {
    emit('upgrade', {name: props.name});

  // user tried to upgrade with 0 free skill points
  } else if(props.availablePoints == 0){
    showNoPoints.value = true;

    setTimeout(() => {
      showNoPoints.value = false;
    }, 1500);

  // user tried to upgrade skill with max level
  }else if(props.level == maxLevel){
    showMaxUpgrade.value = true;

    setTimeout(() => {
      showMaxUpgrade.value = false;
    }, 1500);
  
  }
}

// functio to trigger skill downgrade
const downgradeSkill = () => {

  // check that user will not downgrade skill with 0 points
  if (props.level > 0) {
    emit('downgrade', {name: props.name});

  // user tried to downgrade skill with 0 points
  }else{
    showSkillIsZero.value = true;

    setTimeout(() => {
      showSkillIsZero.value = false;
    }, 1500);
  }
}

// getter of description of skill
const getDescription = () => {

  if(props.name == "armor"){
    return "Tank has more hp";

  }else if(props.name == "power"){
    return "Missiles deal more damage";

  }else if(props.name == "speed"){
    return "Tank drives further on less fuel";
  }
}

// max level of skill
const maxLevel = 5;

// current level of skill
const effectiveLevel = computed(() => {
  return Math.max(0, Math.min(props.level, maxLevel));
});

</script>

<template>

  <div class="flex items-start">
   
    <div class="flex items-center relative">
      
      <!-- Skill detail  -->
      <div class="relative group">
        <div class="absolute opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none group-hover:pointer-events-auto">
          <SkillDetail :skillName="props.name" :description="getDescription()"/>
        </div>
        
        <!-- Skill image  -->
        <img :src="props.image" class="w-9 h-9 mr-4" @mouseover="showDetail = true" @mouseleave="showDetail = false"/>
      </div>
     
      

      <!-- Acitve skill points -->
      <div
        v-for="index in effectiveLevel"
        :key="index"
        class="w-12 h-12 rounded-2xl border-4 bg-yellow-300 border-yellow-400 ml-3"
      ></div>

      <!-- Inactive skill points -->
      <div
        v-for="index in (maxLevel - effectiveLevel)"
        :key="`inactive-${index}`"
        class="w-12 h-12 rounded-2xl border-4 bg-gray-300 border-gray-400 ml-3"
      ></div>

      <!-- Upgrade button -->
      <div
        class="w-12 h-12 rounded-3xl border-4 bg-green-500 border-green-600 ml-8 flex justify-center items-center cursor-pointer
        hover:bg-green-600 hover:border-green-700
        active:bg-green-700 active:border-green-800"
        @click="upgradeSkill">

        <p class="text-white font-black text-2xl">+</p>
      </div>

      <!-- Downgrade button -->
      <div
        class="w-12 h-12 rounded-3xl border-4 bg-red-500 border-red-600 ml-2 flex justify-center items-center cursor-pointer
        hover:bg-red-600 hover:border-red-700
        active:bg-red-700 active:border-red-800"
        @click="downgradeSkill">

          <p class="text-white font-black text-2xl">-</p>
      </div>

      <!-- Error context descriptions -->
      <transition name="fade">
        <div v-if="showMaxUpgrade" class=" bg-gray-300 border-4 rounded-xl opacity-75 border-gray-400 p-2 font-bold absolute left-24">
          {{ props.name }} is on maximum level
        </div>
      </transition>

      <transition name="fade">
        <div v-if="showNoPoints" class=" bg-gray-300 border-4 rounded-xl opacity-75 border-gray-400 p-2 font-bold absolute left-32">
          no free skill points
        </div>
      </transition>

      <transition name="fade">
        <div v-if="showSkillIsZero" class=" bg-gray-300 border-4 rounded-xl opacity-75 border-gray-400 p-2 font-bold absolute left-28">
          no points to be removed
        </div>
      </transition>

    </div>
    
  </div>

</template>

<style scoped>

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

</style>