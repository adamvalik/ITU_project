<!--
  File: RenderingScreen.vue
  Author: Marek Effenberger (xeffen00)
-->
<template>
  <div v-if="visible" class="loading-popup">
    <!-- Loading wheels - images which rotate, indicating that the map is rendering -->
  <div class="loading-container">
      <img src="/assets/loading_wheel.png" alt="Loading" class="loading-wheel large-wheel" />
      <img src="/assets/loading_wheel.png" alt="Loading" class="loading-wheel medium-wheel" />
      <img src="/assets/loading_wheel.png" alt="Loading" class="loading-wheel small-wheel" />
      <p class="loading-message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      default: 'Loading...'
    }
  }
};
</script>

<!--//Styles for the loading popup (b4 tailwind usage, dont want to mess with it)-->
<!--//The wheeling images are rotating, indicating that the map is rendering and their positions-->
<!--//are relative to each other.-->
<style scoped>

.loading-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-container {
  background: #01fd9b;
  padding: 40px;
  border-radius: 15px;
  border: 5px solid #000000;
  text-align: left;
  position: relative;
  width: 220px;
  height: 100px;
}

.loading-wheel {
  position: absolute;
  animation: spin 1s linear infinite;
}

.large-wheel {
  width: 50px;
  height: 50px;
  top: 5px;
  left: 70%;
  transform: translateX(-50%);
  animation-duration: 1s;
  z-index: 2;
}

.medium-wheel {
  width: 40px;
  height: 40px;
  top: 38px;
  left: 65%;
  transform: translateX(-50%);
  animation-duration: 1.5s;
  z-index: 5;
}

.small-wheel {
  width: 35px;
  height: 35px;
  top: 42px;
  left: 82%;
  transform: translateX(-50%);
  animation-duration: 0.75s;
  z-index: 4;
}

.loading-message {
  font-size: 1.3em;
  font-weight: bold;
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  z-index: 3;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
