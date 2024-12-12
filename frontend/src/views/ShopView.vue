<!-- File: ShopView.vue -->
<!-- Author: Dominik Horut (xhorut01) -->

<script setup>
import {ref, defineProps, onMounted} from 'vue';
import PlayerShopCard from '@/components/Shop/PlayerShopCard.vue';
import apiClient from '@/api';

const props = defineProps ({
  
    gameWidth: {
      type: Number,
      required: true,
    },
    gameHeight: {
      type: Number,
      required: true,
    }
});

const players = ref([]);

const getPlayers = async () => {
  try {
    const response = await apiClient.get('/players');
    players.value = response.data;

  } catch (error) {
    console.error(error);
  }
}

onMounted(getPlayers)

</script>

<template>
    
    <div class="flex flex-col items-center bg-cover bg-center" :style="{ width: `${props.gameWidth}px`, height: `${props.gameHeight}px`, backgroundImage: `url('/assets/bg-shop.png')`}">
      <div class="flex justify-center">

        <!-- Player 1 -->
        <PlayerShopCard :player="players[0]"></PlayerShopCard>
        
        <!-- Score -->
        <div class="flex justify-center">
          <h1 v-if="players[0]" class="text-8xl space-x-4 font-black">{{ players[0].wins }}</h1>
          <h1 class="text-8xl space-x-4 font-black mx-6">:</h1>
          <h1 v-if="players[1]" class="text-8xl space-x-4 font-black">{{ players[1].wins }}</h1>
        </div>

        <!-- Player 2 -->
        <PlayerShopCard :player="players[1]" side="r"></PlayerShopCard>

      </div>

      <!-- Menu and Game buttons -->
      <div class="flex justify-around w-full mt-8">
        <router-link to="/" class="flex items-center justify-center w-80 h-14 bg-gray-400 hover:bg-gray-500 border-2 border-gray-600 rounded-lg font-bold text-2xl ml-10 cursor-pointer">MAIN MENU</router-link>
        <router-link to="/game" class="flex items-center justify-center w-80 h-14 bg-green-500 hover:bg-green-600 border-2 border-green-700 rounded-lg font-bold text-2xl mr-10 cursor-pointer">NEXT ROUND</router-link>
      </div>
      
    </div>
    
</template>