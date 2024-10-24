<script setup>
import {defineProps} from 'vue';
import WeaponShop from './WeaponShop.vue';
import SkillShop from './SkillShop.vue';

const props = defineProps({
  side:{
    type: String,
    default: "l"
  },

  playerName:{
    type: String,
    default: "PLAYER"
  }
});



</script>
<template>
    
        <div class="flex flex-col justify-center items-center">
            <div v-if="props.side == 'l'" class="flex justify-between items-center mb-14">
                <div class="text-6xl font-black">
                    {{ props.playerName }}
                </div>
                <img src="../../assets/player1tank.png">
            </div>
            <div v-else class="flex justify-center items-center mb-14">
                <img src="../../assets/player2tank.png">
                <div class="text-6xl font-black">
                    {{ props.playerName }}
                </div>
            
            </div>
            <div>
                <WeaponShop class="mb-14"></WeaponShop>
                <SkillShop></SkillShop>
    
            </div>
        </div>
</template>