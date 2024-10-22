<template>
<div>
  <div class="flex flex-col items-center">
    <!-- Rive Animation Canvas -->
    <canvas ref="riveCanvas" class="mb-8"></canvas>

    <!-- Tank Type Swapping Buttons -->
    <div class="button-container mb-6">
      <button @click="swapLeft" class="px-4 py-2 bg-gray-500 text-white rounded-lg mr-4">Swap Left</button>
      <button @click="swapRight" class="px-4 py-2 bg-gray-500 text-white rounded-lg">Swap Right</button>
    </div>

    <!-- Tank Color Swapping Buttons -->
    <div class="button-container mb-6">
      <button @click="setColorRed" class="px-4 py-4 bg-red-500 rounded-lg mr-4"></button>
      <button @click="setColorGreen" class="px-4 py-4 bg-green-500 rounded-lg mr-4"></button>
      <button @click="setColorBlue" class="px-4 py-4 bg-blue-500 rounded-lg"></button>
      <button @click="setColorWhite" class="px-4 py-4 bg-gray-300 rounded-lg"></button>
      <button @click="setColorBlack" class="px-4 py-4 bg-gray-800 rounded-lg"></button>
      <button @click="setColorOrange" class="px-4 py-4 bg-orange-500 rounded-lg"></button>
      <button @click="setColorYellow" class="px-4 py-4 bg-yellow-500 rounded-lg"></button>
      <button @click="setColorPink" class="px-4 py-4 bg-pink-500 rounded-lg"></button>
      <button @click="setColorPurple" class="px-4 py-4 bg-purple-500 rounded-lg"></button>
    </div>
  </div>
</div>
</template>

<script>
import { Rive } from '@rive-app/canvas';

export default {
  data() {
    return {
      riveInstance: null,  // Store the Rive instance
      swapRightTrigger: null,
      swapLeftTrigger: null,
      colorRedTrigger: null,
      colorGreenTrigger: null,
      colorBlueTrigger: null,
      colorWhiteTrigger: null,
      colorBlackTrigger: null,
      colorOrangeTrigger: null,
      colorYellowTrigger: null,
      colorPinkTrigger: null,
      colorPurpleTrigger: null,
    };
  },
  mounted() {
    // Initialize the Rive animation
    this.riveInstance = new Rive({
      src: '/assets/tankySmall.riv', // Your Rive file
      canvas: this.$refs.riveCanvas,     // Attach to the canvas in the template
      stateMachines: 'SM1', // State machine name in Rive
      autoplay: false,                    // Automatically play the animation
      onLoad: (rive) => {
        console.log('Rive animation loaded successfully');

        // Get the state machine inputs when the Rive file is loaded
        const inputs = rive.stateMachineInputs('SM1');
        
        // Map the triggers to variables for later use
        // this.swapRightTrigger = inputs.find(input => input.name === 'rightClicked');
        // this.swapLeftTrigger = inputs.find(input => input.name === 'leftClicked');
        this.colorRedTrigger = inputs.find(input => input.name === 'red');
        this.colorGreenTrigger = inputs.find(input => input.name === 'green');
        this.colorBlueTrigger = inputs.find(input => input.name === 'blue');
        this.colorWhiteTrigger = inputs.find(input => input.name === 'white');
        this.colorBlackTrigger = inputs.find(input => input.name === 'black');
        this.colorOrangeTrigger = inputs.find(input => input.name === 'orange');
        this.colorYellowTrigger = inputs.find(input => input.name === 'yellow');
        this.colorPinkTrigger = inputs.find(input => input.name === 'pink');
        this.colorPurpleTrigger = inputs.find(input => input.name === 'purple');
      },
    });
  },
  onError: (error) => {
    console.error('Failed to load Rive animation:', error);
  },
  methods: {
    // Trigger the swap left action
    // swapLeft() {
    //   if (this.swapLeftTrigger) {
    //     this.swapLeftTrigger.fire();  // Fire the swapLeft trigger
    //   }
    // },
    // // Trigger the swap right action
    // swapRight() {
    //   if (this.swapRightTrigger) {
    //     this.swapRightTrigger.fire();  // Fire the swapRight trigger
    //   }
    // },
    // Trigger the red color change
    setColorRed() {
      if (this.colorRedTrigger) {
        this.colorRedTrigger.fire();  // Fire the colorRed trigger
      }
    },
    // Trigger the green color change
    setColorGreen() {
      if (this.colorGreenTrigger) {
        this.colorGreenTrigger.fire();  // Fire the colorGreen trigger
      }
    },
    // Trigger the blue color change
    setColorBlue() {
      if (this.colorBlueTrigger) {
        this.colorBlueTrigger.fire();  // Fire the colorBlue trigger
      }
    },
    // Trigger the white color change
    setColorWhite() {
      if (this.colorWhiteTrigger) {
        this.colorWhiteTrigger.fire();  // Fire the colorWhite trigger
      }
    },
    // Trigger the black color change
    setColorBlack() {
      if (this.colorBlackTrigger) {
        this.colorBlackTrigger.fire();  // Fire the colorBlack trigger
      }
    },
    // Trigger the orange color change
    setColorOrange() {
      if (this.colorOrangeTrigger) {
        this.colorOrangeTrigger.fire();  // Fire the colorOrange trigger
      }
    },
    // Trigger the yellow color change
    setColorYellow() {
      if (this.colorYellowTrigger) {
        this.colorYellowTrigger.fire();  // Fire the colorYellow trigger
      }
    },
    // Trigger the pink color change
    setColorPink() {
      if (this.colorPinkTrigger) {
        this.colorPinkTrigger.fire();  // Fire the colorPink trigger
      }
    },
    // Trigger the purple color change
    setColorPurple() {
      if (this.colorPurpleTrigger) {
        this.colorPurpleTrigger.fire();  // Fire the colorPurple trigger
      }
    },
  },
};
</script>

<style scoped>
.button-container {
  display: flex;
  justify-content: center;
}

canvas {
  width: 250px;
  height: 250px;
}
</style>
