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
                <div class="text-black font-bold text-3xl">{{ player1.ammunitionCount[0] }}</div>
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

          <div class ="flex flex-col space-y-4 items-center">
            <div v-if="useTimer" class="font-bold text-white text-2xl">
              <h1>{{ timePerRound }} (s)</h1>
            </div>
            <div v-else class="font-bold text-white text-2xl">
              <h1>Inf</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/time_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2 items-center">
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

          <div class ="flex flex-col space-y-3 items-center">
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

  import axios from 'axios';
  export default {
    props: {
      gameWidth: Number,
      gameHeight: Number,
      scaleFactor: Number,
    },
    data() {
      return {
        //Default canvas size
        canvasWidth: this.gameWidth,
        canvasHeight: this.gameHeight - 176,
        
        //Map data
        terrain: [],

        //Player data
        player1: {
          id: 0,
          xCord: 0,
          yCord: 0,
          angle: 0,
          power: 0,
          color: "",
          name: "",
          health: 0,
          ammunitionCount: 0,
          wins: 0,
          money: 0,
          fuel: 0,
          fuelMax: 0,
          time: 0,
        },

        //Mouse position
        mousePosition: {
          x: 0,
          y: 0,
        },

        //Game data
        useTimer: false,
        timePerRound: 0,
        gameOver: false,
        wind: 0,

        //Aim circle data
        toggleHovering: false,
        toggleDragging: false,
        aimCircleRadius: 200,
        aimLaserXCord: 200,
        aimLaserYCord: 400,
        angle: 45,
        power: 50,

        //Missile data
        missile: null,

        //Fire help visibility
        fireHelpVisible: false,

        //
        isPractice: true,
        practiceTarget: {
          name: "",
          xCord: 0,
          yCord: 0,
          health: 0,
          color: "",
        }
      };
    },
    mounted() {
      this.checkPractice();
      this.loadPlayerData();
      this.loadGameData();
      window.addEventListener('keydown', this.onKeyPressed);
    },
    methods: {
      async checkPractice() {

        if(!this.isPractice){
          return;
        }

        await axios.get('http://localhost:8000/practice-target')
          .then((response) => {
            this.practiceTarget = response.data;
            this.drawGame();
          })
          .catch((error) => {
            console.error(error);
          });
      },

      async loadPlayerData() {
        await axios.get('http://localhost:8000/players/1')
          .then((response) => {
            this.player1 = response.data;
            this.generateTerrain();
            this.drawGame();
          })
          .catch((error) => {
            console.error(error);
          });
      },

    async loadGameData() {
      await axios.get('http://localhost:8000/game')
        .then((response) => {
          this.useTimer = response.data.isTimer;
          this.timePerRound = response.data.timePerTurn;
          this.wind = response.data.wind;
          this.validateTimer();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    validateTimer() {

      if(!this.useTimer){
        return;
      }

      setInterval(() => {
        if(this.timePerRound > 0) {
          this.timePerRound--;
        } else {
          this.gameOver = true;
        }
      }, 1000);
    },

      showFireHelp() {
        this.fireHelpVisible = true;
      },
      hideFireHelp() {
        this.fireHelpVisible = false;
      },

      backToMenu() {
        this.$router.push('/');
      },


      drawPracticeTarget(ctx) {
        ctx.save();
    
        this.practiceTarget.yCord = this.terrain[Math.floor(this.practiceTarget.xCord)] - 40 / 2;
        ctx.translate(this.practiceTarget.xCord, this.practiceTarget.yCord);

        //Color for outline
        ctx.strokeStyle = "black";

        // Draw the tank body
        ctx.fillStyle = this.practiceTarget.color;
        ctx.fillRect(-40 / 2, -40 / 4, 40, 40 / 2);
        ctx.strokeRect(-40 / 2, -40 / 4, 40, 40 / 2);

        // Draw the tank turret
        const turretLength = 40 * 0.7;
        ctx.translate(0, -40 / 7);
        ctx.rotate((-150 * Math.PI) / 180);
        ctx.fillStyle = this.practiceTarget.color;
        ctx.fillRect(0, -5, turretLength, 10);
        ctx.strokeRect(0, -5, turretLength, 10);
        ctx.restore();
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
        if(this.isPractice){
          ctx.fillText(this.practiceTarget.name, player2X, 30);
        } else {
          ctx.fillText("Target", player2X, 30);
        }
        ctx.restore();
      },

      drawPlayerHealth(ctx){
        ctx.save();

        // Draw black fill
        ctx.fillStyle = 'black';
        ctx.fillRect(10, 50, 200, 40);
        ctx.fillRect(this.canvasWidth - 210, 50, 200, 40);

        // Draw red fill
        ctx.fillStyle = '#FF0000'; 
        const healthBarWidth = this.player1.health * 2;
        ctx.fillRect(10, 50, healthBarWidth, 40);

        if(this.isPractice){
          const practiceHealthBarWidth = this.practiceTarget.health * 2;
          ctx.fillRect(this.canvasWidth - 210, 50, practiceHealthBarWidth, 40);
        } else {
          ctx.fillRect(this.canvasWidth - 210, 50, 180, 40); 
        }

        //Draw outline
        ctx.strokeStyle = 'gray';
        ctx.lineWidth = 5; // Border width
        ctx.strokeRect(10, 50, 200, 40);
        ctx.strokeRect(this.canvasWidth - 210, 50, 200, 40);

        ctx.fillStyle = '#FFFFFF'; // Text color
        ctx.font = '20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${this.player1.health}/100`, 110, 70);

        if(this.isPractice){
          ctx.fillText(`${this.practiceTarget.health}/100`, this.canvasWidth - 110, 70);
        } else {
          ctx.fillText('80/100', this.canvasWidth - 110, 70);
        }

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
        ctx.fillStyle = 'black';
        ctx.font = 'bold 20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${Math.round(this.angle)}°,`, this.player1.xCord - 10, this.player1.yCord - 180);
        ctx.fillText(this.power, this.player1.xCord + 26, this.player1.yCord - 180);
        ctx.restore();
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
        const ammunition = this.player1.ammunitionCount[0];
        if(ammunition <= 0){
          return;
        }
        this.player1.ammunitionCount[0]--;
        const startX = this.player1.xCord;
        const startY = this.player1.yCord - 15; //this.terrain[Math.floor(player.x)] - player.size / 2
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

        this.drawGame();

        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext("2d");
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();

        requestAnimationFrame(this.animateMissile);
      },
      checkTerrainCollision(x, y) {
        //Check if the missile hit the terrain
        return y >= this.terrain[Math.floor(x)];
      },
      explodeTerrain(x, y) {
        //Create a circular explosion in the terrain
        const explosionRadius = 30;
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
        this.drawGame();
        //this.wind = 0;// Math.floor(Math.random() * 100 - 50);
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

          if(this.player1.fuel > 0 && this.player1.xCord <  this.canvasWidth - 5){
            this.player1.fuel -= 5;
            this.player1.xCord += 5;
            this.aimLaserXCord += 5;
          }
        } else if(event.key === 'ArrowLeft'){
          if(this.player1.fuel > 0 && this.player1.xCord > 5){
            this.player1.fuel -= 5;
            this.player1.xCord -= 5;
            this.aimLaserXCord -= 5;
          }
        }
        this.drawGame();
      },

      onMouseDown(event) {
        //Obtain mousePosition relative to the canvas
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
        this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

        //Check if the click is within the aim circle
        if (this.toggleHovering) {

          //Start dragging in the circle
          this.toggleDragging = true; 

          //Update aiming line start positions
          this.aimLaserXCord = this.mousePosition.x; 
          this.aimLaserYCord = this.mousePosition.y;
        }
      },

      onMouseUp() {

        //Dragging is stopped
        this.toggleDragging = false; 
      },

      onMouseMove(event) {

          //Obtain mousePosition relative to the canvas
          const rect = this.$refs.gameCanvas.getBoundingClientRect();
          this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
          this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

          //Calculate the distance between the tank and the mouse
          const dx = this.mousePosition.x - this.player1.xCord;
          const dy = this.mousePosition.y - this.player1.yCord;
          const distance = Math.sqrt(dx * dx + dy * dy);

          //Toggle hovering if the mouse is within the aim circle range
          this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;
          if(!this.toggleHovering){
            return;
          }

          //Dragging is enabled
          if (this.toggleDragging) {

            //Update the power value
            this.power = Math.round((distance / this.aimCircleRadius) * 100);

            //Update the laser line stop positions and angle
            const angle = Math.atan2(dy, dx);
            this.aimLaserXCord = this.player1.xCord + distance * Math.cos(angle);
            this.aimLaserYCord = this.player1.yCord + distance * Math.sin(angle);
            this.angle = -(angle * 180) / Math.PI;
          }

          //Redraw the game with updated values
          this.drawGame();
      },

      onMouseClick(event) {

        //Obtain mousePosition relative to the canvas
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
        this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

        //Calculate the distance between the tank and the mouse
        const dx = this.mousePosition.x - this.player1.xCord;
        const dy = this.mousePosition.y - this.player1.yCord;
        const distance = Math.sqrt(dx * dx + dy * dy);

        //Toggle hovering if the mouse is within the aim circle range
        this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;

        if (this.toggleHovering) {

          //Update the angle and power values
          this.angle = -(Math.atan2(dy, dx) * 180) / Math.PI;
          this.power = Math.round((distance / this.aimCircleRadius) * 100);

          //Redraw the game with updated values
          this.drawGame();
        }
      },

      drawTank(ctx) {

        ctx.save();
        console.log(this.player1.xCord, this.player1.yCord, 40);
        this.player1.yCord = this.terrain[Math.floor(this.player1.xCord)] - 40 / 2;
        ctx.translate(this.player1.xCord, this.player1.yCord);

        //Color for outline
        ctx.strokeStyle = "black";


        // Draw the tank body
        ctx.fillStyle = this.player1.color;
        ctx.fillRect(-40 / 2, -40 / 4, 40, 40 / 2);
        ctx.strokeRect(-40 / 2, -40 / 4, 40, 40 / 2);

        // Draw the tank turret
        const turretLength = 40 * 0.7;
        ctx.translate(0, -40 / 7);
        ctx.rotate((-this.angle * Math.PI) / 180);
        ctx.fillStyle = this.player1.color;
        ctx.fillRect(0, -5, turretLength, 10);
        ctx.strokeRect(0, -5, turretLength, 10);

        ctx.restore();
      },

      drawAimCircle(ctx) {
        ctx.beginPath();
        ctx.arc(this.player1.xCord, this.player1.yCord, this.aimCircleRadius, 0, 2 * Math.PI);
        // Fill the circle with a semi-transparent color
        ctx.fillStyle = 'rgba(128, 128, 128, 0.5)';
        ctx.fill();  // Fill first to apply transparency correctly

        // Stroke the border of the circle
        ctx.strokeStyle = "black";
        ctx.stroke();

        // Draw the power/shot line
        ctx.beginPath();
        ctx.moveTo(this.player1.xCord, this.player1.yCord);
        ctx.lineTo(this.aimLaserXCord, this.aimLaserYCord); // Use the updated stop positions
        ctx.strokeStyle = "red";
        ctx.stroke();
      },

      drawGame(){

        // Get the canvas context
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

        // Draw the terrain
        this.drawTerrain(ctx);

        // Draw player 1's tank
        this.drawTank(ctx, this.player1);

        //Draw practice target
        if(this.isPractice){
          this.drawPracticeTarget(ctx);
        }

        //Draw player names
        this.drawPlayerNames(ctx);

        //Draw player health
        this.drawPlayerHealth(ctx);

        //Draw wind
        this.drawWind(ctx);

        //Draw angle and power values in the circle
        this.drawAnglePower(ctx);

        // Draw the aim circle
        this.drawAimCircle(ctx);

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
