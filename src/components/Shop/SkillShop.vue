<script setup>
import {ref, defineProps, defineEmits} from 'vue'
import SkillShopItem from './SkillShopItem.vue';
const props = defineProps({
    armor:{
      type: Number,
      default: 0
    },
    power:{
      type: Number,
      default: 0
    },
    speed:{
      type: Number,
      default: 0
    },
    skillPoints:{
      type: Number,
      default: 0
    },
})

const skillPoints = ref(props.skillPoints)
const emit = defineEmits(['updatePoints']);

function updatePoints(usedPoints, name) {
  skillPoints.value += usedPoints;
  emit('updatePoints', usedPoints, name);
}
</script>
<template>
    <div class="flex flex-col">
        <div class="text-3xl font-black flex justify-center items-center" >
            FREE SKILL POINTS: <span class="text-5xl ml-4 " > {{skillPoints}} </span>
        </div>
        <div>
        <SkillShopItem name="Armor" :image="require('@/assets/armor-icon.png')" :level="props.armor" :availablePoints="skillPoints" class="m-2" @updatePoints="updatePoints"></SkillShopItem>
        <SkillShopItem name="Power" :image="require('@/assets/power-icon.png')" :level="props.power" :availablePoints="skillPoints" class="m-2" @updatePoints="updatePoints"></SkillShopItem>
        <SkillShopItem name="Speed" :image="require('@/assets/speed-icon.png')" :level="props.speed" :availablePoints="skillPoints" class="m-2" @updatePoints="updatePoints"></SkillShopItem>
        </div>
</div>
</template>