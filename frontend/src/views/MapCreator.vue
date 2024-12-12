<!--
  File: MapCreator.vue
  Author: Marek Effenberger (xeffen00)
-->
<script setup>

import { ref, onMounted, onBeforeUnmount, defineProps } from 'vue';
import ThemeSelector from '@/components/MapCreatorComponents/ThemeSelector.vue';
import OperationSelector from '@/components/MapCreatorComponents/OperationSelector.vue';
import SaveMap from '@/components/MapCreatorComponents/SaveMap.vue';
import RenderingScreen from "@/components/MapCreatorComponents/RenderingScreen.vue";
import { useRouter, useRoute } from 'vue-router';
import playerA from '../../public/assets/player_a.svg';
import playerB from '../../public/assets/player_b.svg';
import back from '../../public/assets/back.svg';

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
} from '@/components/MapCreatorComponents/BackendOperations.js';

// Supportive variables for the controller logic
// Utilized for the message appearance when the user tries to save the map without dropping both tanks
const showPopup = ref(false);
const popupMessage = ref('');
const showModal = ref(false);

// Define the properties for the controller (shared dimensions across the game components)
const props = defineProps({
  gameWidth: Number,
  gameHeight: Number,
  scaleFactor: Number,
});

// Utilized for the routing and the current route
const router = useRouter();
const route = useRoute();

// Active theme selected by the user -> representation of the html element of the theme
const activeTheme = ref('forest');
// Cursor type selected by the user -> representation of the html element of the cursor (pen, eraser, obstruction)
const cursorType = ref('');
// Controller variable whether the eraser is active or not
const eraserActive = ref(false);
// Variable used to show loading screen when the map is being rendered
const isLoading = ref(false);
// Brush size for the eraser
const brushSize = 25;
// Brush color for the pen
const brushColor = ref('#2e7d32');
// Path to the obstruction icon
const obstructionIconPath = ref('/assets/tree_icon.svg');
// Variable set to true when the user is coming from the map selector (meaning the user is here and wants to start playing)
const showStartPlayingButton = ref(route.query.fromMapSelector === 'true');
// Variable to store the focused tank (1 or 2) -> utilized for the tank dragging
const focusedTank = ref(null);
// Variables to store the tank images
const tank1 = ref(playerA);
const tank2 = ref(playerB);
// Variable to store the back icon
const backicon = ref(back);
// Variables to store whether the tanks have been dropped (showing of the back button)
const tank1Dropped = ref(false);
const tank2Dropped = ref(false);

// Reference to the canvas element
const canvasRef = ref(null);
// Reference to the canvas context
let ctx = null;
// Variable to store the drawing state
let drawing = false;
// Variable to store the drawn path (array of points)
let drawnPath = [];
// Default map name (this map is never saved -> is used as a dummy map)
const mapName = 'map1';

// Function to update the theme of the map
// Sets the color and the obstruction icon based on the selected theme
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

// Function to update the cursor type (pen, eraser, obstruction)
const updateCursor = (type) => {
  cursorType.value = type;
  let cursorUrl;
  if (type === 'eraser') {
    eraserActive.value = true;
  } else {
    eraserActive.value = false;
  }
  switch (type) {
    case 'pen':
      cursorUrl = '/assets/pen_icon_png.png';
      break;
    case 'eraser':
      cursorUrl = '/assets/eraser_mouse_png.png';
      break;
    case 'obstruction':
    default:
      cursorUrl = 'auto';
  }
  document.querySelector('.custom-cursor').style.cursor = `url(${cursorUrl}), auto`;
};

// Function to start drawing on the canvas (storing the points of the line, when released -> send to the backend)
const startDrawing = (event) => {
  drawing = true;
  drawnPath = [];
  ctx.beginPath();
  draw(event);
};

// Function to stop drawing on the canvas (send the path to the backend)
const stopDrawing = async () => {
  if (!drawing) return;
  drawing = false;
  ctx.beginPath();
  if (drawnPath.length > 0) {
    if (cursorType.value === 'eraser') {
      await erasePath(mapName, drawnPath);
    } else if (cursorType.value === 'pen') {
      await sendToBackend(drawnPath);
    }
  }
};

