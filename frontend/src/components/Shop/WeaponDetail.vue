<script setup>
import { ref, defineProps, watch } from 'vue';

// Define props for the component
const props = defineProps({
  name: {
    type: String,
    default: "Weapon name"
  }
});



const getRadius = () => {
  const weapon = props.name;
  if(weapon === "Striker"){
    return 8;
  } else if(weapon === "Devastator"){
    return 12;
  } else{
    return 16;
  }
}

// Reactive variable for explosion state
const exploded = ref(false);

// Function to handle explosion
const handleExplosion = () => {
  exploded.value = true;
};

// Watch for the explosion state to reset it after a short duration
watch(exploded, (newVal) => {
  if (newVal) {
    // Wait for the explosion animation to finish, then reset
    setTimeout(() => {
      exploded.value = false; // Reset to allow falling again
    }, 500); // Duration of the explode animation (0.5s)
  }
});
</script>
<template>
    <div class="bg-gray-100 border-2 border-gray-500 p-1 px-2 pb-4 w-36 rounded-lg shadow-xl">
        <h1 class="font-black mb-2">{{ props.name }}</h1>
        <div class="border-2 rounded-lg border-gray-500 h-28 relative overflow-hidden">
    <!-- Ball falling area -->
    <div class="h-28 bg-gray-200 flex justify-center items-start relative">
      <div
        class="w-3 h-3 bg-red-500 rounded-full absolute"
        :class="{ 'animate-fall': !exploded, 'hidden': exploded }"
        @animationend="handleExplosion"
      ></div>
      
      <div
        class="absolute bottom-0 w-full h-10 bg-green-600"
      >
        <div v-if="exploded" :class="`w-${getRadius()} h-${getRadius()} bg-gray-200 rounded-full absolute left-11 bottom-7`"></div>
      </div>
      <div
        class="explosion w-16 h-16 bg-yellow-400 rounded-full absolute top-4 animate-explode"
        v-if="exploded"
      ></div>
  </div>
    </div>
    </div>
</template>

<style>
@keyframes fall {
  0% {
    transform: translate(-40px, 0);
  }

  100% {
    transform: translate(0, 64px); /* Land straight down */
  }
}

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