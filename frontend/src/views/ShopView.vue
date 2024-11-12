<script setup>
import {ref, defineProps} from 'vue';
import PlayerShopCard from '@/components/Shop/PlayerShopCard.vue';

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

const P1 = ref(null);
const P2 = ref(null);

function goNextRound(){
    P1.value.savePlayer();
    P2.value.savePlayer();
}

</script>
<template>
    
    <div class="flex flex-col items-center bg-cover bg-center" :style="{ width: `${props.gameWidth}px`, height: `${props.gameHeight}px`, backgroundImage: `url('/assets/bg-shop.png')`}">
    <div class="flex justify-center">
    <PlayerShopCard :player_id="1" ref="P1"></PlayerShopCard>
    <h1 class="text-8xl space-x-4 font-black">0:1</h1>
    <PlayerShopCard :player_id="2" ref="P2" side="r"></PlayerShopCard>
    </div>
    <div class="flex justify-around w-full mt-8">
        <router-link to="/" class="flex items-center justify-center w-80 h-14 bg-gray-400 hover:bg-gray-500 border-2 border-gray-600 rounded-lg font-bold text-2xl ml-10 cursor-pointer">MAIN MENU</router-link>
        <router-link to="/game" class="flex items-center justify-center w-80 h-14 bg-green-500 hover:bg-green-600 border-2 border-green-700 rounded-lg font-bold text-2xl mr-10 cursor-pointer" @click="goNextRound">NEXT ROUND</router-link>

    </div>
    </div>
    
</template>