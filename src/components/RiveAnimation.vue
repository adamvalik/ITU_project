<!-- RiveAnimation.vue -->
<template>
  <canvas ref="riveCanvas" :width="width" :height="height"></canvas>
</template>

<script>
import { Rive } from '@rive-app/canvas';

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
    autoplay: {
      type: Boolean,
      default: true,
    },
  },
  mounted() {
    this.initRiveAnimation();
  },
  methods: {
    initRiveAnimation() {
      this.riveInstance = new Rive({
        src: this.src,
        canvas: this.$refs.riveCanvas,
        autoplay: this.autoplay,
      });
    },
  },
  beforeUnmount() {
    if (this.riveInstance) {
      this.riveInstance.cleanup();
    }
  },
};
</script>
