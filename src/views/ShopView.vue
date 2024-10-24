<script setup>
import PlayerShopCard from '@/components/Shop/PlayerShopCard.vue';
</script>
<template>
    <div class="flex justify-center">
    <PlayerShopCard></PlayerShopCard>
    <h1 class="text-8xl space-x-4 font-black">2 : 1</h1>
    <PlayerShopCard side="r"></PlayerShopCard>
    </div>
</template>