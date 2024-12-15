<!-- File: PlayerShopCard.vue -->
<!-- Author: Dominik Horut (xhorut01) -->

<script setup>

import {defineProps, ref, watch} from 'vue';
import apiClient from '@/api';
import WeaponShop from './WeaponShop.vue';
import SkillShop from './SkillShop.vue';
import TankImage from './TankImage.vue';

const props = defineProps({

  player:{
    type: Object,
  },

  side:{
    type: String,
    default: "l"
  }
});

// players tank image
const svg = ref(null);

const player = ref();

// get players tank image
const fetchTank = async () => {
  try {
    const response = await apiClient.get(`/players/${props.player.id}/tank`);
    svg.value = response.data; 

  } catch (error) {
    console.error('Error fetching tank image:', error);
  }
}

// get player by his id
const fetchPlayer = async () => {
  try {
    const response = await apiClient.get(`/players/${props.player.id}`);
    player.value = response.data; 

  } catch (error) {
    console.error('Error fetching player:', error);
  }
}

// buy certain type of ammunition
const buyAmmo = async (data) => {
  try {
    await apiClient.post(`/player/buyAmmo`, {player: props.player.id, ammo_type: data.ammo_type, price: data.price});

    // update player after purchase
    await fetchPlayer();

  } catch (error) {
    console.error('Error buying ammo:', error);
  }
}

// upgrade certain skill
const upgradeSkill = async (data) => {
  try {
    await apiClient.post(`/player/upgradeSkill`, {player: props.player.id, skill: data.name, value: 0});

    // update player after purchase
    await fetchPlayer();

  } catch (error) {
    console.error('Error upgrading skill:', error);
  }
}

// downgrade certain skill
const downgradeSkill = async (data) => {
  try {
    await apiClient.post(`/player/downgradeSkill`, {player: props.player.id, skill: data.name, value: 0});

    // update player after purchase
    await fetchPlayer();

  } catch (error) {
    console.error('Error upgrading skill:', error);
  }
}

// get player data after props are passed
watch(() => props.player, (fetchedPlayer) => {
  if (fetchedPlayer && fetchedPlayer.id) {
    fetchPlayer();
    fetchTank();
  }
});

</script>

<template>
  
  <div class="flex flex-col justify-center items-center mt-6">

    <!-- Player is displayed on left side -->
    <div v-if="props.side == 'l'" class="flex justify-between">
      <div class="text-6xl font-black self-center">
        {{ player ? player.name : 'Loading...' }}
      </div>
      <TankImage :svg="svg" class="self-end h-24"></TankImage>
    </div>

    <!-- Player is displayed on right side -->
    <div v-else class="flex justify-between items-center">
      <TankImage :svg="svg" class="self-start flip h-24"></TankImage>    
      <div class="text-6xl font-black ml-2">
        {{ player ? player.name : 'Loading...' }}
      </div>
    </div>

    <!-- Parts of shop -->
    <div v-if="player">

      <WeaponShop :weapon1="player.ammunitionCount[0]" :weapon2="player.ammunitionCount[1]" :weapon3="player.ammunitionCount[2]" :cash="player.money" @buy="buyAmmo"></WeaponShop>
                
      <SkillShop  :armor="player.armorSkill" :power="player.powerSkill" :speed="player.speedSkill" :skillPoints="player.skillPoints" @upgrade="upgradeSkill" @downgrade="downgradeSkill"></SkillShop>
                
    </div>
    <div v-else>Loading player data...</div>

  </div>
  
</template>

<style scoped>
 
/* flipped image of player on right side */
.flip {
  transform: scaleX(-1);
  direction: rtl; 
}

</style>