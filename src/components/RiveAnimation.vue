<template>
  <div>
    <canvas ref="riveCanvas" :width="width" :height="height"></canvas>
    <!-- Buttons to trigger animations -->
    <button @click="triggerLeftClick" class="left-button">Left Click</button>
    <button @click="triggerRightClick" class="right-button">Right Click</button>
  </div>
</template>

<script>
import { Rive } from '@rive-app/canvas'; // Correctly import Rive

export default {
  name: 'RiveAnimation',
  props: {
    src: {
      type: String,
      required: true,
    },
    width: {
      type: Number,
      default: 800,
    },
    height: {
      type: Number,
      default: 600,
    },
    stateMachineName: {
      type: String,
      default: 'State Machine 1', // Replace this with the actual name of your state machine
    },
    autoplay: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      riveInstance: null,
      leftClickInput: null,
      rightClickInput: null,
    };
  },
  mounted() {
    this.initRiveAnimation();
  },
  methods: {
    initRiveAnimation() {
      // Initialize the Rive instance with error handling
      this.riveInstance = new Rive({
        src: this.src,
        canvas: this.$refs.riveCanvas,
        stateMachines: this.stateMachineName,
        autoplay: this.autoplay,
        onLoad: () => {
          // Get the state machine inputs (triggers)
          const stateMachine = this.riveInstance.stateMachineInputs(this.stateMachineName);

          // Find the triggers (inputs) by name
          this.leftClickInput = stateMachine.find((input) => input.name === 'leftClicked');
          this.rightClickInput = stateMachine.find((input) => input.name === 'rightClicked');
        },
        onError: (error) => {
          console.error('Error loading Rive animation:', error); // Log any errors
        }
      });
    },

    // Trigger the left click animation
    triggerLeftClick() {
      if (this.leftClickInput) {
        this.leftClickInput.fire();
      }
    },
    // Trigger the right click animation
    triggerRightClick() {
      if (this.rightClickInput) {
        this.rightClickInput.fire();
      }
    },
  },
  beforeUnmount() {
    if (this.riveInstance) {
      this.riveInstance.cleanup();
    }
  },
};
</script>

<style scoped>
/* Basic styling for buttons */
.left-button,
.right-button {
  margin: 10px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.left-button:hover,
.right-button:hover {
  background-color: #0056b3;
}
</style>
