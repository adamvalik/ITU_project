<script setup>
import {ref} from 'vue';
import WeaponShopItem from './WeaponShopItem.vue';
const cash = ref(600);
const spentCash = ref(0); 
const showSpent = ref(false); 

function updateCash(price) {
 
  cash.value -= price;

  spentCash.value = price;
  showSpent.value = true;

  
  setTimeout(() => {
    showSpent.value = false;
  }, 50);
}

</script>
<template>
    <div class="flex flex-col justify-center">
      <!-- Current Cash Display -->
      <div class="flex flex-col text-4xl font-extrabold text-center min-h-28 relative">
        <div class="flex ">CASH: <span class="ml-4 text-green-600">{{ cash }} $</span></div>
  
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
        <WeaponShopItem :image="require('@/assets/weapon1.png')" price="200" :quantity="quantity1" name="Striker" class="m-3" @updateCash="updateCash"></WeaponShopItem>
        <WeaponShopItem :image="require('@/assets/weapon2.png')" price="400" :quantity="quantity2" name="Devastator" class="m-3" @updateCash="updateCash"></WeaponShopItem>
        <WeaponShopItem :image="require('@/assets/weapon3.png')" price="600" :quantity="quantity3" name="Phantom" class="m-3" @updateCash="updateCash"></WeaponShopItem>
      </div>
    </div>
  </template>
  