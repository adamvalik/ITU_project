<template>
    <div class="game-screen text-center mt-10">
      <h1 class="text-2xl font-bold mb-4">Tanks</h1>
      <label class="block"><span class="font-bold">Wind: <span class="text-2xl">{{ wind }}</span> </span>  (positive for right, negative for left)</label>
      <div class="controls mt-4 flex justify-center items-center gap-4">
        <div>
          <label class="block font-bold">Angle: {{ angle }}°</label>
          <input 
            type="range" 
            min="0" 
            max="90" 
            v-model="angle" 
            class="w-32"
          />
        </div>
        <div>
          <label class="block font-bold">Power: {{ power }}</label>
          <input 
            type="range" 
            min="10" 
            max="100" 
            v-model="power" 
            class="w-32"
          />
        </div>
      </div>
      <div
        class="h-48 bg-black bg-opacity-80 bg-neutral-900 text-white m-auto items-center justify-center flex flex-rows space-x-6"
        style="width: 1280px;">
        <!-- style="background: url('assets/metalbg.png') no-repeat center center; background-size: cover; width: 1280px;"> -->

        <div class="flex flex-col space-y-1">
          <div>
            <button
              mouseover="showFireHelp"
              @mouseleave="hideFireHelp"
              @click="fireMissile"
              class="ml-4 w-96 h-16 bg-blue-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-blue-400 font-bold text-4xl">
              WEAPON SELECTOR
            </button>
          </div>

          <div>
            <button
              mouseover="showFireHelp"
              @mouseleave="hideFireHelp"
              @click="fireMissile"
              class="ml-4 w-96 h-16 bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-4">
                <div class="text-black font-bold text-3xl">SMALL MISSILE</div>
                <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                <div class="text-black font-bold text-3xl">20</div>
              </div>
               
            </button>
          </div>
      </div>
        <!-- <img src="assets/small_missile_icon.png" alt="Missile Icon"> -->

        <div class="relative">
          <button
              @mouseover="showFireHelp"
              @mouseleave="hideFireHelp"
              @click="fireMissile"
              class="w-80 py-16 bg-red-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-red-400 font-bold text-4xl">
              FIRE
            <span v-if="fireHelpVisible" class="absolute top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-2xl">
              Click to fire!
            </span>
          </button>
        </div>

        <!-- Row flex for money, time and so on -->
        <div class ="flex flex-rows space-x-8">

          <div class ="flex flex-col space-y-4">
            <div class="font-bold text-white text-2xl">
              <h1>{{ time }} (s)</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/time_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2">
            <div class="font-bold text-white text-2xl">
              <h1>{{ money }}$</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/money_bag_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2, items-center">
            <div class="font-bold text-white text-2xl">
              <h1>{{ fuel }}/{{ fuelMax }}</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/fuel_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-3">
            <div class="font-bold text-white text-2xl">
              <h1>{{ wins }}win</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/trophy_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

        </div>

        <!-- Pause button, absolute position from the bar-->
        <div class="relative mb-16">
          <div class="w-20 h-20" style="background: url('assets/pause_icon.png') no-repeat center center; background-size: cover;"></div>
        </div>

        
        
      </div>

    </div>
      <canvas 
        ref="gameCanvas" 
        :width="canvasWidth" 
        :height="canvasHeight" 
        class="border border-gray-700 m-auto"
        @mousemove="onMouseMove"
        @click="onMouseClick"
        @mouseleave="onMouseLeave"
        @mouseup="onMouseUp"
        @mousedown="onMouseDown"
      ></canvas>
      <img :src="'assets/svgtank1.svg'" alt="Tank" id="tankImage" style="display: none;"/>


      <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <!-- Tank -->
      <rect x="30" y="50" width="40" height="10" fill="lightgreen" />
      <rect x="40" y="45" width="20" height="5" fill="green" />
      <circle cx="35" cy="62" r="3" fill="black" />
      <circle cx="65" cy="62" r="3" fill="black" />

      <!-- Arc for shell trajectory -->
      <path d="M 50 50 A 30 30 0 0 1 80 20" fill="none" stroke="blue" stroke-width="2" />
      </svg>


  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: "GameScreen",
    data() {
      return {
        canvasWidth: 1280,
        canvasHeight: 720,
        terrain: [],
        player1: {
          x: 100,
          y: 370,
          size: 40,
          angle: 45,
          power: 50,
          tankColor: "green",
          name: "DJ Khaled",
          health: 100,
        },
        mousePosition: {
          x: 0,
          y: 0,
        },
        isHovering: false,
        aimCircleRadius: 200,
        maxShotPower: 100,
        minShotPower: 1,
        minShotDistance: 50,
        stopLine: false,
        lineStopX: 200,
        lineStopY: 400,
        isDragging: false,

        wind: 0,
        missile: null,
        angle: 45,
        power: 50,
        gameOver: false,
        fireHelpVisible: false,
        time: 10,
        money: 4000,
        fuel: 100,
        fuelMax: 250,
        wins: 1,
      };
    },
    mounted() {
      this.wind = 0;//Math.floor(Math.random() * 100 - 50); 
      this.player1.tankColor = "green"; //this.$route.query.color;
      this.startTimer();
      this.generateTerrain();
      this.renderGame();
    },
    methods: {
      showFireHelp() {
        this.fireHelpVisible = true;
      },
      hideFireHelp() {
        this.fireHelpVisible = false;
      },

      drawPlayerNames(ctx) {
        ctx.save();

        //size of rectangles for healthbars
        const player1X = 10 + 200 / 2;
        const player2X = 1070 + 200 / 2;

        ctx.font = "28px Montserrat";
        ctx.fillStyle = "black";
        // ctx.textAlign = "left";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(this.player1.name, player1X, 30);
        ctx.fillText("Player 2", player2X, 30);
        ctx.restore();
      },

      drawPlayerHealth(ctx){
        ctx.save();
        // const canvas = this.$refs.canvas;
        // const ctx = canvas.getContext('2d');

        ctx.fillStyle = 'black'; // White color
        ctx.fillRect(10, 50, 200, 40);

        ctx.fillRect(1070, 50, 200, 40);

        // Draw red fill
        ctx.fillStyle = '#FF0000'; // Red color
        ctx.fillRect(10, 50, 180, 40); // Adjusted for border thickness
        ctx.fillRect(1070, 50, 180, 40); // Adjusted for border thickness

        //Draw outline
        ctx.strokeStyle = 'gray';
        ctx.lineWidth = 5; // Border width
        ctx.strokeRect(10, 50, 200, 40);
        ctx.strokeRect(1070, 50, 200, 40);

        ctx.fillStyle = '#000000'; // Text color
        ctx.font = '20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('80/100', 110, 70);
        ctx.fillText('80/100', 1170, 70);

        ctx.restore();
      },

      startTimer() {
        setInterval(() => {
          if (this.time > 0) {
            this.time--;
          } else {
            this.gameOver = true;
          }
        }, 1000);
      },

      generateTerrain() {
        // Generate a simple random terrain within 2/3 of the canvas height
        const maxTerrainHeight = (this.canvasHeight * 2) / 3;
        this.terrain = new Array(this.canvasWidth).fill(0).map((_, x) => {
          const baseHeight = maxTerrainHeight; // Base height is 2/3 of the canvas height
          const variation = Math.sin(x * 0.06) * 15 + Math.sin(x * 0.1) * 10 + Math.sin(x * 0.01) * 50;
          return baseHeight + variation;
        });
      },

      fireMissile() {
        const startX = this.player1.x + 15;
        const startY = this.player1.y - 15; //this.terrain[Math.floor(player.x)] - player.size / 2
        const controlX = startX + Math.cos(this.angle * (Math.PI / 180)) * this.power * 5 + this.wind * 4;
        const controlY = startY - Math.sin(this.angle * (Math.PI / 180)) * this.power * 5;
        const endX = controlX + Math.cos(this.angle * (Math.PI / 180)) * this.power * 5 + this.wind * 8;
        const endY = this.canvasHeight;
  
        this.missile = {
          t: 0,
          startX,
          startY,
          controlX,
          controlY,
          endX,
          endY,
        };
  
        this.animateMissile();
      },
      animateMissile() {
        if (!this.missile) return;
  
        const { t, startX, startY, controlX, controlY, endX, endY } = this.missile;
  
        const x = (1 - t) * (1 - t) * startX + 2 * (1 - t) * t * controlX + t * t * endX;
        const y = (1 - t) * (1 - t) * startY + 2 * (1 - t) * t * controlY + t * t * endY;
  
        this.missile.t += 0.01;
        if (this.missile.t >= 1 || this.checkTerrainCollision(x, y)) {
          this.explodeTerrain(x, y);
          this.missile = null;
          this.gameOver = true;
          return;
        }
  
        this.renderGame();
  
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext("2d");
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();
  
        requestAnimationFrame(this.animateMissile);
      },
      checkTerrainCollision(x, y) {
        // Check if the missile hit the terrain
        return y >= this.terrain[Math.floor(x)];
      },
      explodeTerrain(x, y) {
        // Create a circular explosion in the terrain
        const explosionRadius = 20;
        for (let i = -explosionRadius; i <= explosionRadius; i++) {
          const pos = Math.floor(x) + i;
          if (pos >= 0 && pos < this.canvasWidth) {
            const distance = Math.sqrt(i * i);
            if (distance <= explosionRadius) {
              const impactDepth = Math.sqrt(explosionRadius * explosionRadius - distance * distance);
              this.terrain[pos] = Math.max(this.terrain[pos], y + impactDepth);
            }
          }
        }
        this.renderGame();
        this.wind = 0;//Math.floor(Math.random() * 100 - 50); 

      },
      renderGame() {
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

        // Draw the terrain
        this.drawTerrain(ctx);
  
        // Draw player 1's tank
        this.drawTank(ctx, this.player1);

        //Draw player names
        this.drawPlayerNames(ctx);

        //Draw player health
        this.drawPlayerHealth(ctx);

      },
      drawTerrain(ctx) {
        ctx.beginPath();
        ctx.moveTo(0, this.canvasHeight);
        for (let x = 0; x < this.terrain.length; x++) {
          ctx.lineTo(x, this.terrain[x]);
        }
        ctx.lineTo(this.canvasWidth, this.canvasHeight);
        ctx.closePath();
        ctx.fillStyle = "saddlebrown";
        ctx.fill();
      },

      onMouseDown(event) {
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = event.clientX - rect.left;
        this.mousePosition.y = event.clientY - rect.top;

        // Check if the click is within the aim circle
        if (this.isHovering) {
          this.isDragging = true; // Start dragging
          this.lineStopX = this.mousePosition.x; // Initialize line stop positions
          this.lineStopY = this.mousePosition.y;
        }
      },

      onMouseUp() {
        this.isDragging = false; // Stop dragging
      },

      onMouseMove(event) {
          const rect = this.$refs.gameCanvas.getBoundingClientRect();
          this.mousePosition.x = event.clientX - rect.left;
          this.mousePosition.y = event.clientY - rect.top;

          const dx = this.mousePosition.x - this.player1.x;
          const dy = this.mousePosition.y - this.player1.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          if (this.isDragging) {

            
            // Cap the power line's length to the circle radius
            const clampedDistance = Math.min(distance, this.aimCircleRadius);
            this.power = Math.round((clampedDistance / this.aimCircleRadius) * this.maxShotPower);
            
            // Update the line end positions
            const angle = Math.atan2(dy, dx);
            this.lineStopX = this.player1.x + clampedDistance * Math.cos(angle);
            this.lineStopY = this.player1.y + clampedDistance * Math.sin(angle);
            this.angle = -(angle * 180) / Math.PI;
          }

          // const dx = this.mousePosition.x - this.player1.x;
          // const dy = this.mousePosition.y - this.player1.y;
          // const distance = Math.sqrt(dx * dx + dy * dy);

          // Show the aiming UI if the mouse is within the aiming circle range
          this.isHovering = distance >= 1 && distance <= this.aimCircleRadius;

          if (this.isHovering) {
            // Calculate the angle between the tank and the mouse
            // if(!this.stopLine){
            //   this.angle = (Math.atan2(dy, dx) * 180) / Math.PI;
            // }
            this.drawAimCircle(this.player1);
          }
        

      },

      onMouseClick(event) {
        console.log("Clicked insideee the aim circle!"); // Debug message
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = event.clientX - rect.left;
        this.mousePosition.y = event.clientY - rect.top;

        const dx = this.mousePosition.x - this.player1.x;
        const dy = this.mousePosition.y - this.player1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Show the aiming UI if the mouse is within the aiming circle range
        this.isHovering = distance >= 1 && distance <= this.aimCircleRadius;

        if (this.isHovering) {
          this.angle = -(Math.atan2(dy, dx) * 180) / Math.PI;
          this.stopLine = true;
          this.stopLineX = this.mousePosition.x;
          this.stopLineY = this.mousePosition.y;
          this.drawAimCircle(this.player1);
        }
      },
      
      
      async drawTank(ctx, player) {
        ctx.save();

        this.player1.y = this.terrain[Math.floor(player.x)] - player.size / 2;

        // ctx.translate(player.x, this.player1.y - player.size / 2)

        // Fetch the SVG from the FastAPI endpoint
        const response = await axios.get(`/player/0/tank`, {
          responseType: 'blob'
        });

        const blob = await response.data;
        const url = URL.createObjectURL(blob);

        // Create an image from the fetched SVG
        const img = new Image();
        img.src = url;

        // Define the desired size for the tank
        const tankWidth = 50; // Adjust the width to suit your needs
        const tankHeight = 50; // Adjust the height to suit your needs

        // Once the image is loaded, draw it on the canvas
        img.onload = () => {
          ctx.drawImage(img, player.x - tankWidth / 2, this.player1.y - tankHeight / 2, tankWidth, tankHeight);

          // Draw the gun (turret)
          ctx.translate(player.x, this.player1.y - tankHeight / 2); // Adjust for tank position
          ctx.rotate((-this.angle * Math.PI) / 180); // Rotate based on angle
          ctx.restore();
        };
        // // Load the tank image
        // const img = document.getElementById('tankImage');

        // // Define the desired size for the tank
        // const tankWidth = img.width / 2; // Change this value to adjust the width
        // const tankHeight = img.height / 2; // Change this value to adjust the height

        // // Draw the tank image at the player's position with the specified size
        // ctx.drawImage(img, player.x - tankWidth / 2, this.player1.y - tankHeight / 2, tankWidth, tankHeight); // Center the tank image

        // // Draw the gun (turret)
        // ctx.translate(player.x, this.player1.y - img.height / 2); // Adjust for tank position
        // ctx.rotate((-this.angle * Math.PI) / 180); // Rotate based on angle
        // ctx.restore();
      },

      drawAimCircle(player){

        // Get the canvas context
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext('2d');
        this.renderGame();
        ctx.save();

        const x = player.x;
        const y = player.y;

        ctx.beginPath();
        ctx.arc(x, y, this.aimCircleRadius, 0, 2 * Math.PI);
        // Fill the circle with a semi-transparent color
        ctx.fillStyle = 'rgba(128, 128, 128, 0.5)';
        ctx.fill();  // Fill first to apply transparency correctly

        // Stroke the border of the circle
        ctx.strokeStyle = "black";
        ctx.stroke();

        // Draw the power/shot line
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(this.lineStopX, this.lineStopY); // Use the updated stop positions
        ctx.strokeStyle = "red";
        ctx.stroke();
        ctx.restore();

      },
    },
  };
  </script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

canvas {
  font-family: 'Montserrat', sans-serif;
}
</style>