// Function to draw on the canvas (pen, eraser, obstruction)
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

  // If the cursor is an eraser, clear the area (rectangle) around the point
  if (cursorType.value === 'eraser') {
    ctx.clearRect(x - brushSize / 2, y - brushSize / 2, brushSize, brushSize);
  } else {
    ctx.lineTo(x, y);
    ctx.stroke();
  }
};

// After the path is drawn, send it to the backend for processing, redraw the map with the new area
const sendToBackend = async (path) => {
  isLoading.value = true;  // Show the loading popup
  const canvas = canvasRef.value;
  const bottomY = canvas.height;

  try {
    await processPath(mapName, path, bottomY);
    // Update the map with the new area
    await updateMapArea();
  } catch (error) {
    console.error('Error sending path to backend:', error);
  } finally {
    isLoading.value = false;  // Hide the loading popup
  }
};

// Update the map area based on the stored data (drawn paths, images, player positions)
// The most important function for the map rendering
// Calls the object from the BE and iteratively goes through the array of objects to draw the map
const updateMapArea = async () => {
  ctx.beginPath();

  ctx.strokeStyle = brushColor.value;
  ctx.lineWidth = 2;

  const result = await retrieveMap(mapName);

  result.arrayArray.forEach(({ type, data }) => {
    if (type === "eraserArray" && Array.isArray(data.data)) {
      data.data.forEach(([x, y]) => {
        ctx.clearRect(x - brushSize / 2, y - brushSize / 2, brushSize, brushSize);
      });
    } else if (type === "greenCoordinates" && data && Array.isArray(data.data)) {
      ctx.beginPath();
      data.data.forEach(([x, y]) => {
        ctx.lineTo(x, y);
      });
      ctx.stroke();
    } else if (type === "imageArray" && Array.isArray(data.data)) {
      const img = new Image();
      img.src = obstructionIconPath.value;
      img.onload = () => {
        ctx.drawImage(img, data.data[0] - 29 / 2, data.data[1] - 29 / 2, 29, 37);
      };
    } else {
      console.warn(`Unexpected data type or structure for type: ${type}`, data);
    }
  });
  // Draw the player positions
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

// Update the brush circle position while moving the mouse
// Glow effect for the eraser
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

// Hide the brush circle when the mouse leaves the canvas
const hideBrushCircle = () => {
  document.querySelector('.brush-circle').style.display = 'none';
};

// Function to handle the drop event on the canvas
// Enables animation of the dropped image (tank, obstruction)
const onDrop = (event) => {
  event.preventDefault();

  // Get the drop coordinates
  const rect = canvasRef.value.getBoundingClientRect();
  const x = (event.clientX - rect.left) / props.scaleFactor;
  const y = (event.clientY - rect.top) / props.scaleFactor;

  // Get the dragged image URL
  let imgUrl;
  if (focusedTank.value === 1) {
    imgUrl = tank1.value;
    tank1Dropped.value = true;
  } else if (focusedTank.value === 2) {
    imgUrl = tank2.value;
    tank2Dropped.value = true;
  } else {
    imgUrl = obstructionIconPath.value;
  }

  // Create a new image element to draw on the canvas
  const img = new Image();
  img.src = imgUrl;
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    const desiredWidth = 29;
    const desiredHeight = 37;
    animateImage(img, x, y, desiredWidth, desiredHeight);
  };
};

// Function to animate the image (tank, obstruction) when dropped on the canvas
// Utilizes gravity effect to animate the image falling down
// Draws an imaginary line at the bottom of the image to check for collision with the ground
// Effectively looks for some change in color to detect the ground
// When the image hits the ground, the final position is stored in the backend
const animateImage = (img, startX, startY, width, height) => {
  let y = startY;
  const gravity = 1;

  const step = async () => {
    ctx.clearRect(startX - width / 2, y - height / 2, width, height);

    const imageData = ctx.getImageData(startX - 10, y + height / 2, width, 1).data;
    let collision = false;

    for (let i = 3; i < imageData.length; i += 4) {
      // Some magical threshold which works for the beige background
      if (imageData[i] > 30) {
        collision = true;
        break;
      }
    }

    if (!collision) {
      y += gravity;
      ctx.drawImage(img, startX - width / 2, y - height / 2, width, height);
      requestAnimationFrame(step);
    } else {
      ctx.drawImage(img, startX - width / 2, y - height / 2, width, height); // Draw image at final position

      // Store the final position in the backend, based on the focused tank (otherwise store the obstruction)
      if (focusedTank.value === 1) {
        await addPlayerPosition(mapName, 1, [startX, y]);
        focusedTank.value = null;
      } else if (focusedTank.value === 2) {
        await addPlayerPosition(mapName, 2, [startX, y]);
        focusedTank.value = null;
      } else {
        await addNewImage(mapName, startX, y);
      }
      await updateMapArea();
    }
  };
  // Go for another step
  step();
};

