<script setup>
import { defineProps, defineEmits, computed} from 'vue';
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


const emit = defineEmits(['upgrade', 'downgrade']); 

function upgradeSkill() {
  if (props.level < maxLevel && props.availablePoints > 0) {
    emit('upgrade', {name: props.name});
  }
}

function downgradeSkill() {
  if (props.level > 0) {
    emit('downgrade', {name: props.name});

  }
}

function getDescription(){
  if(props.name == "armor"){
    return "Tank has more hp";

  }else if(props.name == "power"){
    return "Missiles deal more damage";

  }else if(props.name == "speed"){
    return "Tank drives further on less fuel";
  }
}


// Max level
const maxLevel = 5;

// Computed property for effectiveLevel
const effectiveLevel = computed(() => {
  return Math.max(0, Math.min(props.level, maxLevel));
});
</script>

<template>
  <div class="flex items-start">
    <!-- Armor Label and Icon -->

    <!-- Armor Status Bars -->
    <div class="flex items-center">
      
        <div class="relative group">
          <div class="absolute opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none group-hover:pointer-events-auto">
          <SkillDetail
            
            :skillName="props.name"
            :description="getDescription()"
          />
          </div>
        
        <img
          :src="props.image"
          class="w-9 h-9 mr-4"
          @mouseover="showDetail = true"
          @mouseleave="showDetail = false"
        />
      </div>
     
      

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
