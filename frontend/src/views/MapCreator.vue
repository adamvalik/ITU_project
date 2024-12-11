<script setup>

import { ref, onMounted, onBeforeUnmount, defineProps } from 'vue';

import {
  erasePath,
  setMapType,
  createMap,
  processPath,
  addNewImage,
  retrieveMap,
  deleteMap,
  addPlayerPosition,
  copyMap,
  retrieveNumOfMaps,
  //retrievePlayerPosition,
} from '@/components/mapcreatorcomponents/BackendOperations.js';

import ThemeSelector from '../components/mapcreatorcomponents/ThemeSelector.vue';
import OperationSelector from '../components/mapcreatorcomponents/OperationSelector.vue';
import SaveMap from '@/components/mapcreatorcomponents/SaveMap.vue';
const showModal = ref(false);
import RenderingScreen from "@/components/mapcreatorcomponents/RenderingScreen.vue";
import { useRouter, useRoute } from 'vue-router';
import playerA from '../../public/assets/player_a.svg';
import playerB from '../../public/assets/player_b.svg';
import back from '../../public/assets/back.svg';

const props = defineProps({
  gameWidth: Number,
  gameHeight: Number,
  scaleFactor: Number,
});

const router = useRouter();

const activeTheme = ref('forest'); // Default theme
const cursorType = ref(''); // Default cursor type
const eraserActive = ref(false); // Track if eraser is being used
const isLoading = ref(false); // Add this reactive state to track loading
const brushSize = 25; // Eraser brush size
const brushColor = ref('#2e7d32'); // Make brushColor reactive
const obstructionIconPath = ref('/assets/tree_icon.svg'); // Default obstruction icon
const route = useRoute();
const showStartPlayingButton = ref(route.query.fromMapSelector === 'true');

const focusedTank = ref(null);
const tank1 = ref(playerA);
const tank2 = ref(playerB);
const backicon = ref(back);
const tank1Dropped = ref(false);
const tank2Dropped = ref(false);

const canvasRef = ref(null);
let ctx = null;
let drawing = false;
let drawnPath = [];
// const storedGreenCoordinates = ref([]);  // Array to store all green areas
// const imageArray = ref([]);  // Array to store all images
// const eraserArray = ref([]);  // Array to store all eraser paths
// const arrayArray = ref([]);  // Array to store all arrays
const mapName = 'map1';  // Default map name

const updateTheme = async (theme) => {
  activeTheme.value = theme;
  if (theme === 'forest') {
    brushColor.value = '#2e7d32';
    obstructionIconPath.value = '/assets/tree_icon.svg';
  } else if (theme === 'beach') {
    brushColor.value = '#c68e17';
    obstructionIconPath.value = '/assets/cactus_icon.svg';
  } else {
    brushColor.value = '#02f1fb';
    obstructionIconPath.value = '/assets/snowman_icon.svg';
  }
  setMapType(mapName, theme);
  // Clear the canvas before recoloring
  ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);

  // Recolor all stored areas with the new theme
  isLoading.value = true;  // Show the loading popup
  try {
    await updateMapArea();
  } catch (error) {
    console.error('Error updating map area:', error);
  } finally {
    isLoading.value = false;  // Hide the loading popup
  }
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
  if (drawnPath.length > 0) {
    if (cursorType.value === 'eraser') {
      await erasePath(mapName, drawnPath);  // Send eraser path to backend after drawing
    } else if (cursorType.value === 'pen') {
      await sendToBackend(drawnPath);  // Send path to backend after drawing
    }
  }
};

