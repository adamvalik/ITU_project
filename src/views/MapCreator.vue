<script setup>
import ThemeSelector from '../components/mapcreatorcomponents/ThemeSelector.vue';
import OperationSelector from '../components/mapcreatorcomponents/OperationSelector.vue';
import { ref, onMounted } from 'vue';

const activeTheme = ref('forest'); // Default theme
const cursorType = ref(''); // Default cursor type
const eraserActive = ref(false); // Track if eraser is being used
const brushSize = 25; // Eraser brush size

const updateTheme = (theme) => {
  activeTheme.value = theme;
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

const startDrawing = (event) => {
  drawing = true;
  draw(event);
};

const stopDrawing = () => {
  drawing = false;
  ctx.beginPath();
};

const draw = (event) => {
  if (!drawing) return;

  ctx.lineWidth = cursorType.value === 'eraser' ? brushSize : 2;
  ctx.lineCap = 'round';
  ctx.strokeStyle = cursorType.value === 'eraser' ? '#f5f5dc' : '#000000';

  ctx.lineTo(event.clientX - canvasRef.value.offsetLeft, event.clientY - canvasRef.value.offsetTop);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(event.clientX - canvasRef.value.offsetLeft, event.clientY - canvasRef.value.offsetTop);
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
    <ThemeSelector :activeTheme="activeTheme" @theme-change="updateTheme"
                   class="absolute top-0 left-1/2 transform -translate-x-1/2 mt-4"/>
    <OperationSelector :activeTheme="activeTheme" @cursor-change="updateCursor" class="absolute top-1/4 right-0 mr-4"/>
    <canvas ref="canvasRef" width="900" height="500" class="border-2 border-black mt-4"></canvas>
    <!-- Glowing eraser brush circle -->
    <div class="brush-circle"></div>
  </div>
</template>

<style scoped>
.bg-beige {
  background-color: #f5f5dc; /* Beige color */
}

.brush-circle {
  position: absolute;
  width: 25px; /* Match the brush size */
  height: 25px;
  border-radius: 50%;
  background-color: rgba(34, 85, 193, 0.3); /* Red color with transparency */
  box-shadow: 0 0 10px rgba(90, 189, 202, 0.7); /* Glowing red shadow */
  pointer-events: none; /* Ensure the circle doesn’t interfere with events */
  display: none; /* Hidden until the eraser is active */
}
</style>
