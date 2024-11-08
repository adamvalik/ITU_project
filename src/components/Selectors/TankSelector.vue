<template>
  <div class="flex flex-col items-center bg-gray-100">
    <div class="flex gap-4 items-center justify-between">
      <button @click="swapTank('left')" class="h-10 w-10 bg-red-500 rounded-xl hover:border-2 border-gray-100 transition-all"></button>

      <div ref="svgContainer" class="tank-container w-64 h-64 mb-4 shadow-xl" :class="{ 'flip-x': isFlipped }"></div>

      <button @click="swapTank('right')" class="h-10 w-10 bg-red-500 rounded-xl hover:border-2 border-gray-100 transition-all"></button>
    </div>

    <!-- Color Change Buttons -->
    <div class="flex gap-4">
    <!-- Color Buttons -->
    <button
      v-for="(color, index) in colorOptions"
      :key="index"
      :style="{ backgroundColor: color.hex }"
      @click="changeColor(color.hex)"
      class="w-14 h-14 rounded-3xl hover:border-2 border-gray-100 transition-all"
    ></button>

    <!-- Custom Color Input -->
    <label class="relative w-14 h-14 rounded-3xl cursor-pointer hover:border-2 border-gray-100 transition-all">
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
      console.log("loadTank: this.selectedColor", this.selectedColor, ", this.tankType", this.tankType);
      try {
        const response = await axios.get(`http://localhost:8000/selector/${this.tankType}`);

        this.$refs.svgContainer.innerHTML = response.data;

        // wait until the next DOM update cycle
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
.tank-container {
  background-color: white;
  overflow: hidden;
}

.flip-x {
  transform: scaleX(-1);
}

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
</style>