const draw = (event) => {
  if (!drawing || cursorType.value === '' || cursorType.value === 'obstruction') return;

  const rect = canvasRef.value.getBoundingClientRect();
  const x = (event.clientX - rect.left)/props.scaleFactor;
  const y = (event.clientY - rect.top)/props.scaleFactor;

  if (x < 0 || y < 0 || x > canvasRef.value.width || y > canvasRef.value.height) {
    return;
  }

  // Store the current point in the path
  drawnPath.push([x, y]);

  ctx.lineWidth = cursorType.value === 'eraser' ? brushSize : 2;
  ctx.lineCap = 'round';
  ctx.strokeStyle = cursorType.value === 'eraser' ? '#f5f5dc' : brushColor.value;

  if (cursorType.value === 'eraser') {
    ctx.clearRect(x - brushSize / 2, y - brushSize / 2, brushSize, brushSize);
    // Store the eraser path
    // eraserArray.value.push([x, y]);
   // arrayArray.value.push({ type: "eraser", data: [x, y] });
  } else {
    ctx.lineTo(x, y);
    ctx.stroke();
  }
};

const sendToBackend = async (path) => {
  isLoading.value = true;  // Show the loading popup
  const canvas = canvasRef.value;
  const bottomY = canvas.height;

  try {
    await processPath(mapName, path, bottomY);

    // Store the green coordinates
    // storedGreenCoordinates.value.push(result.greenCoordinates);
   // arrayArray.value.push({ type: "stroke", data: result.greenCoordinates });

    // Update the map with the new area
    await updateMapArea();
  } catch (error) {
    console.error('Error sending path to backend:', error);
  } finally {
    isLoading.value = false;  // Hide the loading popup
  }
};

const updateMapArea = async () => {
  ctx.beginPath();

  // Set color based on active theme
  ctx.strokeStyle = brushColor.value;
  ctx.lineWidth = 2;

  const result = await retrieveMap(mapName);
  console.log('Result from retrieveMap:', result);

  result.arrayArray.forEach(({ type, data }) => {
    console.log(`Processing type: ${type}, data:`, data);

    if (type === "eraserArray" && Array.isArray(data.data)) {
      console.log('Eraser data:', data);
      // ctx.clearRect(data.data[0] - brushSize / 2, data.data[1] - brushSize / 2, brushSize, brushSize);
      data.data.forEach(([x, y]) => {
        ctx.clearRect(x - brushSize / 2, y - brushSize / 2, brushSize, brushSize);
      });
    } else if (type === "greenCoordinates" && data && Array.isArray(data.data)) {
      console.log('Stroke data:', data.data);
      ctx.beginPath();
      data.data.forEach(([x, y]) => {
        ctx.lineTo(x, y);
      });
      ctx.stroke();
    } else if (type === "imageArray" && Array.isArray(data.data)) {
      console.log('Image data:', data);
      console.log('X:', data.data[0], 'Y:', data.data[1]);
      const img = new Image();
      img.src = obstructionIconPath.value;
      img.onload = () => {
        ctx.drawImage(img, data.data[0] - 29 / 2, data.data[1] - 29 / 2, 29, 37);
      };
    } else {
      console.warn(`Unexpected data type or structure for type: ${type}`, data);
    }
  });

  console.log('Tank1:', result.tank1pos);
  console.log('Tank2:', result.tank2pos);
  if (result.tank1pos[0] !== 0 || result.tank1pos[1] !== 0) {
    const newTank1 = new Image();
    newTank1.src = tank1.value;
    newTank1.onload = () => {
      ctx.drawImage(newTank1, result.tank1pos[0] - 12, result.tank1pos[1] - 12, 24, 24);
    };
  }
  if (result.tank2pos[0] !== 0 || result.tank2pos[1] !== 0) {
    const newTank2 = new Image();
    newTank2.src = tank2.value;
    newTank2.onload = () => {
      ctx.drawImage(newTank2, result.tank2pos[0] - 12, result.tank2pos[1] - 12, 24, 24);
    };
  }

};

const updateBrushCircle = (event) => {
  if (!eraserActive.value) return;

  const brushCircle = document.querySelector('.brush-circle');
  brushCircle.style.display = 'block';

  const rect = canvasRef.value.getBoundingClientRect();
  const x = (event.clientX - rect.left) / props.scaleFactor;
  const y = (event.clientY - rect.top) / props.scaleFactor;

  brushCircle.style.left = `${x - brushSize /2}px`;
  brushCircle.style.top = `${y - brushSize /2}px`;
};

