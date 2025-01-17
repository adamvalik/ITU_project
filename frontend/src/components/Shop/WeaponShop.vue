<!-- File: WeaponShop.vue -->
<!-- Author: Dominik Horut (xhorut01) -->

<script setup>

import { ref, defineProps, defineEmits, onMounted } from 'vue';
import WeaponShopItem from './WeaponShopItem.vue';
import apiClient from '@/api';

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

const spentCash = ref(0);

// flags to animate cash changes
const showSpent = ref(false);
const shakeCash = ref(false);

const missiles = ref([]);

const emit = defineEmits(['buy']); 

// fucntion to trigger ammuntion purchase
const buyAmmo = (data) => {
  
  // check that user has enough money to purchase
  if (data.price > props.cash) {

    // show error animation
    shakeCash.value = true;

    setTimeout(() => {
      shakeCash.value = false; 
    }, 800); 
    
    return; 
  }

  spentCash.value = data.price;
  showSpent.value = true;

  emit('buy', {ammo_type: data.ammo_type, price: data.price});

  // show purchase animation
  setTimeout(() => {
    showSpent.value = false;
  }, 1000); 
}

// getter of all missile types
const getMissiles = async () => {

  try {
    const response = await apiClient.get(`/missiles`);
    missiles.value = response.data;

  } catch (error) {
    console.error('Error getting missiles:', error);
  }
}

onMounted(getMissiles);

</script>

<template>

  <div class="flex flex-col justify-center mt-4">

    <!-- Current cash display -->
    <div class="flex flex-col items-center text-4xl font-extrabold text-center min-h-20 relative">

      <div class="flex">
        CASH: <span class="ml-4 text-green-600" :class="{ shake: shakeCash }">{{ cash }} $</span>

        <transition name="fade">

          <div v-if="shakeCash" class=" bg-red-500 border-4 rounded-xl text-xl text-white border-red-600 p-2 font-bold absolute -right-6 -top-1">
            not enough cash
          </div>

      </transition>
      
      </div>

      <!-- Spent cash display -->
      <transition
        leave-active-class="transition-all duration-1000 linear"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-10">

        <span v-if="showSpent" class="ml-36 mt-10 text-red-600 font-bold absolute">
          - {{ spentCash }} $
        </span>

      </transition>

    </div>

    <!-- Ammunition types -->
    <div class="flex">

      <WeaponShopItem :image="require('@/assets/weapon1.png')" :missile="missiles[0]" :quantity="props.weapon1" class="m-3" @buy="buyAmmo"></WeaponShopItem>
      <WeaponShopItem :image="require('@/assets/weapon2.png')" :missile="missiles[1]" :quantity="props.weapon2" class="m-3" @buy="buyAmmo"></WeaponShopItem>
      <WeaponShopItem :image="require('@/assets/weapon3.png')" :missile="missiles[2]" :quantity="props.weapon3" class="m-3" @buy="buyAmmo"></WeaponShopItem>

    </div>

  </div>
  
</template>

<style scoped>

.shake {
  animation: shake 0.8s;
}

/* money shake animation */
@keyframes shake {
  0%, 100% { transform: translate(0, 0); color: red; }
  25% { transform: translate(2px, 0); color: #dc2626; }
  50% { transform: translate(-2px, 0); color: red; }
  75% { transform: translate(2px, 0); color: #dc2626; }
  100% { transform: translate(-2px, 0); color: red; }
}
</style>

<style scoped>

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

</style>