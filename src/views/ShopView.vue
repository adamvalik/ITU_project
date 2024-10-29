<script setup>
import {ref} from 'vue';
import PlayerShopCard from '@/components/Shop/PlayerShopCard.vue';

const P1 = ref(null);
const P2 = ref(null);

function goNextRound(){
    P1.value.savePlayer();
    P2.value.savePlayer();
}

</script>
<template>
    <div class="flex flex-col items-center">
    <div class="flex justify-center">
    <PlayerShopCard :player_id="0" ref="P1"></PlayerShopCard>
    <h1 class="text-8xl space-x-4 font-black">2 : 1</h1>
    <PlayerShopCard :player_id="1" ref="P2" side="r"></PlayerShopCard>
    </div>
    <div class="flex justify-between w-full my-10">
        <div class="flex items-center justify-center w-80 h-14 bg-gray-400 rounded-lg font-bold text-2xl ml-10 cursor-pointer">MAIN MENU</div>
        <div class="flex items-center justify-center w-80 h-14 bg-green-500 rounded-lg font-bold text-2xl mr-10 cursor-pointer" @click="goNextRound">NEXT ROUND</div>

    </div>
    </div>
</template>