const hideBrushCircle = () => {
  document.querySelector('.brush-circle').style.display = 'none';
};

const onDrop = (event) => {
  event.preventDefault();
  console.log('onDrop event triggered');

  //if (cursorType.value !== 'obstruction') return;

  // Get the drop coordinates
  const rect = canvasRef.value.getBoundingClientRect();
  const x = (event.clientX - rect.left) / props.scaleFactor;
  const y = (event.clientY - rect.top) / props.scaleFactor;
  console.log(`Drop coordinates: x=${x}, y=${y}`);

  // Get the dragged image URL
  let imgUrl;
  if (focusedTank.value === 1) {
    imgUrl = tank1.value;
    tank1Dropped.value = true; // Mark tank1 as dropped
    //focusedTank.value = null;
  } else if (focusedTank.value === 2) {
    imgUrl = tank2.value;
    tank2Dropped.value = true; // Mark tank2 as dropped
    //focusedTank.value = null;
  } else {
    imgUrl = obstructionIconPath.value;
  }
  console.log(`Image URL: ${imgUrl}`);

  // Create a new image element to draw on the canvas
  const img = new Image();
  img.src = imgUrl;
  img.crossOrigin = 'anonymous'; // Enable CORS for the image
  img.onload = () => {
    const desiredWidth = 29; // Set the desired width
    const desiredHeight = 37; // Set the desired height
    console.log('Image loaded, starting animation');
    animateImage(img, x, y, desiredWidth, desiredHeight);
  };
};

const animateImage = (img, startX, startY, width, height) => {
  let y = startY;
  const gravity = 1; // Gravity effect

  const step = async () => {
    ctx.clearRect(startX - width / 2, y - height / 2, width, height); // Clear previous image position

    // Check for collision with any non-transparent color TODO: CHANGE THIS MAGIC THING
    const imageData = ctx.getImageData(startX - 10, y + height / 2, width, 1).data;
    let collision = false;

    // Check if all pixels in the row are transparent
    for (let i = 3; i < imageData.length; i += 4) { // Iterate over alpha values
      if (imageData[i] > 30) { // Check for non-transparent pixel
        collision = true;
        break;
      }
    }

    if (!collision) {
      y += gravity; // Apply gravity
      ctx.drawImage(img, startX - width / 2, y - height / 2, width, height); // Draw image at new position
      requestAnimationFrame(step); // Continue animation
    } else {
      ctx.drawImage(img, startX - width / 2, y - height / 2, width, height); // Draw image at final position
      // imageArray.value.push({ x: startX, y, desiredWidth: width, desiredHeight: height }); // Store final position
      //  arrayArray.value.push({type: "image", data: { x: startX, y, desiredWidth: width, desiredHeight: height }}); // Store final position

      if (focusedTank.value === 1) {
        await addPlayerPosition(mapName, 1, [startX, y]);
        focusedTank.value = null;
      } else if (focusedTank.value === 2) {
        await addPlayerPosition(mapName, 2, [startX, y]);
        focusedTank.value = null;
      } else {
        console.log('Adding new image to the map');
        await addNewImage(mapName, startX, y);
      }

      await updateMapArea();
    }
  };

  step(); // Start the animation
};

const clearMap = async () => {
  if (canvasRef.value) {
    ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);
  } else {
    console.error('Canvas reference is null');
  }
  await addPlayerPosition(mapName, 1, [0.0, 0.0]);
  await addPlayerPosition(mapName, 2, [0.0, 0.0]);
  await deleteMap("map1");
  await createMap(mapName);
};

