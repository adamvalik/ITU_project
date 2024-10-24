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
  export default {
    props: {
      isFlipped: {
        type: Boolean,
        default: false,
      }, 
      defaultColor: {
        type: String,
        default: '#06B559',
      }
    },
    data() {
      return {
        currentTankIndex: 0, // Track the current tank type (0-4)
        tanks: [
          "/assets/tank1.svg", // Path to the first tank SVG
          "/assets/tank2.svg", // Path to the second tank SVG
          "/assets/tank3.svg", // Path to the third tank SVG
          "/assets/tank4.svg", // Path to the fourth tank SVG
          "/assets/tank5.svg", // Path to the fifth tank SVG
        ],
        targetColor: this.defaultColor, // Color to change (initially set to red)
        specificColorToChange: this.defaultColor, // The specific color in the SVG that you want to change
        colorOptions: [
        { name: "Green", hex: "#06B559" },
          { name: "Red", hex: "#BF1313" },
          { name: "Blue", hex: "#0D6BBD" },
        ],
        customColor: null, // Custom color picker value
      };
    },
    watch: {
      // Watch for changes in the custom color picker
      customColor(newColor) {
        this.changeColor(newColor); // Apply the color change when the custom color changes
      }
    },
    computed: {
    gradientStyle() {
      return this.customColor
        ? { backgroundColor: this.customColor } // Use selected color
        : { background: `linear-gradient(217deg, rgb(255,0,0), rgb(255,0,0,0) 70%),
                         linear-gradient(127deg, rgb(0,255,0), rgb(0,255,0,0) 70%),
                         linear-gradient(336deg, rgb(0,0,255), rgb(0,0,255,0) 70%)` }; 
    }
  },
    methods: {
      // Swap between tanks
      swapTank(direction) {
        if (direction === "left") {
          this.currentTankIndex =
            this.currentTankIndex === 0
              ? this.tanks.length - 1
              : this.currentTankIndex - 1;
        } else if (direction === "right") {
          this.currentTankIndex =
            this.currentTankIndex === this.tanks.length - 1
              ? 0
              : this.currentTankIndex + 1;
        }

        this.emitSelectedTank(); // Emit the selected tank

        // After swapping the tank, reload the SVG and apply the current color
        this.loadTank();
      },

        // Emit the selected tank
      emitSelectedTank() {
        const selectedTank = this.tanks[this.currentTankIndex];
        this.$emit('tank-selected', selectedTank); // Emit event to parent
      },
  
      // Change the color of the specific part of the SVG
      changeColor(newColor) {
        this.specificColorToChange = this.targetColor; // Update the specific color to be changed
        this.targetColor = newColor; // Update the color to be applied
        this.applyColorChange();
      },

      // Emit the selected color
      emitSelectedColor() {
        if (this.customColor) {
          this.$emit('color-selected', this.customColor); // Emit event to parent
        } else {
          this.$emit('color-selected', this.targetColor); // Emit event to parent
        }
      },
  
      // Load the current tank SVG file
      async loadTank() {
        this.specificColorToChange = '#06B559'
        const response = await fetch(this.tanks[this.currentTankIndex]);
        const svgText = await response.text();
        this.$refs.svgContainer.innerHTML = svgText; // Insert the SVG into the container
        this.applyColorChange(); // Apply the selected color
      },
  
      // Apply the color change to elements that initially have the specific color
      applyColorChange() {
        const elements = this.$refs.svgContainer.querySelectorAll(`[fill="${this.specificColorToChange}"]`);
        elements.forEach((element) => {
          element.setAttribute("fill", this.targetColor); // Change the color only if it matches the specific color
        });
      },
    },
    mounted() {
      this.loadTank(); // Load the first tank when the component is mounted
      this.emitSelectedTank(); 
      this.emitSelectedColor();
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

/* Style for the custom color input */
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
  