// Function to clear the map (clear the canvas, reset the player positions)
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

// Function to roll the dice (generate a random path)
// Click on your own risk, the random path takes forever to render
const rollDice = async () => {
  const path = [];
  let previousY = Math.random() * 500;

  for (let x = 1; x <= 899; x++) {
    const y = previousY + (Math.random() * 20 - 10);
    path.push([x, y]);
    previousY = y;
  }
  await sendToBackend(path);
};

// On mounted, set the canvas context, add event listeners for drawing
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

// On before unmount, remove the event listeners
onBeforeUnmount(() => {
  document.removeEventListener('mousedown', startDrawing);
  document.removeEventListener('mouseup', stopDrawing);
  document.removeEventListener('mousemove', draw);
});

// Function to open the save map modal
const openModal = () => {
  cursorType.value = '';
  showModal.value = true;
};

// Function to close the save map modal
const closeModal = () => {
  showModal.value = false;
};

// Function to show a popup message for 3 seconds
const showPopupMessage = (message) => {
  popupMessage.value = message;
  showPopup.value = true;
  setTimeout(() => {
    showPopup.value = false;
  }, 3000);
};

// Function to save the map (with a given name or a default name)
const saveMap = async (name) => {
  cursorType.value = '';
  if (!tank1Dropped.value || !tank2Dropped.value) {
    showPopupMessage('You Have To Drop Both Tanks!');
    return;
  }
  let new_name
  if (name === ''){
    let name_num;
    name_num = await retrieveNumOfMaps();
    new_name = `map${name_num.numOfMaps + 1}`;
  } else {
    new_name = name;
  }
  await copyMap(new_name, mapName);
  await clearMap()
  router.back();
};

// Function to start playing the game (only shown when the user comes from the map selector)
const startPlaying = async () => {
  if (!tank1Dropped.value || !tank2Dropped.value) {
    showPopupMessage('You Have To Drop Both Tanks!');
    return;
  }
  let name_num;
  name_num = await retrieveNumOfMaps();
  let new_name = `map${name_num.numOfMaps + 1}`;
  await copyMap(new_name, mapName);
};

// Function to focus the tank (1 or 2) -> utilized for the dragging
// If the tank is dropped, the back icon appears for its reversal
// It runs the render, so it gets a bit slow
const focusTank = async (tankNumber) => {
  if (tankNumber === 1 && tank1Dropped.value) {
    await addPlayerPosition(mapName, 1, [0.0, 0.0]);
    tank1Dropped.value = false;
    focusedTank.value = null;
    tank1.value = playerA;
    isLoading.value = true;
    try {
      ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);
      await updateMapArea();
    } catch (error) {
      console.error('Error updating map area:', error);
    } finally {
      isLoading.value = false;
    }
  } else if (tankNumber === 2 && tank2Dropped.value) {
    await addPlayerPosition(mapName, 2, [0.0, 0.0]);
    tank2Dropped.value = false;
    focusedTank.value = null;
    tank2.value = playerB;
    isLoading.value = true;
    try {
      ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);
      await updateMapArea();
    } catch (error) {
      console.error('Error updating map area:', error);
    } finally {
      isLoading.value = false;
    }
  } else {
    if (focusedTank.value === tankNumber) {
      focusedTank.value = null;
    } else {
      focusedTank.value = tankNumber;
    }
  }
};

