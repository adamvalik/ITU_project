<script setup>
import {defineProps} from 'vue';
const props = defineProps({
    svg:{
        type: String
    }
})

</script>
<template>
    <div class="flex items-end justify-end">
      <div v-html="props.svg"></div>
    </div>
</template>

