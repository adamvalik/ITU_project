<script setup>
import {defineProps} from 'vue'
const props = defineProps({
    name:{
        type: String,
        default : "Weapon name"
    }
})
</script>
<template>
    <div class="bg-gray-100 border-2 border-gray-500 p-1 px-2 pb-4 w-36 rounded-lg shadow-xl">
        <h1 class="font-black mb-2">{{ props.name }}</h1>
        <div class="border-2 rounded-lg border-gray-500 h-28">
            <div class="h-28 bg-gray-200 flex justify-center items-start">
                <div class="ball"></div>
            </div>
        </div>
    </div>
</template>

<style>
@keyframes fall {
  0% {
    transform: translateY(0); /* Start at the top */
  }
  100% {
    transform: translateY(4rem); /* Small bounce */
  }
}

/* Tailwind Custom Class for Ball */
.ball {
  @apply w-12 h-12 bg-red-500 rounded-full;
  animation: fall 2s ease-in-out infinite;
}
</style>