// Function to handle the drag start event (when the user starts dragging the tank)
const onDragStart = (event, tankNumber) => {
  cursorType.value = '';
  if ((tankNumber === 1 && tank1Dropped.value) || (tankNumber === 2 && tank2Dropped.value)) {
    event.preventDefault();
    return;
  }
  event.dataTransfer.setData('tankNumber', tankNumber);
  focusedTank.value = tankNumber;
  console.log(`Dragging tank ${tankNumber}`);
};

// Function to go back (clear the map and go back to the previous page)
const goBack = async () => {
  await clearMap()
  router.back();
};

</script>

<template>
  <div :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`}">

    <div class="bg-beige flex flex-col items-center relative custom-cursor">

<!--      Button to go back to the previous page-->
      <button @click="goBack" class="back-button border-4 border-blue-700 bg-blue-300 hover:bg-blue-400 font-bold text-xl py-2 px-4 rounded-2xl">
        GO BACK
      </button>
<!--      Component to select the theme of the map-->
      <ThemeSelector :activeTheme="activeTheme" @theme-change="updateTheme" class="theme-selector"/>

<!--      Canvas container with the canvas element and the brush circle-->
      <div class="canvas-container">
        <canvas ref="canvasRef" width="900" height="500" class="border-2 border-black"
                @dragover.prevent
                @drop="onDrop"
        ></canvas>
        <div class="brush-circle"></div>
      </div>

<!--      Component to select the operation (pen, eraser, obstruction)-->
      <OperationSelector :activeTheme="activeTheme" @cursor-change="updateCursor" class="operation-selector"/>

<!--      Loading screen when the map is being rendered-->
      <RenderingScreen :visible="isLoading" message="Rendering..." />

<!--      Button to roll the dice (generate a random path, just don't)-->
      <button @click="rollDice" class="dice-button border-8 border-red-700 bg-red-300 hover:bg-red-400 font-bold text-xl py-4 px-6 rounded-2xl">
        <img src="/assets/dice.svg" alt="Dice" class="w-full h-full"/>
      </button>

<!--      Buttons to clear the map, save the map, start playing the game-->
      <div class="flex justify-between w-3/4  mt-4 mb-8 pt-6 gap-4">
        <button @click="clearMap" class="border-4 border-red-700 text-center bg-red-300 hover:bg-red-400 font-bold text-xl py-4 px-4 rounded-2xl w-1/5">
          CLEAR MAP
        </button>

        <button @click="openModal" class="border-4 border-green-700 text-center bg-green-300 hover:bg-green-400 font-bold text-xl py-4 px-4 rounded-2xl w-1/5">
          SAVE MAP
        </button>

<!--        Save map component (modal)-->
        <SaveMap
          :visible="showModal"
          :onSave="saveMap"
          :onClose="closeModal"
        />

        <router-link v-if="showStartPlayingButton" to="/chooseMap" @click="startPlaying" class="border-4 border-blue-700 text-center bg-blue-300 hover:bg-blue-400 font-bold text-xl py-4 px-4 rounded-2xl w-1/5">
          START PLAYING
        </router-link>
      </div>

<!--      Tank images (player A, player B)-->
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

<!--      Popup message when the user tries to save the map without dropping both tanks-->
      <div v-if="showPopup" class="popup-message fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white py-2 px-4 rounded">
        {{ popupMessage }}
      </div>

    </div>

  </div>
</template>

<style scoped>
.hover\:scale-110:hover {
  transform: scale(1.10);
}
.extra-margin {
  margin-top: 10px;
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
  background-color: #f5f5dc;
}

.canvas-container {
  position: relative;
  display: inline-block;
  margin-top: 150px;

}

.theme-selector {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
}

.operation-selector {
  position: absolute;
  top: 40%;
  right: 90px;
  transform: translateY(-50%);
}


.dice-button {
  position: absolute;
  top: 65%;
  right: 90px;
  width: 110px;
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.brush-circle {
  position: absolute;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: rgba(41, 220, 70, 0.3);
  box-shadow: 0 0 10px rgba(78, 238, 61, 0.7);
  pointer-events: none;
  display: none;
}

.back-button {
  position: absolute;
  top: 50px;
  left: 220px;
}

.popup-message {
  z-index: 1000;
}

</style>


