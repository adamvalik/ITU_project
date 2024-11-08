<template>
  <div :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`}">
    <div>
      <div class="h-44 bg-opacity-80 bg-neutral-900 text-white items-center justify-center flex flex-rows space-x-8">

        <div class="flex flex-col space-y-1 w-1/3">
          <div>
            <button
              mouseover="showFireHelp"
              @mouseleave="hideFireHelp"
              @click="fireMissile"
              class="h-16 w-full bg-blue-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-blue-400 font-bold text-4xl">
              WEAPON SELECTOR
            </button>
          </div>

          <div>
            <button
              class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">SMALL MISSILE</div>
                <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                <div class="text-black font-bold text-3xl">{{ player1.ammunition[0].count }}</div>
              </div>

            </button>
          </div>
        </div>

        <div class="relative w-1/4">
          <button
              @mouseover="showFireHelp"
              @mouseleave="hideFireHelp"
              @click="fireMissile"
              class="py-16 w-full bg-red-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-red-400 font-bold text-4xl">
              FIRE
            <span v-if="fireHelpVisible" class="absolute top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-2xl">
              Click to fire!
            </span>
          </button>
        </div>

        <!-- Row flex for money, time and so on -->
        <div class ="flex flex-rows space-x-8 w-1/3 mt-4">

          <div class ="flex flex-col space-y-4">
            <div class="font-bold text-white text-2xl">
              <h1>{{ player1.time }} (s)</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/time_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2">
            <div class="font-bold text-white text-2xl">
              <h1>{{ player1.money }}$</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/money_bag_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2, items-center">
            <div class="font-bold text-white text-2xl">
              <h1>{{ player1.fuel }}/{{ player1.fuelMax }}</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/fuel_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-3">
            <div class="font-bold text-white text-2xl">
              <h1>{{ player1.wins }}win</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/trophy_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class="relative mb-16">
            <div class="w-20 h-20" style="background: url('assets/pause_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

        </div>
      </div>

    </div>

    <div>
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
    </div>
    <div v-if="gameOver" class="absolute inset-0 flex flex-col space-y-2 items-center justify-center bg-black bg-opacity-50">
        <h1 class="text-4xl font-bold">Game Over!</h1>
        <button @click="backToMenu" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl mt-4 justify-center items-center">
          Back to Menu
        </button>

    </div>
  </div>
</template>

  <script>
  //import axios from 'axios';
  export default {
    props: {
      gameWidth: Number,
      gameHeight: Number,
      scaleFactor: Number,
    },
    data() {
      return {
        canvasWidth: this.gameWidth,
        canvasHeight: this.gameHeight - 176,
        terrain: [],
        player1: {
          x: 120,
          y: 140,
          size: 40,
          angle: 45,
          power: 50,
          tankColor: "green",
          name: "DJ Khaled",
          health: 100,
          ammunition: [
            {
              name: "smallMissile",
              count: 20,
              damage: 20,
              radius: 30,
              cost: 200,
            },
          ],
          wins: 1,
          money: 4000,
          fuel: 100,
          fuelMax: 250,
          time: 40,

        },
        mousePosition: {
          x: 0,
          y: 0,
        },
        isHovering: false,
        aimCircleRadius: 200,
        maxShotPower: 100,
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
      };
    },
    mounted() {
      //this.wind = 0;//Math.floor(Math.random() * 100 - 50);
      //this.player1.tankColor = "green"; //this.$route.query.color;
      this.startTimer();
      this.generateTerrain();
      this.renderGame();
      window.addEventListener('keydown', this.onKeyPressed);
    },
    methods: {
      showFireHelp() {
        this.fireHelpVisible = true;
      },
      hideFireHelp() {
        this.fireHelpVisible = false;
      },

      backToMenu() {
        this.$router.push('/');
      },

      drawPlayerNames(ctx) {
        ctx.save();

        //size of rectangles for healthbars
        const player1X = 10 + 200 / 2;
        const player2X = this.canvasWidth - 210 + 200 / 2;

        ctx.font = "28px Montserrat";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(this.player1.name, player1X, 30);
        ctx.fillText("Player 2", player2X, 30);
        ctx.restore();
      },

      drawPlayerHealth(ctx){
        ctx.save();

        ctx.fillStyle = 'black'; // White color
        ctx.fillRect(10, 50, 200, 40);

        ctx.fillRect(this.canvasWidth - 210, 50, 200, 40);

        // Draw red fill
        ctx.fillStyle = '#FF0000'; // Red color
        ctx.fillRect(10, 50, 180, 40); // Adjusted for border thickness
        ctx.fillRect(this.canvasWidth - 210, 50, 180, 40); // Adjusted for border thickness

        //Draw outline
        ctx.strokeStyle = 'gray';
        ctx.lineWidth = 5; // Border width
        ctx.strokeRect(10, 50, 200, 40);
        ctx.strokeRect(this.canvasWidth - 210, 50, 200, 40);

        ctx.fillStyle = '#000000'; // Text color
        ctx.font = '20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('80/100', 110, 70);
        ctx.fillText('80/100', this.canvasWidth - 110, 70);

        ctx.restore();
      },

      drawWind(ctx){
        ctx.save();

        ctx.fillStyle = 'black'; // Text color
        ctx.font = 'bold 20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Wind: ', this.canvasWidth/2, 20);
        ctx.fillText(this.wind, this.canvasWidth/2 + 40, 20);

        ctx.restore();
      },

      drawAnglePower(ctx) {
        ctx.save();
        ctx.fillStyle = "black";
        ctx.font = "bold 20px Montserrat";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        // ctx.fillText(`Angle: ${this.angle}°`, this.player1.x, this.player1.y - 50);
        // ctx.fillText(`Power: ${this.power}`, this.player1.x + 10, this.player1.y - 50);
        ctx.fillText(`${Math.round(this.angle)}°,`, this.player1.x - 10, this.player1.y - 180);
        ctx.fillText(this.power, this.player1.x + 26, this.player1.y - 180);
        ctx.restore();
      },

      startTimer() {
        setInterval(() => {
          if (this.player1.time > 0) {
            this.player1.time--;
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
        const ammunition = this.player1.ammunition[0].count;
        if(ammunition <= 0){
          return;
        }
        this.player1.ammunition[0].count--;
        const startX = this.player1.x;
        const startY = this.player1.y - 15; //this.terrain[Math.floor(player.x)] - player.size / 2
        const controlX = startX + Math.cos(this.angle * (Math.PI / 180)) * this.power * 12 + this.wind * 4;
        const controlY = startY - Math.sin(this.angle * (Math.PI / 180)) * this.power * 12;
        const endX = controlX + Math.cos(this.angle * (Math.PI / 180)) * this.power * 12 + this.wind * 8;
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
        const explosionRadius = this.player1.ammunition[0].radius;
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
        this.wind = 0;// Math.floor(Math.random() * 100 - 50);

      },
      renderGame() {
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

        // Draw the terrain
        // this.drawTerrain(ctx);

        // Draw player 1's tank
        // this.drawTank(ctx, this.player1);

        // //Draw wind
        // this.drawWind(ctx);

        // //Draw player names
        // this.drawPlayerNames(ctx);

        // //Draw player health
        // this.drawPlayerHealth(ctx);

        // Draw the aiming circle
        this.drawAimCircle(this.player1);

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

      onKeyPressed(event){
        if(event.key === 'ArrowRight'){

          if(this.player1.fuel > 0 && this.player1.x <  this.canvasWidth - 5){
            this.player1.fuel -= 5;
            this.player1.x += 5;
            this.lineStopX += 5;
          }
        } else if(event.key === 'ArrowLeft'){
          if(this.player1.fuel > 0 && this.player1.x > 5){
            this.player1.fuel -= 5;
            this.player1.x -= 5;
            this.lineStopX -= 5;
          }
        }
        this.renderGame();
      },

      onMouseDown(event) {
        console.log(event.clientX);
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
        this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

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
          this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
          this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

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
            //Calculate the angle between the tank and the mouse
            if(!this.stopLine && this.isDragging){
              this.angle = -(Math.atan2(dy, dx) * 180) / Math.PI;
            }
            this.drawAimCircle(this.player1);
          }
      },

      onMouseClick(event) {
        console.log("Clicked insideee the aim circle!"); // Debug message
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
        this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

        const dx = this.mousePosition.x - this.player1.x;
        const dy = this.mousePosition.y - this.player1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Show the aiming UI if the mouse is within the aiming circle range
        this.isHovering = distance >= 1 && distance <= this.aimCircleRadius;

        if (this.isHovering) {
          this.angle = -(Math.atan2(dy, dx) * 180) / Math.PI;
          this.power = Math.round((distance / this.aimCircleRadius) * this.maxShotPower);
          this.stopLine = true;
          // this.stopLineX = this.mousePosition.x;
          // this.stopLineY = this.mousePosition.y;
          this.drawAimCircle(this.player1);
        }
      },


      drawTank(ctx, player) {

        ctx.save();
        this.player1.y = this.terrain[Math.floor(player.x)] - player.size / 2;
        ctx.translate(player.x, this.player1.y);

        // Draw the tank body
        ctx.fillStyle = this.player1.tankColor;
        ctx.fillRect(-player.size / 2, -player.size / 4, player.size, player.size / 2);

        // Draw the tank turret
        const turretLength = player.size * 0.7;
        ctx.translate(0, -player.size / 7);
        ctx.rotate((-this.angle * Math.PI) / 180);
        ctx.fillStyle = this.player1.tankColor;
        ctx.fillRect(0, -5, turretLength, 10);

        ctx.restore();
      },

      drawAimCircle(player){

        // Get the canvas context
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

        // Draw the terrain
        this.drawTerrain(ctx);

        // Draw player 1's tank
        this.drawTank(ctx, this.player1);

        //Draw player names
        this.drawPlayerNames(ctx);

        //Draw player health
        this.drawPlayerHealth(ctx);

        this.drawWind(ctx);

        this.drawAnglePower(ctx);

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

      },
    },
    beforeUnmount() {
      window.removeEventListener('keydown', this.onKeyPressed);
    },
  };
  </script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

canvas {
  font-family: 'Montserrat', sans-serif;
}
</style>
