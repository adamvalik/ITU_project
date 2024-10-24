<script setup>
import { ref, defineProps } from 'vue';
import WeaponShopItem from './WeaponShopItem.vue';

const props = defineProps({
  weapon1: {
    type: Number,
    default: 0,
  },
  weapon2: {
    type: Number,
    default: 0,
  },
  weapon3: {
    type: Number,
    default: 0,
  },
  cash: {
    type: Number,
    default: 0,
  },
});

const cash = ref(props.cash);
const spentCash = ref(0);
const showSpent = ref(false);
const shakeCash = ref(false); // New state for shaking cash display

function updateCash(price) {
  // Check if price is greater than the available cash
  if (price > cash.value) {
    shakeCash.value = true; // Trigger shake animation
    setTimeout(() => {
      shakeCash.value = false; // Reset after shaking
    }, 800); // Duration matches the shake animation
    return; // Exit the function if cash is insufficient
  }

  // Update cash and spent cash
  cash.value -= price;
  spentCash.value = price;
  showSpent.value = true;

  setTimeout(() => {
    showSpent.value = false;
  }, 1000); // Duration for spent cash display
}
</script>

<template>
  <div class="flex flex-col justify-center mt-10">
    <!-- Current Cash Display -->
    <div class="flex flex-col items-center text-4xl font-extrabold text-center min-h-28 relative">
      <div class="flex">
        CASH: <span class="ml-4 text-green-600" :class="{ shake: shakeCash }">{{ cash }} $</span>
      </div>

      <!-- Display Spent Cash with fade-out and slide-down effect -->
      <transition
        leave-active-class="transition-all duration-1000 linear"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-10"
      >
        <!-- Render only if showSpent is true -->
        <span v-if="showSpent" class="ml-36 mt-10 text-red-600 font-bold absolute">
          - {{ spentCash }} $
        </span>
      </transition>
    </div>

    <!-- Weapon Shop Items -->
    <div class="flex">
      <WeaponShopItem :image="require('@/assets/weapon1.png')" price="200" :quantity="props.weapon1" name="Striker" class="m-3" @updateCash="updateCash"></WeaponShopItem>
      <WeaponShopItem :image="require('@/assets/weapon2.png')" price="400" :quantity="props.weapon2" name="Devastator" class="m-3" @updateCash="updateCash"></WeaponShopItem>
      <WeaponShopItem :image="require('@/assets/weapon3.png')" price="600" :quantity="props.weapon3" name="Phantom" class="m-3" @updateCash="updateCash"></WeaponShopItem>
    </div>
  </div>
</template>

<style scoped>
.shake {
  animation: shake 0.8s; /* Adjust duration to match keyframe animation */
}

@keyframes shake {
  0%, 100% { transform: translate(0, 0); color: red; }
  25% { transform: translate(2px, 0); color: black; }
  50% { transform: translate(-2px, 0); color: red; }
  75% { transform: translate(2px, 0); color: black; }
  100% { transform: translate(-2px, 0); color: red; }
}
</style>
