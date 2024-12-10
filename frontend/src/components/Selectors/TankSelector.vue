<!-- File: TankSelector.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <div class="flex flex-col items-center mb-6">
    <div class="flex gap-4 items-center justify-between">
      <svg
        @click="swapTank('left')"
        class="cursor-pointer "
        width="39"
        height="43"
        viewBox="0 0 39 43"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
       <path d="M3 26.7162C-0.999998 24.4068 -1 18.6333 3 16.3239L29.28 1.15112C33.28 -1.15828 38.28 1.72847 38.28 6.34727L38.28 36.6928C38.28 41.3116 33.28 44.1984 29.28 41.889L3 26.7162Z" fill="#EF4446"/>
      </svg>

      <div ref="svgContainer" class="w-64 h-64 mb-4 shadow-xl" :class="{ 'transform -scale-x-100': isFlipped }"></div>

      <svg
        @click="swapTank('right')"
        class="cursor-pointer transform rotate-180"
        width="39"
        height="43"
        viewBox="0 0 39 43"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M3 26.7162C-0.999998 24.4068 -1 18.6333 3 16.3239L29.28 1.15112C33.28 -1.15828 38.28 1.72847 38.28 6.34727L38.28 36.6928C38.28 41.3116 33.28 44.1984 29.28 41.889L3 26.7162Z" fill="#EF4446"/>
      </svg>

    </div>

    <!-- color change buttons -->
    <div class="flex gap-4">
    <button
      v-for="(color, index) in colorOptions"
      :key="index"
      :style="{ backgroundColor: color.hex }"
      @click="changeColor(color.hex)"
      class="w-14 h-14 rounded-3xl hover:border-2 border-sky transition-all"
    ></button>

    <!-- custom color input -->
    <label class="relative w-14 h-14 rounded-3xl cursor-pointer hover:border-2 border-sky transition-all">
      <input v-model="customColor" type="color" class="absolute opacity-0 ">
      <div
        class="absolute inset-0 rounded-3xl flex items-center justify-center text-l font-bold"
        :style="gradientStyle"
      >
        <span class="text-white">+</span>
      </div>
    </label>
   </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    isFlipped: {
      type: Boolean,
      default: false,
    },
    defaultColor: {
      type: String,
      default: '#123456',
    },
    defaultTankType: {
      type: Number,
      default: 0,
    }
  },
  mounted() {
    this.tankType = this.defaultTankType;
    // if defaultColor is not one of the colorOptions, set customColor to defaultColor
    if (!this.colorOptions.some((color) => color.hex === this.defaultColor)) {
      this.customColor = this.defaultColor;
    }
    this.changeColor(this.defaultColor);
    this.emitSelectedTank();
    this.emitSelectedColor();
  },
  data() {
    return {
      tankType: 0,
      selectedColor: this.defaultColor,
      colorOptions: [
        { hex: "#06B559" },
        { hex: "#0D6BBD" },
        { hex: "#BF1313" },
      ],
      customColor: null,
    };
  },
  watch: {
    customColor(newColor) {
      this.changeColor(newColor);
    }
  },
  computed: {
    gradientStyle() {
      return this.customColor
        ? { backgroundColor: this.customColor }
        : { background: `linear-gradient(217deg, rgb(255,0,0), rgb(255,0,0,0) 70%),
                        linear-gradient(127deg, rgb(0,255,0), rgb(0,255,0,0) 70%),
                        linear-gradient(336deg, rgb(0,0,255), rgb(0,0,255,0) 70%)` };
    }
  },
  methods: {
    swapTank(direction) {
      if (direction === "left") {
        this.tankType = (this.tankType + 4) % 5;
      } else if (direction === "right") {
        this.tankType = (this.tankType + 1) % 5;
      }

      this.emitSelectedTank();
      this.loadTank();
    },

    changeColor(newColor) {
      this.color = newColor;

      this.emitSelectedColor();
      this.loadTank();
    },

    async loadTank() {
      try {
        const response = await axios.get(`http://localhost:8000/selector/${this.tankType}`);
        this.$refs.svgContainer.innerHTML = response.data;

        await this.$nextTick();
        // apply color to tank
        const elements = this.$refs.svgContainer.querySelectorAll(`[fill="#123456"]`);
        elements.forEach((element) => {
          element.setAttribute("fill", this.color);
        });
      } catch (error) {
        console.error(error);
      }
    },

    emitSelectedTank() {
      this.$emit('tank-selected', this.tankType);
    },
    emitSelectedColor() {
      this.$emit('color-selected', this.color);
    },
  },
};
</script>

<style scoped>
input[type="color"] {
  -webkit-appearance: none;
  appearance: none;
  border: none;
  cursor: pointer;
}

input[type="color"]::-webkit-color-swatch-wrapper {
  padding: 0;
}

input[type="color"]::-webkit-color-swatch {
  border: none;
}

.border-sky {
  border-color: #D5EFF4;
}
</style>