const rollDice = async () => {
  const path = [];
  let previousY = Math.random() * 500; // Initial random y value

  for (let x = 1; x <= 899; x++) {
    const y = previousY + (Math.random() * 20 - 10); // Random y value close to previous y
    path.push([x, y]);
    previousY = y; // Update previous y
  }

  await sendToBackend(path);
};

onMounted(async () => {
  await deleteMap("map1");
  const canvas = canvasRef.value;
  ctx = canvas.getContext('2d', { willReadFrequently: true });

  document.addEventListener('mousedown', startDrawing);
  document.addEventListener('mouseup', stopDrawing);
  document.addEventListener('mousemove', (event) => {
    draw(event);
    updateBrushCircle(event); // Update circle position while moving
  });
  canvas.addEventListener('mouseleave', hideBrushCircle); // Hide circle when mouse leaves canvas

  await createMap(mapName);
});

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', startDrawing);
  document.removeEventListener('mouseup', stopDrawing);
  document.removeEventListener('mousemove', draw);
});

const openModal = () => {

  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveMap = async (name) => {
  // Implement save map logic here
  console.log('Saving map:', name);
  let new_name
  if (name === ''){
    let name_num;
    name_num = await retrieveNumOfMaps();
    new_name = `map${name_num.numOfMaps + 1}`;
  } else {
    new_name = name;
  }
  await copyMap(new_name, mapName);
};

// const saveAndReturn = async (name) => {
//   // Implement save and return logic here
//   console.log('Saving and returning map:', name);
//   // Add logic to return to the previous page or state
//   await copyMap(name, mapName);
//   await clearMap();
// };

const startPlaying = async () => {
  // Implement logic to start playing the game
  console.log('Starting the game');
  let name_num;
  name_num = await retrieveNumOfMaps();
  let new_name = `map${name_num.numOfMaps + 1}`;
  await copyMap(new_name, mapName);
  // await clearMap();
};

const focusTank = async (tankNumber) => {
  if (tankNumber === 1 && tank1Dropped.value) {
    await addPlayerPosition(mapName, 1, [0.0, 0.0]);
    tank1Dropped.value = false;
    focusedTank.value = null;
    tank1.value = playerA;
    isLoading.value = true;  // Show the loading popup
    try {
      ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);
      await updateMapArea();
    } catch (error) {
      console.error('Error updating map area:', error);
    } finally {
      isLoading.value = false;  // Hide the loading popup
    }
  } else if (tankNumber === 2 && tank2Dropped.value) {
    await addPlayerPosition(mapName, 2, [0.0, 0.0]);
    tank2Dropped.value = false;
    focusedTank.value = null;
    tank2.value = playerB;
    isLoading.value = true;  // Show the loading popup
    try {
      ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);
      await updateMapArea();
    } catch (error) {
      console.error('Error updating map area:', error);
    } finally {
      isLoading.value = false;  // Hide the loading popup
    }
  } else {
    if (focusedTank.value === tankNumber) {
      focusedTank.value = null; // Unfocus if already focused
    } else {
      focusedTank.value = tankNumber; // Focus the clicked tank
    }
  }
  console.log(`Tank ${tankNumber} ${focusedTank.value === tankNumber ? 'focused' : 'unfocused'}`);
};

const onDragStart = (event, tankNumber) => {
  cursorType.value = '';
  if ((tankNumber === 1 && tank1Dropped.value) || (tankNumber === 2 && tank2Dropped.value)) {
    event.preventDefault(); // Prevent dragging if the tank has been dropped
    return;
  }
  event.dataTransfer.setData('tankNumber', tankNumber);
  focusedTank.value = tankNumber;
  console.log(`Dragging tank ${tankNumber}`);
};

const goBack = () => {
  clearMap()
  router.back();
};

</script>

