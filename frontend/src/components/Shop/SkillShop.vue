<script setup>
import {defineProps, defineEmits} from 'vue'
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

const emit = defineEmits(['upgrade', 'downgrade']);

const upgradeSkill = (data) => {
  emit('upgrade', {name: data.name});
}

const downgradeSkill = (data) => {
  emit('downgrade', {name: data.name});
}
</script>
<template>
    <div class="flex flex-col">
        <div class="text-3xl font-black flex justify-center items-center" >
            FREE SKILL POINTS: <span class="text-5xl ml-4 " > {{props.skillPoints}} </span>
        </div>
        <div>
        <SkillShopItem name="armor" :image="'/assets/armor-icon.png'" :level="props.armor" :availablePoints="props.skillPoints" class="m-2" @upgrade="upgradeSkill" @downgrade="downgradeSkill"></SkillShopItem>
        <SkillShopItem name="power" :image="'/assets/power-icon.png'" :level="props.power" :availablePoints="props.skillPoints" class="m-2" @upgrade="upgradeSkill" @downgrade="downgradeSkill"></SkillShopItem>
        <SkillShopItem name="speed" :image="'/assets/speed-icon.png'" :level="props.speed" :availablePoints="props.skillPoints" class="m-2" @upgrade="upgradeSkill" @downgrade="downgradeSkill"></SkillShopItem>
        </div>
</div>
</template>
