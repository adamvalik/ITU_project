<!-- File: WeaponDetail.vue -->
<!-- Author: Dominik Horut (xhorut01) -->

<script setup>

import { ref, defineProps, watch } from 'vue';

const props = defineProps({

  missile: {
    type: Object,
  }
});

const radius = ref(0); 

// getter of radius to be used in weapon showcase
const getRadius = () => {

  if (props.missile?.radius === 30) {
    return 10;

  } else if (props.missile?.radius === 40) {
    return 16;

  } else if (props.missile?.radius === 50) {
    return 20;

  } else {
    return 0; 
  }
};

// explosion animation flag
const exploded = ref(false);

const handleExplosion = () => {
  exploded.value = true;
};

watch(exploded, (newVal) => {
  if (newVal) {
    setTimeout(() => {
      exploded.value = false; 
    }, 500); 
  }
});

watch(
  () => props.missile, 
  (newMissile) => {
    if (newMissile) {
      radius.value = getRadius();
    }
  }, 
  { immediate: true } 
);

</script>

<template>

  <div class="bg-gray-100 border-2 border-gray-500 p-1 px-2 pb-4 w-36 rounded-lg shadow-xl">

    <h1 class="font-black mb-2">{{ props.missile ? props.missile.name : 'Loading...' }}</h1>

    <div class="border-2 rounded-lg border-gray-500 h-28 relative overflow-hidden">

      <div class="h-28 bg-gray-200 flex justify-center items-start relative">

        <!-- Missile -->
        <div
          class="w-3 h-3 bg-red-500 rounded-full absolute"
          :class="{ 'animate-fall': !exploded, 'hidden': exploded }"
          @animationend="handleExplosion"
        ></div>
        
        <!-- Damage area -->
        <div class="absolute bottom-0 w-full h-10 bg-green-600">
          <div v-if="exploded" :class="`w-${radius} h-${radius} bg-gray-200 rounded-full absolute left-8 bottom-4`"></div>
        </div>

        <!-- Explosion -->
        <div
          class="explosion w-16 h-16 bg-yellow-400 rounded-full absolute top-4 animate-explode text-red-600 font-bold "
          v-if="exploded"
        >-{{props.missile ? props.missile.damage : 'Loading...'}}</div>

      </div>

    </div>

  </div>

</template>

<style>

/* missile fall animation */
@keyframes fall {
  0% {
    transform: translate(-40px, 0);
  }

  100% {
    transform: translate(0, 64px); 
  }
}

/* missile explosion animation */
@keyframes explode {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

.animate-fall {
  animation: fall 1s ease-in forwards;
}

.animate-explode {
  animation: explode 1s ease-out forwards;
}

.hidden {
  display: none;
}

</style>
