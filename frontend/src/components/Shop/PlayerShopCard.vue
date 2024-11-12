<script setup>
import {defineProps, ref, onMounted, defineExpose} from 'vue';
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
    const response = await axios.get(`http://localhost:8000/players/${playerId}`);
    player.value = response.data; // Set player data
  } catch (error) {
    console.error('Error fetching player data:', error);
  }
}

async function fetchTankData(playerId){
      try {
        const response = await axios.get(`http://localhost:8000/players/${playerId}/tank`);
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

function updatePoints(usedPoints, name) {
  if(name === "Armor"){
    player.value.armorSkill -= usedPoints;
    
    
  } else if(name === "Power"){
    player.value.powerSkill -= usedPoints;
    
  } else if(name === "Speed"){
    player.value.speedSkill -= usedPoints;
  
  }
  player.value.skillPoints += usedPoints;
}

function updateCash(cash, name, quantity) {
  player.value.money = cash;
  if(name === "Striker"){
    player.value.ammunitionCount[0] = quantity;
 
  } else if(name === "Devastator"){
    player.value.ammunitionCount[1] = quantity;
    
  } else if(name === "Phantom"){
    player.value.ammunitionCount[2] = quantity;
    
  }
}

defineExpose({
  savePlayer
});

function savePlayer() {
  console.log("Money",player.value.money);
  console.log("W1:",player.value.weapon1);
  console.log("W2:",player.value.weapon2);
  console.log("W3:",player.value.weapon3);
  console.log("Armor:",player.value.armorSkill);
  console.log("Power:",player.value.powerSkill);
  console.log("Speed:",player.value.speedSkill);
  console.log("Free Pts:",player.value.skillPoints);


}

</script>
<template>
    
        <div class="flex flex-col justify-center items-center mt-6">
          <div v-if="props.side == 'l'" class="flex justify-between">
            <div class="text-6xl font-black self-center">
              {{ player ? player.name : 'Loading...' }}
            </div>
            <TankImage :svg="svg" class="self-end h-24"></TankImage>
          </div>
          <div v-else class="flex justify-between items-center">
            <TankImage :svg="svg" class="self-start flip h-24"></TankImage>    
            <div class="text-6xl font-black ">
              {{ player ? player.name : 'Loading...' }}
            </div>
          </div>

            <div v-if="player">
                <WeaponShop :weapon="player.weapon" :weapon1="player.ammunitionCount[0]" :weapon2="player.ammunitionCount[1]" :weapon3="player.ammunitionCount[2]" :cash="player.money" @updateCash="updateCash"></WeaponShop>
                <SkillShop  :armor="player.armorSkill" :power="player.powerSkill" :speed="player.speedSkill" :skillPoints="player.skillPoints" @updatePoints="updatePoints"></SkillShop>
                
            </div>
            <div @click="savePlayer" v-else>Loading player data...</div>
        </div>
</template>

<style scoped>
.flip {
  transform: scaleX(-1);
  direction: rtl; 
}
</style>