<script setup>
import {ref} from 'vue'
import SkillShopItem from './SkillShopItem.vue';
const skillPoints = ref(3)

function updatePoints(usedPoints) {
  skillPoints.value += usedPoints;
}
</script>
<template>
    <div class="flex flex-col">
        <div class="text-3xl font-black flex justify-center items-center" >
            FREE SKILL POINTS: <span class="text-5xl ml-4 " > {{skillPoints}} </span>
        </div>
        <div>
        <SkillShopItem name="Armor" :image="require('@/assets/armor-icon.png')" :level="3" :availablePoints="skillPoints" class="m-2" @updatePoints="updatePoints"></SkillShopItem>
        <SkillShopItem name="Power" :image="require('@/assets/power-icon.png')" :level="2" :availablePoints="skillPoints" class="m-2" @updatePoints="updatePoints"></SkillShopItem>
        <SkillShopItem name="Speed" :image="require('@/assets/speed-icon.png')" :level="1" :availablePoints="skillPoints" class="m-2" @updatePoints="updatePoints"></SkillShopItem>
        </div>
</div>
</template>