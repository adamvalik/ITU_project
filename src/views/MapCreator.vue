<script setup>
import ThemeSelector from '../components/mapcreatorcomponents/ThemeSelector.vue';
import OperationSelector from '../components/mapcreatorcomponents/OperationSelector.vue';
import RenderingScreen from "@/components/mapcreatorcomponents/RenderingScreen.vue";

import { ref, onMounted } from 'vue';
import axios from 'axios';

const activeTheme = ref('forest'); // Default theme
const cursorType = ref(''); // Default cursor type
const eraserActive = ref(false); // Track if eraser is being used
const isLoading = ref(false); // Add this reactive state to track loading
const brushSize = 25; // Eraser brush size

const updateTheme = (theme) => {
  activeTheme.value = theme;

  // Clear the canvas before recoloring
  ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);

  // Recolor all stored areas with the new theme
  storedGreenCoordinates.value.forEach(greenCoordinates => {
    updateMapArea(greenCoordinates);
  });
};

const updateCursor = (type) => {
  cursorType.value = type;
  let cursorUrl;
  if (type === 'eraser') {
    eraserActive.value = true; // Activate eraser
  } else {
    eraserActive.value = false; // Deactivate eraser
  }

  switch (type) {
    case 'pen':
      cursorUrl = '/assets/pen_icon_png.png';
      break;
    case 'eraser':
      cursorUrl = '/assets/eraser_mouse_png.png'; // We’ll hide the default cursor
      break;
    case 'obstruction':
    default:
      cursorUrl = 'auto';
  }
  document.querySelector('.custom-cursor').style.cursor = `url(${cursorUrl}), auto`;
};

const canvasRef = ref(null);
let ctx = null;
let drawing = false;
let drawnPath = [];
const storedGreenCoordinates = ref([]);  // Array to store all green areas

const startDrawing = (event) => {
  drawing = true;
  drawnPath = [];  // Clear previous path
  ctx.beginPath();  // Start a new path
  draw(event);
};

const stopDrawing = async () => {
  if (!drawing) return;
  drawing = false;
  ctx.beginPath();
  if (drawnPath.length > 0 && cursorType.value === 'pen') {
    await sendToBackend(drawnPath);  // Send path to backend after drawing
  }
};

const draw = (event) => {
  if (!drawing || cursorType.value === '') return;

  const rect = canvasRef.value.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  // Store the current point in the path
  drawnPath.push([x, y]);

  ctx.lineWidth = cursorType.value === 'eraser' ? brushSize : 2;
  ctx.lineCap = 'round';
  ctx.strokeStyle = cursorType.value === 'eraser' ? '#f5f5dc' : '#000000';

  if (cursorType.value === 'eraser') {
    ctx.clearRect(x - brushSize / 2, y - brushSize / 2, brushSize, brushSize);
  } else {
    ctx.lineTo(x, y);
    ctx.stroke();
    // ctx.beginPath();
    // ctx.moveTo(x, y);
  }
};

const sendToBackend = async (path) => {
  isLoading.value = true;  // Show the loading popup
  const canvas = canvasRef.value;
  const bottomY = canvas.height;

  try {
    const response = await axios.post('http://localhost:8000/process-path', {
      path,
      bottomY
    });
    const result = response.data;

    // Store the green coordinates
    storedGreenCoordinates.value.push(result.greenCoordinates);

    // Update the map with the new area
    updateMapArea(result.greenCoordinates);
  } catch (error) {
    console.error('Error sending path to backend:', error);
  } finally {
    isLoading.value = false;  // Hide the loading popup
  }
};

const updateMapArea = (greenCoordinates) => {
  ctx.beginPath();

  // Set color based on active theme
  let activeThemer = activeTheme.value;
  if (activeThemer === 'forest') {
    ctx.strokeStyle = '#2e7d32'; // Green color
  } else if (activeThemer === 'beach') {
    ctx.strokeStyle = '#c68e17'; // Yellow color
  } else {
    ctx.strokeStyle = '#02f1fb'; // Blue color
  }
  ctx.lineWidth = 2;

  greenCoordinates.forEach(([x, y]) => {
    ctx.lineTo(x, y);
  });

  ctx.stroke();
};

const updateBrushCircle = (event) => {
  if (!eraserActive.value) return;

  const brushCircle = document.querySelector('.brush-circle');
  brushCircle.style.display = 'block';
  brushCircle.style.left = `${event.clientX - brushSize / 2}px`;
  brushCircle.style.top = `${event.clientY - brushSize / 2}px`;
};

const hideBrushCircle = () => {
  document.querySelector('.brush-circle').style.display = 'none';
};

onMounted(() => {
  const canvas = canvasRef.value;
  ctx = canvas.getContext('2d');
  canvas.addEventListener('mousedown', startDrawing);
  canvas.addEventListener('mouseup', stopDrawing);
  canvas.addEventListener('mousemove', (event) => {
    draw(event);
    updateBrushCircle(event); // Update circle position while moving
  });
  canvas.addEventListener('mouseleave', () => {
    stopDrawing();
    hideBrushCircle(); // Hide circle when mouse leaves canvas
  });
});

</script>

<template>
  <div class="min-h-screen bg-beige flex flex-col justify-center items-center relative custom-cursor">
    <div class="canvas-container">
      <ThemeSelector :activeTheme="activeTheme" @theme-change="updateTheme" class="theme-selector"/>
      <OperationSelector :activeTheme="activeTheme" @cursor-change="updateCursor" class="operation-selector"/>
      <canvas ref="canvasRef" width="900" height="500" class="border-2 border-black mt-4"></canvas>
    </div>
    <div class="brush-circle"></div>
    <RenderingScreen :visible="isLoading" message="Rendering..." />
  </div>
</template>

<style scoped>

.extra-margin {
  margin-top: 10px; /* Adjust the value as needed */
}

.bg-beige {
  background-color: #f5f5dc; /* Beige color */
}

.canvas-container {
  position: relative;
  display: inline-block;
  margin-top: 50px; /* Adjust the value as needed */

}

.theme-selector {
  position: absolute;
  top: -90px; /* Adjust as needed */
  left: 50%;
  transform: translateX(-50%);
}

.operation-selector {
  position: absolute;
  top: 40%;
  right: -140px; /* Adjust as needed */
  transform: translateY(-50%);
}
.brush-circle {
  position: absolute;
  width: 25px; /* Match the brush size */
  height: 25px;
  border-radius: 50%;
  background-color: rgba(41, 220, 70, 0.3); /* Red color with transparency */
  box-shadow: 0 0 10px rgba(78, 238, 61, 0.7); /* Glowing red shadow */
  pointer-events: none; /* Ensure the circle doesn’t interfere with events */
  display: none; /* Hidden until the eraser is active */
}
</style>
