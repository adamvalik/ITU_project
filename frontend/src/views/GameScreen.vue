<template>
  <div :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`, backgroundColor: '#D5EFF4'}">
    <div>
      <div class="h-44 bg-opacity-80 bg-neutral-900 text-white items-center justify-center flex flex-rows space-x-8">

        <div class="flex flex-col space-y-1 w-1/3 relative">
          <div>
            <button
              @mouseover="showSelectorHelp"
              @mouseleave="hideSelectorHelp"
              @click="toggleWeaponMenu"
              class="h-16 w-full bg-blue-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-blue-400 font-bold text-4xl relative">
              WEAPON SELECTOR
              <span v-if="selectorHelpVisible" class="absolute top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-2xl">
              Click to select weapon!
            </span>
            </button>
          </div>

          <div v-if="!toggleDropDownMenu && activeMissile">
            <button
              class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">{{ activeMissile.name }}</div>
                <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                <div class="text-black font-bold text-3xl">{{ currentPlayer.ammunitionCount[this.activeMissileId] }}</div>
              </div>
            </button>
          </div>

          <div v-if="toggleDropDownMenu" class="absolute top-full mt-2 bg-gray-600 border-4 border-gray-700 space-y-2">
            <button 
              v-for="(missile) in currentPlayerMissiles" 
              :key="missile.id"
              @click="selectMissile(missile.id)"
              class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400"
            >
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">{{ missile.name }}</div>
                <div class="w-8 h-8" :style="{ background: `url(${missile.picture}) no-repeat center center`, backgroundSize: 'cover' }"></div>
                <div class="text-black font-bold text-3xl">{{ currentPlayer.ammunitionCount[missile.id] }}</div>
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
              <h1>{{ currentPlayer.money }}$</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/money_bag_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2, items-center">
            <div class="font-bold text-white text-2xl">
              <h1>{{ currentPlayer.fuel }}/{{ player1.fuelMax }}</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/fuel_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-3 items-center">
            <div class="font-bold text-white text-2xl">
              <h1>{{ currentPlayer.wins }}win</h1>
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
        <h1 class="text-4xl font-bold">You won!</h1>
        <button @click="backToMenu" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl mt-4 justify-center items-center">
          Back to Menu
        </button>
    </div>
  </div>
</template>

  <script>
import axios from 'axios';
import apiClient from '@/api';

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
        terrainType: "",

        //Player 1 data
        player1: {
          id: 0,
          name: "",
          tankType: 0,
          color: "",
          armorSkill: 0,
          powerSkill: 0,
          speedSkill: 0,
          skillPoints: 0,
          wins: 0,
          money: 0,
          fuel: 0,
          fuelMax: 0,
          health: 0,
          ammunitionCount: 0,
          xCord: 0,
          yCord: 0,
        },

        //Player data
        player2: {
          id: 0,
          name: "",
          tankType: 0,
          color: "",
          armorSkill: 0,
          powerSkill: 0,
          speedSkill: 0,
          skillPoints: 0,
          wins: 0,
          money: 0,
          fuel: 0,
          fuelMax: 0,
          health: 0,
          ammunitionCount: 0,
          xCord: 0,
          yCord: 0,
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
        p1Turn: true,

        //Aim circle data
        toggleHovering: false,
        toggleDragging: false,
        aimCircleRadius: 200,
        p1Circle: {
          angle: 45,
          power: 50,
          aimLaserXCord: 0,
          aimLaserYCord: 0,
        },
        p2Circle: {
          angle: 45,
          power: 50,
          aimLaserXCord: 0,
          aimLaserYCord: 0,
        },

        //Missile trajectory data
        missileTrajectory: [],
        missiles: [],
        activeMissileId: 0,

        //Response
        responseGameOver: false,
        responseHitPlayer: false,
        responseMoney: 0,
        newterrain: [],
        newTargetHealth: 0,

        //Fire help visibility
        fireHelpVisible: false,
        selectorHelpVisible: false,
        toggleDropDownMenu: false,
        toggleDisableFire: false,
      };
    },
    computed: {
      currentPlayer() {
        return this.p1Turn ? this.player1 : this.player2;
      },

      nextPlayer() {
        return this.p1Turn ? this.player2 : this.player1;
      },

      activeMissile() {
        return this.missiles[this.activeMissileId];
      },

      currentAimCircle() {
        return this.p1Turn ? this.p1Circle : this.p2Circle;
      },

      currentPlayerMissiles() {
        const displayedMissiles = [];
        for (let i = 0; i < this.player1.ammunitionCount.length; i++) {
          if (this.currentPlayer.ammunitionCount[i] >= 0) {
            displayedMissiles.push(this.missiles[i]);
          }
        }
        return displayedMissiles;
      }
    },
    mounted() {
      this.loadMissiles();
      this.generateTerrain();
      this.loadPlayerData();
      this.loadGameData();
      window.addEventListener('keydown', this.onKeyPressed);
    },
    watch: {
      async gameOver(newValue) {
        if (newValue) {
          try {
            await apiClient.post('/players/1/skillPointsInc');
            await apiClient.post('/players/2/skillPointsInc');
          } catch (error) {
            console.error(error);
          }
          this.$router.push('/shop');
        }
      }
    },
    methods: {
      toggleWeaponMenu() {
        this.toggleDropDownMenu = !this.toggleDropDownMenu;
      },

      async loadMissiles() {
        await apiClient.get('/missiles')
          .then((response) => {
            this.missiles = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },

      selectMissile(missileId) {
        this.activeMissileId = missileId;
        this.toggleDropDownMenu = false;
      },

      async loadPlayerData() {
        await axios.get('http://localhost:8000/players/1')
          .then((response) => {
            this.player1 = response.data;
            console.log(response.data);
          })
          .catch((error) => {
            console.error(error);
          });

        await axios.get('http://localhost:8000/players/2')
          .then((response) => {
            this.player2 = response.data;
            console.log(response.data);
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

      showSelectorHelp() {
        this.selectorHelpVisible = true;
      },

      hideSelectorHelp() {
        this.selectorHelpVisible = false;
      },

      backToMenu() {
        this.$router.push('/');
      },

      calculateLaserPos(playerAimCircle, player) {
        const distance = (playerAimCircle.power / 100) * this.aimCircleRadius;
        let angleInRadians;
        if (this.p1Turn) {
            angleInRadians = (-playerAimCircle.angle * Math.PI) / 180;
        } else {
            angleInRadians = (-(180 - playerAimCircle.angle) * Math.PI) / 180;
        }

        // Calculate laser position
        playerAimCircle.aimLaserXCord = player.xCord + distance * Math.cos(angleInRadians);
        playerAimCircle.aimLaserYCord = player.yCord + distance * Math.sin(angleInRadians);
      },

      drawPlayerNames(ctx) {
        ctx.save();
        //size of rectangles for healthbars
        const player1X = 10 + 200 / 2;
        const player2X = this.canvasWidth - 210 + 200 / 2;

        ctx.font = "28px sans-serif";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(this.player1.name, player1X, 30);
        ctx.fillText(this.player2.name, player2X, 30);
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
        const player1HealthWidth = this.player1.health * 2;
        ctx.fillRect(10, 50, player1HealthWidth, 40);


        const player2HeathWidth = this.player2.health * 2;
        ctx.fillRect(this.canvasWidth - 210, 50, player2HeathWidth, 40);

        //Draw outline
        ctx.strokeStyle = 'gray';
        ctx.lineWidth = 5; // Border width
        ctx.strokeRect(10, 50, 200, 40);
        ctx.strokeRect(this.canvasWidth - 210, 50, 200, 40);

        ctx.fillStyle = '#FFFFFF'; // Text color
        ctx.font = '20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${this.player1.health}/100`, 110, 70);
        ctx.fillText(`${this.player2.health}/100`, this.canvasWidth - 110, 70);

        ctx.restore();
      },

      drawWind(ctx){
        ctx.save();

        ctx.fillStyle = 'black'; // Text color
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Wind: ', this.canvasWidth/2, 20);
        ctx.fillText(this.wind, this.canvasWidth/2 + 40, 20);

        ctx.restore();
      },

      drawAnglePower(ctx, playerAimCircle, player) {
        ctx.save();
        ctx.fillStyle = 'black';
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${Math.round(playerAimCircle.angle)}°,`, player.xCord - 10, player.yCord - 180);
        ctx.fillText(playerAimCircle.power, player.xCord + 26, player.yCord - 180);
        ctx.restore();
      },

      async generateTerrain() {
        await axios.get('http://localhost:8000/generate-terrain', {
          params: {
            canvasWidth: this.canvasWidth,
            canvasHeight: this.canvasHeight,
          }
        })
        .then((response) => {
          this.terrain = response.data.data;
          this.terrainType = response.data.type;
        })
        .catch((error) => {
          console.error(error);
        });
      },

      async fireMissile() {

        if(this.toggleDisableFire){
          return;
        }
        this.toggleDisableFire = true;

        await axios.post('http://localhost:8000/save-current-player-data', {
          player1: this.player1,
          player2: this.player2,
        })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });

        const ammunition = this.currentPlayer.ammunitionCount[this.activeMissileId];
        if(ammunition <= 0){
          this.toggleDisableFire = false;
          return;
        }

        await axios.post('http://localhost:8000/compute-missile-data', {
          canvasWidth: this.canvasWidth,
          canvasHeight: this.canvasHeight,
          playerId: this.currentPlayer.id,
          terrain: this.terrain,
          angle: this.currentAimCircle.angle,
          power: this.currentAimCircle.power,
          wind: this.wind,
          weaponSelected: this.activeMissile.id,
        })
        .then((response) => {
          console.log(response);
          this.currentPlayer.ammunitionCount[this.activeMissileId] = response.data.ammunitionCount;
          this.missileTrajectory = response.data.missileTrajectory;
          this.newTerrain = response.data.newTerrain;
          this.responseGameOver = response.data.gameOver;
          this.newTargetHealth = response.data.targetHealth;
          this.responseHitPlayer = response.data.hitPlayer;
          this.responseMoney = response.data.playerMoney;
        })
        .catch((error) => {
          console.error(error);
        });

        if(this.missileTrajectory != null){
          this.animateMissile();
        }

      },
      animateMissile() {

        const [x, y] = this.missileTrajectory.shift();

        this.drawGame();

        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext("2d");
        ctx.beginPath();
        ctx.arc(x, y, this.missiles[this.activeMissileId].damage / 4, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();

        if(this.missileTrajectory.length > 0){
          requestAnimationFrame(this.animateMissile);
        } else {

          this.terrain = this.newTerrain;

          if(this.responseHitPlayer){
            this.nextPlayer.health = this.newTargetHealth;
            this.currentPlayer.money += this.responseMoney;

          }
          if(this.responseGameOver){
            this.gameOver = true;
          }
          this.toggleDisableFire = false;
          this.p1Turn = !this.p1Turn;
          this.activeMissileId = 0;
          this.drawGame();
        }
      },
      drawTerrain(ctx) {
        ctx.beginPath();
        ctx.moveTo(0, this.canvasHeight);
        for (let x = 0; x < this.terrain.length; x++) {
          ctx.lineTo(x, this.terrain[x]);
        }
        ctx.lineTo(this.canvasWidth, this.canvasHeight);
        ctx.closePath();
        if(this.terrainType === "mud"){
          // ctx.fillStyle = "saddlebrown";
          ctx.fillStyle = "#0D8747";
        } else {
          ctx.fillStyle = "green";
          console.log(this.terrain.type);
        }

        ctx.fill();
      },

      onKeyPressed(event){
        if(event.key === 'd'){

          if(this.p1Turn){
            if(this.player1.fuel > 0 && this.player1.xCord <  this.canvasWidth - 25){
              this.player1.fuel -= 5;
              this.player1.xCord += 5;
              this.p1Circle.aimLaserXCord += 5;
            }
          } else {
            if(this.player2.fuel > 0 && this.player2.xCord <  this.canvasWidth - 25){
              this.player2.fuel -= 5;
              this.player2.xCord += 5;
              this.p2Circle.aimLaserXCord += 5;
            }
          }
        } else if(event.key === 'a'){

          if(this.p1Turn){
            if(this.player1.fuel > 0 && this.player1.xCord > 25){
              this.player1.fuel -= 5;
              this.player1.xCord -= 5;
              this.p1Circle.aimLaserXCord -= 5;
            }
          } else {
            if(this.player2.fuel > 0 && this.player2.xCord > 25){
              this.player2.fuel -= 5;
              this.player2.xCord -= 5;
              this.p2Circle.aimLaserXCord -= 5;
            }
          }
        } else if(event.key === 'ArrowRight'){
          if(this.p1Turn){
            this.p1Circle.power = Math.min(100, this.p1Circle.power + 1);
          } else {
            this.p2Circle.power = Math.min(100, this.p2Circle.power + 1);
          }
        } else if(event.key === 'ArrowLeft'){
          if(this.p1Turn){
            this.p1Circle.power = Math.max(1, this.p1Circle.power - 1);
          } else {
            this.p2Circle.power = Math.max(1, this.p2Circle.power - 1);
          }
        } else if(event.key === 'ArrowUp'){
          if(this.p1Turn){
            this.p1Circle.angle += 1;
          } else {
            this.p2Circle.angle += 1;
          }
        } else if(event.key === 'ArrowDown'){
          if(this.p1Turn){
            this.p1Circle.angle -= 1;
          } else {
            this.p2Circle.angle -= 1;
          }
        } else if(event.key === ' '){
          this.fireMissile();
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
          let dx, dy;
          if(this.p1Turn){
            dx = this.mousePosition.x - this.player1.xCord;
            dy = this.mousePosition.y - this.player1.yCord;
          } else {
            dx = this.mousePosition.x - this.player2.xCord;
            dy = this.mousePosition.y - this.player2.yCord;
          }
          const distance = Math.sqrt(dx * dx + dy * dy);

          //Toggle hovering if the mouse is within the aim circle range
          this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;
          if(!this.toggleHovering){
            return;
          }

          //Dragging is enabled
          if (this.toggleDragging) {

            //Update the power value
            if(this.p1Turn){
              this.p1Circle.power = Math.round((distance / this.aimCircleRadius) * 100);
              this.p1Circle.angle = -(Math.atan2(dy, dx) * 180) / Math.PI;
            } else {
              this.p2Circle.power = Math.round((distance / this.aimCircleRadius) * 100);
              let p2Angle = 180 - (-(Math.atan2(dy, dx) * 180) / Math.PI);
              if (p2Angle > 180) {
                p2Angle -= 360;
              }
              this.p2Circle.angle = p2Angle;
            }
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
        let dx, dy;
          if(this.p1Turn){
            dx = this.mousePosition.x - this.player1.xCord;
            dy = this.mousePosition.y - this.player1.yCord;
          } else {
            dx = this.mousePosition.x - this.player2.xCord;
            dy = this.mousePosition.y - this.player2.yCord;
          }
        const distance = Math.sqrt(dx * dx + dy * dy);

        //Toggle hovering if the mouse is within the aim circle range
        this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;

        if (this.toggleHovering) {

          //Update the angle and power values
          if(this.p1Turn){
            this.p1Circle.angle = -(Math.atan2(dy, dx) * 180) / Math.PI;
            this.p1Circle.power = Math.round((distance / this.aimCircleRadius) * 100);
          } else {
            let p2Angle = 180 - (-(Math.atan2(dy, dx) * 180) / Math.PI);
            if (p2Angle > 180) {
              p2Angle -= 360;
            }
            this.p2Circle.angle = p2Angle;
            this.p2Circle.power = Math.round((distance / this.aimCircleRadius) * 100);
          }

          //Redraw the game with updated values
          this.drawGame();
        }
      },

      drawTank(ctx, player, playerAimCircle) {

        ctx.save();
        player.yCord = this.terrain[Math.floor(player.xCord)] - 40 / 2;

        const groundLevel = this.canvasHeight - 40 / 2;
        if (player.yCord > groundLevel) {
          player.yCord = groundLevel;
        }

        ctx.translate(player.xCord, player.yCord);

        //Color for outline
        ctx.strokeStyle = "black";


        // Draw the tank body
        ctx.fillStyle = player.color;
        ctx.fillRect(-40 / 2, -40 / 4, 40, 40 / 2);
        ctx.strokeRect(-40 / 2, -40 / 4, 40, 40 / 2);

        // Draw the tank turret
        const turretLength = 40 * 0.7;
        ctx.translate(0, -40 / 7);
        if(player.id === 1){
          ctx.rotate((-playerAimCircle.angle * Math.PI) / 180);
        } else {
          ctx.rotate((-(180 - playerAimCircle.angle) * Math.PI) / 180);
        }
        //ctx.fillStyle = this.player1.color;
        ctx.fillStyle = player.color;
        ctx.fillRect(0, -5, turretLength, 10);
        ctx.strokeRect(0, -5, turretLength, 10);

        ctx.restore();
      },

      drawAimCircle(ctx, playerAimCircle, player) {
        ctx.beginPath();
        ctx.arc(player.xCord, player.yCord, this.aimCircleRadius, 0, 2 * Math.PI);
        // Fill the circle with a semi-transparent color
        ctx.fillStyle = 'rgba(128, 128, 128, 0.2)';
        ctx.fill();  // Fill first to apply transparency correctly

        // Stroke the border of the circle
        ctx.strokeStyle = "black";
        ctx.stroke();

        // Draw the power/shot line
        ctx.beginPath();
        ctx.moveTo(player.xCord, player.yCord);
        ctx.lineTo(playerAimCircle.aimLaserXCord, playerAimCircle.aimLaserYCord); // Use the updated stop positions
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
        this.drawTank(ctx, this.player1, this.p1Circle);

        // Draw player 2's tank
        this.drawTank(ctx, this.player2, this.p2Circle);

        //Draw player names
        this.drawPlayerNames(ctx);

        //Draw player health
        this.drawPlayerHealth(ctx);

        //Draw wind
        this.drawWind(ctx);

        //Draw angle and power values in the circle
        if(this.p1Turn){

          // Calculate the laser line's endpoint based on the updated angle and power
          this.calculateLaserPos(this.p1Circle, this.player1);

          // Draw the angle and power values
          this.drawAnglePower(ctx, this.p1Circle, this.player1);

          // Draw the aim circle and the aiming line
          this.drawAimCircle(ctx, this.p1Circle, this.player1);
        } else {
          this.calculateLaserPos(this.p2Circle, this.player2);
          this.drawAnglePower(ctx, this.p2Circle, this.player2);
          this.drawAimCircle(ctx, this.p2Circle, this.player2);
        }
      },
    },
    beforeUnmount() {
      window.removeEventListener('keydown', this.onKeyPressed);
    },
  };
  </script>

<style scoped>
</style>
