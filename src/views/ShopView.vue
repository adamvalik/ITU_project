<script setup>
import PlayerShopCard from '@/components/Shop/PlayerShopCard.vue';
</script>
<template>
    <div class="flex justify-center">
    <PlayerShopCard :player_id="0"></PlayerShopCard>
    <h1 class="text-8xl space-x-4 font-black">2 : 1</h1>
    <PlayerShopCard :player_id="1" side="r"></PlayerShopCard>
    </div>
</template>