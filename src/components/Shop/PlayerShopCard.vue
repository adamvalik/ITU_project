<script setup>
import {defineProps, ref, onMounted} from 'vue';
import axios from 'axios';
import WeaponShop from './WeaponShop.vue';
import SkillShop from './SkillShop.vue';
import TankImage from './TankImage.vue';

const props = defineProps({
  player_id:{
    type: Number,
    default: 0
  },
  side:{
    type: String,
    default: "l"
  }
});

// Reactive reference to hold player data
const player = ref(null);
const svg = ref(null)

// Function to fetch player data
async function fetchPlayerData(playerId) {
  try {
    const response = await axios.get(`http://localhost:8000/player/${playerId}`);
    player.value = response.data; // Set player data
  } catch (error) {
    console.error('Error fetching player data:', error);
  }
}

async function fetchTankData(playerId){
      try {
        const response = await axios.get(`http://localhost:8000/player/${playerId}/tank`);
        svg.value = response.data; // Set the SVG data
      } catch (error) {
        console.error('Error fetching tank data:', error);
      }
}

// Lifecycle hook to fetch player data when the component is mounted
onMounted(() => {
   // Change this to the desired player ID
  fetchPlayerData(props.player_id);
  fetchTankData(props.player_id);
});



</script>
<template>
    
        <div class="flex flex-col justify-center items-center">
          <div v-if="props.side == 'l'" class="flex flex-col justify-between h-52 w-full">
            <div class="text-6xl font-black self-center">
              {{ player ? player.name : 'Loading...' }}
            </div>
            <TankImage :svg="svg" class="self-end "></TankImage>
          </div>
          <div v-else class="flex flex-col-reverse justify-between h-52 w-full">
            <TankImage :svg="svg" class="self-start flip"></TankImage>    
            <div class="text-6xl font-black self-center">
              {{ player ? player.name : 'Loading...' }}
            </div>
          </div>

            <div v-if="player">
                <WeaponShop class="mb-14" :weapon="player.weapon" :weapon1="player.weapon1" :weapon2="player.weapon2" :weapon3="player.weapon3" :cash="player.money" ></WeaponShop>
                <SkillShop  :armor="player.armor" :power="player.power" :speed="player.speed" :skillPoints="player.skillPoints"></SkillShop>
                
            </div>
            <div v-else>Loading player data...</div>
        </div>
</template>

<style scoped>
/* CSS to flip the div along the Y-axis */
.flip {
  transform: scaleX(-1);
  /* Optional: If you want to maintain the same direction of text */
  direction: rtl; 
}
</style>