<template>
  <div :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`}">

    <div class="bg-beige flex flex-col items-center relative custom-cursor">

      <button @click="goBack" class="back-button border-4 border-blue-700 bg-blue-300 hover:bg-blue-400 font-bold text-xl py-2 px-4 rounded-2xl">
        GO BACK
      </button>

      <ThemeSelector :activeTheme="activeTheme" @theme-change="updateTheme" class="theme-selector"/>

      <div class="canvas-container">
        <canvas ref="canvasRef" width="900" height="500" class="border-2 border-black"
                @dragover.prevent
                @drop="onDrop"
        ></canvas>
        <div class="brush-circle"></div>
      </div>

      <OperationSelector :activeTheme="activeTheme" @cursor-change="updateCursor" class="operation-selector"/>

      <RenderingScreen :visible="isLoading" message="Rendering..." />

      <button @click="rollDice" class="dice-button border-8 border-red-700 bg-red-300 hover:bg-red-400 font-bold text-xl py-4 px-6 rounded-2xl">
        <img src="/assets/dice.svg" alt="Dice" class="w-full h-full"/>
      </button>

      <div class="flex justify-between w-3/4  mt-4 mb-8 pt-6 gap-4">
        <button @click="clearMap" class="border-4 border-red-700 text-center bg-red-300 hover:bg-red-400 font-bold text-xl py-4 px-4 rounded-2xl w-1/5">
          CLEAR MAP
        </button>

        <button @click="openModal" class="border-4 border-green-700 text-center bg-green-300 hover:bg-green-400 font-bold text-xl py-4 px-4 rounded-2xl w-1/5">
          SAVE MAP
        </button>

        <SaveMap
          :visible="showModal"
          :onSave="saveMap"
          :onClose="closeModal"
        />

        <router-link v-if="showStartPlayingButton" to="/chooseMap" @click="startPlaying" class="border-4 border-blue-700 text-center bg-blue-300 hover:bg-blue-400 font-bold text-xl py-4 px-4 rounded-2xl w-1/5">
          START PLAYING
        </router-link>
      </div>

      <div class="absolute top-7 right-[25%] transform translate-x-1/2 flex gap-4">
        <div v-if="tank1"
             :class="['w-24 h-24 rounded-full overflow-hidden hover:scale-110 transition-transform duration-300', focusedTank === 1 ? 'border-8 border-black' : 'border-8 border-gray-300']"
             style="background-color: #16b4d8;"
             @click="focusTank(1)">
          <img :src="tank1Dropped ? backicon : tank1" class="w-full h-full p-2" draggable="true" @dragstart="onDragStart($event, 1)"/>
        </div>
        <div v-if="tank2"
             :class="['w-24 h-24 rounded-full overflow-hidden hover:scale-110 transition-transform duration-300', focusedTank === 2 ? 'border-8 border-black' : 'border-8 border-gray-300']"
             style="background-color: #ffcc99;"
             @click="focusTank(2)">
          <img :src="tank2Dropped ? backicon : tank2" class="w-full h-full p-2" draggable="true" @dragstart="onDragStart($event, 2)"/>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>
.hover\:scale-110:hover {
  transform: scale(1.10);
}
.extra-margin {
  margin-top: 10px; /* Adjust the value as needed */
}
.w-full {
  width: 100%;
}

.h-full {
  height: 100%;
}

.object-cover {
  object-fit: cover;
}
.bg-beige {
  background-color: #f5f5dc; /* Beige color */
}

.canvas-container {
  position: relative;
  display: inline-block;
  margin-top: 150px; /* Adjust the value as needed */

}

.theme-selector {
  position: absolute;
  top: 30px; /* Adjust as needed */
  left: 50%;
  transform: translateX(-50%);
}

.operation-selector {
  position: absolute;
  top: 40%;
  right: 90px; /* Adjust as needed */
  transform: translateY(-50%);
}


.dice-button {
  position: absolute;
  top: 65%; /* Adjust as needed */
  right: 90px; /* Adjust as needed */
  width: 110px; /* Adjust size as needed */
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
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

.back-button {
  position: absolute;
  top: 50px; /* Align with tank buttons */
  left: 220px; /* Adjust as needed */
}

</style>


