<script setup>
import {ref, defineProps, defineEmits} from 'vue';
import WeaponDetail from './WeaponDetail.vue';
const props = defineProps({
    image : {
        type: String,
        default: ""
    },
    price : {
        type: Number,
        default: 0
    },
    quantity : {
        type: Number,
        default: 0
    },
    name:{
        type: String,
        default : "Weapon name"
    },
    cash:{
        type: Number,
        default : 0
    }
})

const quantity = ref(props.quantity);


const emit = defineEmits(['updateCash']); // Define custom event

function buyItem() {
  if(props.price > props.cash){
    console.log("nelze", props.cash);
    emit('updateCash', props.price, props.name, quantity.value);
    return;
  }
  quantity.value += 1; // Example logic to decrease quantity
 
  emit('updateCash', props.price, props.name, quantity.value);
}
</script>
<template>
    <div class="flex flex-col justify-center items-center">
    <div class="bg-gray-300 rounded-lg p-4 text-center shadow-md w-32">
      <!-- Item icon and quantity -->
      <div class="relative bg-gray-100 rounded-md p-2">
        <!-- Quantity in upper-left corner -->
        <div class="absolute top-0 left-0 bg-gray-400 text-black font-black rounded-full w-10 h-10 flex items-center justify-center shadow-md -translate-x-2 -translate-y-2">
          {{ quantity }}
        </div>
        <img class="w-20 h-20 mx-auto" :src="image" alt="Item" />
        <div class="relative group">
  <!-- The hover trigger div (the "?" button) -->
  <div class="absolute bottom-0 right-0 bg-gray-100 hover:bg-gray-400 text-black font-black rounded-full w-8 h-8 flex items-center justify-center translate-x-1 translate-y-1 cursor-pointer group">
    ?
  </div>

  <!-- The div that appears when hovering on the "?" -->
  <div class="absolute bottom-10 -right-8 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none group-hover:pointer-events-auto">
    <WeaponDetail :name="props.name"/> 
  </div>
</div>
      </div>

      <!-- Price -->
      <div class="bg-yellow-400 text-black font-bold p-1 mt-3 rounded-md">
        {{ props.price }} $
      </div>

      <!-- Buy Button -->
    </div>
      <button 
        class="bg-green-500 text-white font-bold py-2 w-full rounded-md mt-3 hover:bg-green-600"
        @click="buyItem"
      >
        BUY
      </button>
    
  </div>
</template>