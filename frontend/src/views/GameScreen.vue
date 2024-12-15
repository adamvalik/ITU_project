<!--
  File: GameScreen.vue
  Author: Samue, Hejnicek (xhejni00)
-->


<template>
  <div :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`, backgroundColor: '#D5EFF4'}">
    <div>
      <div class="h-44 bg-opacity-80 bg-neutral-900 text-white items-center justify-center flex flex-rows space-x-8">

        <!-- Weapon selector button -->
        <div class="w-1/3 relative">
          <div class="flex flex-col space-y-1" :class="{'-mt-16' : toggleDropDownMenu}">
            <div>
              <button
                @mouseover="showSelectorHelp"
                @mouseleave="hideSelectorHelp"
                @click="toggleWeaponMenu"
                class="h-16 w-full bg-blue-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-blue-400 font-bold text-4xl relative">
                WEAPON SELECTOR

                <!-- Weapon selector help text -->
                <span v-if="selectorHelpVisible" class="absolute top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-2xl">
                Click to select weapon!
              </span>
              </button>
            </div>

            <!-- Active missile -->
            <div v-if="!toggleDropDownMenu && activeMissile">
              <button
                class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
                <div class="flex flex-row justify-center space-x-8">
                  <div class="text-black font-bold text-3xl">{{ activeMissile.name }}</div>
                  <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                  <div class="text-black font-bold text-3xl">{{ currentPlayer.ammunitionCount[this.currentPlayer.activeMissileId] }}</div>
                </div>
              </button>
            </div>
          </div>

          <!-- Drop down menu with missiles -->
          <div v-if="toggleDropDownMenu" class="absolute top-1/2 bg-gray-600 border-4 border-gray-700 space-y-2">
            <button
              v-for="(missile) in currentPlayerMissiles"
              :key="missile.id"
              @click="selectMissile(missile.id)"
              @mouseover="showMissileInfo = missile.id"
              @mouseleave="showMissileInfo = null"
              class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">{{ missile.name }}</div>
                <div class="w-8 h-8" :style="{ background: `url(${missile.picture}) no-repeat center center`, backgroundSize: 'cover' }"></div>
                <div class="text-black font-bold text-3xl">{{ currentPlayer.ammunitionCount[missile.id] }}</div>
              </div>

              <!-- Detailed missile info -->
              <div v-if="showMissileInfo === missile.id" class="absolute top-0 left-full ml-0 w-60 bg-gray-400 rounded-lg p-2 border-4 border-black" style="z-index: 10;">
                <div class="text-black font-bold text-2xl">Cost in shop: <span :style="{ color: 'green' }"> {{ missile.price }}$ </span></div>
                <div class="text-black font-bold text-2xl">Shell radius: <span :style="{ color: 'blue' }"> {{ missile.radius }} </span></div>
                <div class="text-black font-bold text-2xl">Damage: <span :style="{ color: 'red' }"> {{ missile.damage }}HP </span></div>
              </div>
            </button>
          </div>
        </div>

        <!-- Fire button -->
        <div class="relative w-1/4">
          <button
              @mouseover="showFireHelp"
              @mouseleave="hideFireHelp"
              @click="fireMissile"
              class="py-16 w-full bg-red-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-red-400 font-bold text-4xl">
              FIRE
            
            <!-- Fire button help text -->
            <span v-if="fireHelpVisible" class="absolute top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-2xl">
              Click to fire!
            </span>
          </button>
        </div>

        <!-- Row flex for money, time and so on -->
        <div class ="flex flex-rows space-x-8 w-1/3 mt-4">

          <!-- Col flex for items in the row-->
          <div class ="flex flex-col space-y-4 items-center">

            <!-- Time per round -->
            <div v-if="this.useTimer" class="font-bold text-white text-2xl">
              <h1>{{ timePerRound }} (s)</h1>
            </div>
            <div v-else class="font-bold text-white text-2xl">
              <h1>Inf</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/time_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2 items-center">

            <!-- Player money -->
            <div class="font-bold text-white text-2xl">
              <h1>{{ currentPlayer.money }}$</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/money_bag_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2, items-center">

            <!-- Player fuel -->
            <div class="font-bold text-white text-2xl">
              <h1>{{ currentPlayer.fuel }}/{{ currentPlayer.fuelMax }}</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/fuel_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-3 items-center">

            <!-- Player wins -->
            <div class="font-bold text-white text-2xl">
              <h1>{{ currentPlayer.wins }}wins</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/trophy_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <!-- Pause button -->
          <div class="relative mb-16">
            <button
              @click="togglePauseGame">
              <div class="w-20 h-20" style="background: url('assets/pause_icon.png') no-repeat center center; background-size: cover;"></div>
            </button>
          </div>

        </div>
      </div>

    </div>

    <!-- Game canvas for tanks -->
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

    <!-- Pause game window -->
    <div v-if="pauseGame" class="bg-black bg-opacity-70 items-center justify-center flex flex-col absolute inset-0 z-20">
      <h1 class="text-4xl font-bold text-black">Game Paused</h1>

      <!-- Resume game -->
      <button @click="togglePauseGame" class="w-64 border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl rounded-2xl px-4 py-4 mt-4 justify-center items-center">
        Resume
      </button>

      <!-- Back to main menu -->
      <button @click="backToMenu" class="w-64 border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl px-4 py-4 rounded-2xl mt-4 justify-center items-center">
        Back to Main Menu
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
        // Default canvas size based on scale got from App Vue
        canvasWidth: this.gameWidth,
        canvasHeight: this.gameHeight - 176,

        // Image canvas
        //imageCanvas: null,

        // Map data for drawing
        terrainData: {
          terrain: [],
        },

        // PLayer data for drawing
        player1: {
          ammunitionCount: 0,
        },
        player2: {
          ammunitionCount: 0,
        },

        // Mouse position for aiming
        mousePosition: {
          x: 0,
          y: 0,
        },

        // Use Timer for the game
        useTimer: false,

        // Time per round
        timePerRound: 0,

        // Game over flag
        gameOver: false,

        // Response game over flag
        responseGameOver: false,

        // Wind value for the lap
        wind: 0,

        // Player turn
        p1Turn: true,

        // Aim circle data
        toggleHovering: false,
        toggleDragging: false,
        aimCircleRadius: 0,

        // Laser coordinates for player circle
        p1Circle: {
          aimLaserXCord: 0,
          aimLaserYCord: 0,
        },
        p2Circle: {
          aimLaserXCord: 0,
          aimLaserYCord: 0,
        },

        // Missile trajectory for animation
        missileTrajectory: [],

        // Available missiles to choose from
        missiles: [],

        // Player selected missile
        activeMissileId: 0,

        // Show missile info if hovering on the missile
        showMissileInfo: null,

        // Control bar toggles
        fireHelpVisible: false,
        selectorHelpVisible: false,
        toggleDropDownMenu: false,
        toggleDisableFire: false,
        pauseGame: false,
      };
    },
    // created() {
    //   this.imageCanvas = document.createElement('canvas');
    // },
    computed: {
      currentPlayer() {
        return this.p1Turn ? this.player1 : this.player2;
      },

      nextPlayer() {
        return this.p1Turn ? this.player2 : this.player1;
      },

      activeMissile() {
        return this.missiles[this.currentPlayer.activeMissileId];
      },

      currentAimCircle() {
        return this.p1Turn ? this.p1Circle : this.p2Circle;
      },

      currentPlayerMissiles() {

        // Filter only missiles where player has ammunition
        const displayedMissiles = [];
        for (let i = 0; i < this.currentPlayer.ammunitionCount.length; i++) {
          if (this.currentPlayer.ammunitionCount[i] >= 0) {
            displayedMissiles.push(this.missiles[i]);
          }
        }
        return displayedMissiles;
      }
    },
    mounted() {
      // Load missiles, map data, game data and player data
      this.loadMissiles();
      this.loadMapData();
      this.loadGameData();
      this.loadPlayerData();
      window.addEventListener('keydown', this.onKeyPressed);
    },
    watch: {
      // Watch for game over flag, if true, increment skill points and reset player values
      async gameOver(newValue) {
        if (newValue) {
          try {
            await apiClient.post('/player/skillPointsInc', { player: 1});
            await apiClient.post('/player/skillPointsInc', { player: 2});
            await apiClient.delete('/players/reset-values');
            await apiClient.delete('/game/reset-turn');
          } catch (error) {
            console.error(error);
          }
          // Redirect to shop
          this.$router.push('/shop');
        }
      }
    },
    methods: {
      // Toggle dropdown menu after clicking on the weapon selector
      toggleWeaponMenu() {
        this.toggleDropDownMenu = !this.toggleDropDownMenu;
      },

      // Toggle pause game after clicking on the pause button
      togglePauseGame() {
        this.pauseGame = !this.pauseGame;
      },

      // Load missiles from database using API
      async loadMissiles() {
        await apiClient.get('/missiles')
          .then((response) => {
            this.missiles = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },

      // Chamge active missile id to show current weapon under the weapon selector
      selectMissile(missileId) {
        this.currentPlayer.activeMissileId = missileId;
        this.toggleDropDownMenu = false;

        axios.post('http://localhost:8000/save-current-active-missile', {
          id: this.currentPlayer.activeMissileId,
        })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });
        
      },

      // Load map data from the database using API
      async loadMapData() {
        await axios.get('http://localhost:8000/obtain-terrain-data', {
          params: {
            canvasWidth: this.canvasWidth,
            canvasHeight: this.canvasHeight,
          }
        })
        .then((response) => {

          //Obtain terrain, color and background color to draw later
          this.terrainData.terrain = response.data.data;
          this.terrainData.terrainType = response.data.type;
          this.terrainData.terrainBgColor = response.data.background;
        })
        .catch((error) => {
          console.error(error);
        });
      },

      // Load game data from the database using API
      async loadGameData() {
      await axios.get('http://localhost:8000/game')
        .then((response) => {
          // Obtain game data such as if the timer is enabled, whose turn it is, wind value
          this.timePerRound = response.data.timePerTurn;
          this.wind = response.data.wind;
          this.useTimer = response.data.isTimer;
          this.p1Turn = response.data.p1Turn;
          this.aimCircleRadius = response.data.aimCircleRadius;

          // Validate timer if enabled 
          this.validateTimer();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    validateTimer() {

      // No timer is set
      if(!this.useTimer){
        return;
      }

      // Set interval for the timer to count down every second
      setInterval(() => {
        if(this.timePerRound > 0) {
          this.timePerRound--;
        } else {
          this.gameOver = true;
        }
      }, 1000);
    },

      // Load both player data from the database using API
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

            // Draw the game after loading the player data
            this.drawGame();
          })
          .catch((error) => {
            console.error(error);
          });
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

      // Calculate ending position of the aiming laser based on the angle, power and player's position
      async calculateLaserPos(playerAimCircle) {

        //Calculate the distance based on the power
        const distance = (this.currentPlayer.power / 100) * this.aimCircleRadius;

        // Calculate the angle in radians based on whose turn it is
        let angleInRadians;
        if (this.p1Turn) {
            angleInRadians = (-this.currentPlayer.angle * Math.PI) / 180;
        } else {
            angleInRadians = (-(180 - this.currentPlayer.angle) * Math.PI) / 180;
        }

        // Calculate laser's endpoint x and y coordinates based on the angle and distance
        playerAimCircle.aimLaserXCord = this.currentPlayer.xCord + distance * Math.cos(angleInRadians);
        playerAimCircle.aimLaserYCord = this.currentPlayer.yCord + distance * Math.sin(angleInRadians);
      },

      // Fire missile after clicking on the fire button or pressing spacebar
      async fireMissile() {

        // Disable firing until the animation is finished
        if(this.toggleDisableFire){
          return;
        }
        this.toggleDisableFire = true;

        // Save current players data (angle, power)
        await axios.post('http://localhost:8000/save-current-players-data', {
          player1: this.player1,
          player2: this.player2,
        })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });

        // Compute missile data including trajectory, if the player hit the target and so on
        await axios.post('http://localhost:8000/compute-missile-data', {
          canvasWidth: this.canvasWidth,
          canvasHeight: this.canvasHeight,
        })
        .then((response) => {
          console.log(response);

          // Return if player is out of ammo
          if(response.data.noAmmunition){
            this.toggleDisableFire = false;
            return;
          }

          // Obtain missile trajectory for animation
          this.missileTrajectory = response.data.missileTrajectory;

          // Update new ammunition count
          this.currentPlayer.ammunitionCount[this.currentPlayer.activeMissileId] = response.data.ammunitionCount;

          // Update response game over flag
          this.responseGameOver = response.data.gameOver;

        });

        // Obtain updated terrain data
        await axios.get('http://localhost:8000/obtain-updated-map')
        .then((response) => {

          //Obtain updated terrain, color and background color
          this.terrainData.terrain = response.data.data;
          this.terrainData.terrainType = response.data.type;
          this.terrainData.terrainBgColor = response.data.background;

          // Animate the missile
          this.animateMissile();
        })
        .catch((error) => {
          console.error(error);
        });
      },
      animateMissile() {

        // Obtain the x and y coordinates for the missile trajectory
        const [xCord, yCord] = this.missileTrajectory.shift();

        //this.drawGame();

        // Draw the missile as a red circle as big as the damage
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext("2d");
        ctx.beginPath();
        ctx.arc(xCord, yCord, this.missiles[this.currentPlayer.activeMissileId].damage / 4, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();

        // Animates the missile based on the trajectory
        if(this.missileTrajectory.length > 0){
          requestAnimationFrame(this.animateMissile);
        } else {

          // Load updated player data after the missile has landed
          this.loadPlayerData();

          // If response game over flag is true, game is over
          if(this.responseGameOver){
            this.gameOver = true;
          }
          
          // Switch player turn and enable firing
          this.toggleDisableFire = false;
          this.p1Turn = !this.p1Turn;

          // Redraw the game
          this.drawGame();
        }
      },

            // Draw player names at the top of the canvas
            drawPlayerNames(ctx) {
        ctx.save();

        // Size of rectangles for healthbars
        const player1X = 10 + 200 / 2;
        const player2X = this.canvasWidth - 210 + 200 / 2;

        // Text properties
        ctx.font = "28px sans-serif";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        // Draw player names
        ctx.fillText(this.player1.name, player1X, 30);
        ctx.fillText(this.player2.name, player2X, 30);

        ctx.restore();
      },

      // Draw player health bars with health values on top of the canvas
      drawPlayerHealth(ctx){
        ctx.save();

        // Draw black background for health bars
        ctx.fillStyle = 'black';
        ctx.fillRect(10, 50, 200, 40);
        ctx.fillRect(this.canvasWidth - 210, 50, 200, 40);

        // Draw red background for remaining health
        ctx.fillStyle = '#FF0000';
        const player1HealthWidth = this.player1.health * 2;
        ctx.fillRect(10, 50, player1HealthWidth, 40);
        const player2HeathWidth = this.player2.health * 2;
        ctx.fillRect(this.canvasWidth - 210, 50, player2HeathWidth, 40);

        //Draw outline for health bars
        ctx.strokeStyle = 'gray';
        ctx.lineWidth = 5; // Border width
        ctx.strokeRect(10, 50, 200, 40);
        ctx.strokeRect(this.canvasWidth - 210, 50, 200, 40);

        // Draw remaining health / 100
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${this.player1.health}/${this.player1.healthMax}`, 110, 70);
        ctx.fillText(`${this.player2.health}/${this.player2.healthMax}`, this.canvasWidth - 110, 70);

        ctx.restore();
      },

      // Draw wind value in the middle of the canvas
      drawWind(ctx){
        ctx.save();

        // Text properties
        ctx.fillStyle = 'black';
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Wind: ', this.canvasWidth/2, 20);
        ctx.fillText(this.wind, this.canvasWidth/2 + 40, 20);

        ctx.restore();
      },

      // Draw angle and power values at the top of the aim circle
      drawAnglePower(ctx) {
        ctx.save();

        // Text properties
        ctx.fillStyle = 'black';
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${Math.round(this.currentPlayer.angle)}°,`, this.currentPlayer.xCord - 10, this.currentPlayer.yCord - 180);
        ctx.fillText(this.currentPlayer.power, this.currentPlayer.xCord + 26, this.currentPlayer.yCord - 180);

        ctx.restore();
      },

      // Draw the terrain based on map data
      drawTerrain(ctx) {

        // Draw background color
        ctx.fillStyle = this.terrainData.terrainBgColor;
        ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight);

        // Draw the terrain
        ctx.beginPath();
        ctx.moveTo(0, this.canvasHeight);
        for (let x = 0; x < this.terrainData.terrain.length; x++) {
          ctx.lineTo(x, this.terrainData.terrain[x]);
        }
        ctx.lineTo(this.canvasWidth, this.canvasHeight);
        ctx.closePath();

        // Set the terrain color
        ctx.fillStyle = this.terrainData.terrainType;
        ctx.fill();
      },

      // Draw the tank based on player data
      drawTank(ctx, player) {
        ctx.save();

        // Update the player's yCord based on the terrain so tank is always on the terrain
        player.yCord = this.terrainData.terrain[Math.floor(player.xCord)] - 40 / 4;

        // Move to player's position
        ctx.translate(player.xCord, player.yCord);

        // Color for outline
        ctx.strokeStyle = "black";

        // Draw the tank body
        ctx.fillStyle = player.color;
        ctx.fillRect(-40 / 2, -40 / 4, 40, 40 / 2);
        ctx.strokeRect(-40 / 2, -40 / 4, 40, 40 / 2);

        // Draw the tank turret
        const turretLength = 25;
        ctx.translate(0, -7);
        if(player.id === 1){
          ctx.rotate((-player.angle * Math.PI) / 180);
        } else {
          ctx.rotate((-(180 - player.angle) * Math.PI) / 180);
        }
        ctx.fillStyle = player.color;
        ctx.fillRect(0, -5, turretLength, 10);
        ctx.strokeRect(0, -5, turretLength, 10);

        ctx.restore();
      },

      drawAimCircle(ctx, playerAimCircle) {
        ctx.save();

        ctx.beginPath();

        // Draw the aim circle
        ctx.arc(this.currentPlayer.xCord, this.currentPlayer.yCord, this.aimCircleRadius, 0, 2 * Math.PI);
        ctx.fillStyle = 'rgba(128, 128, 128, 0.2)';
        ctx.fill();

        // Create the outline for the aim circle
        ctx.strokeStyle = "black";
        ctx.stroke();

        // Draw the laser line in red color
        ctx.beginPath();

        // Obtain laser start position based on the turret angle
        let turretAngle = this.p1Turn ?(-this.currentPlayer.angle * Math.PI) / 180 : (-(180 - this.currentPlayer.angle) * Math.PI) / 180;
        const laserStartPosX = this.currentPlayer.xCord + 25 * Math.cos(turretAngle);
        const laserStartPosY = this.currentPlayer.yCord + 25 * Math.sin(turretAngle);

        // Draw the laser line
        ctx.moveTo(laserStartPosX, laserStartPosY);
        ctx.lineTo(playerAimCircle.aimLaserXCord, playerAimCircle.aimLaserYCord);
        ctx.strokeStyle = "red";
        ctx.stroke();

        ctx.restore();
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

        // Draw player names
        this.drawPlayerNames(ctx);

        // Draw player health
        this.drawPlayerHealth(ctx);

        // Draw wind
        this.drawWind(ctx);

        // Calculate the laser line's endpoint based on the updated angle and power
        this.calculateLaserPos(this.currentAimCircle);

        // Draw the angle and power values
        this.drawAnglePower(ctx, this.currentAimCircle);

        // Draw the aim circle and the aiming line
        this.drawAimCircle(ctx, this.currentAimCircle);

      },

      // Handle keyboard input for player movement and aiming
      async onKeyPressed(event){

        // No keys registered if the game is paused
        if(this.pauseGame){
          return;
        }

        // Compute player movement and aiming based on the key pressed via API
        await axios.post('http://localhost:8000/keyboard-movement', {
          key: event.key,
          canvasWidth: this.canvasWidth,
          canvasHeight: this.canvasHeight,
          aimLaserXCord: this.currentAimCircle.aimLaserXCord,
          power: this.currentPlayer.power,
          angle: this.currentPlayer.angle,
        })
        .then((response) => {
          console.log(response);

          // If space is pressed, fire the missile
          if(response.data.shoot === true){
            this.fireMissile();
          }

          // Update player data based on the response
          this.currentPlayer.xCord = response.data.playerXCord;
          this.currentPlayer.fuel = response.data.playerFuel;
          this.currentAimCircle.aimLaserXCord = response.data.aimLaserXCord;
          this.currentPlayer.power = response.data.power;
          this.currentPlayer.angle = response.data.angle;

          // Redraw the game with updated values
          this.drawGame();
        })
        .catch((error) => {
          console.error(error);
        });
      },

      // If mouse pressed, start dragging if mouse in the aim circle
      onMouseDown() {

        // If mouse in the aim circle, enable dragging
        if (this.toggleHovering) {
          this.toggleDragging = true;
        }
      },

      // If mouse is released, stop dragging
      onMouseUp() {
        this.toggleDragging = false;
      },

      // If mouse moves
      onMouseMove(event) {

          // Obtain mousePosition relative to the canvas
          const rect = this.$refs.gameCanvas.getBoundingClientRect();
          this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
          this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

          // Calculate the distance between the tank and the mouse
          let tankMouseX, tankMouseY;
          if(this.p1Turn){
            tankMouseX = this.mousePosition.x - this.player1.xCord;
            tankMouseY = this.mousePosition.y - this.player1.yCord;
          } else {
            tankMouseX = this.mousePosition.x - this.player2.xCord;
            tankMouseY = this.mousePosition.y - this.player2.yCord;
          }

          // Calculate the distance between the tank and the mouse
          const distance = Math.sqrt(tankMouseX ** 2 + tankMouseY ** 2);

          // Toggle hovering if the mouse is within the aim circle
          this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;

          // Return if not in the aim circle
          if(!this.toggleHovering){
            return;
          }

          // Dragging is enabled
          if (this.toggleDragging) {

            // Update power value for current player
            this.currentPlayer.power = Math.round((distance / this.aimCircleRadius) * 100);

            // Update the power value and angle values based on player turn
            if(this.p1Turn){
              this.currentPlayer.angle = -(Math.atan2(tankMouseY, tankMouseX) * 180) / Math.PI;
            } else {

              // Update the angle for second player
              let p2Angle = 180 - (-(Math.atan2(tankMouseY, tankMouseX) * 180) / Math.PI);
              if (p2Angle > 180) {
                p2Angle -= 360;
              }
              this.currentPlayer.angle = p2Angle;
            }
          }

          // Redraw the game with updated values
          this.drawGame();
      },

      onMouseClick(event) {

        // Obtain mousePosition relative to the canvas
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
        this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

          // Calculate the distance between the tank and the mouse
          let tankMouseX, tankMouseY;
          if(this.p1Turn){
            tankMouseX = this.mousePosition.x - this.player1.xCord;
            tankMouseY = this.mousePosition.y - this.player1.yCord;
          } else {
            tankMouseX = this.mousePosition.x - this.player2.xCord;
            tankMouseY = this.mousePosition.y - this.player2.yCord;
          }

        // Calculate the distance between the tank and the mouse
        const distance = Math.sqrt(tankMouseX ** 2 + tankMouseY ** 2);

        // Toggle hovering if the mouse is within the aim circle range
        this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;

        // If mouse is within the aim circle
        if (this.toggleHovering) {

          // Update power value for current player
          this.currentPlayer.power = Math.round((distance / this.aimCircleRadius) * 100);

          // Update the power value and angle values based on player turn
          if(this.p1Turn){
            this.currentPlayer.angle = -(Math.atan2(tankMouseY, tankMouseX) * 180) / Math.PI;
          } else {

            // Update the angle for second player
            let p2Angle = 180 - (-(Math.atan2(tankMouseY, tankMouseX) * 180) / Math.PI);
            if (p2Angle > 180) {
              p2Angle -= 360;
            }
            this.currentPlayer.angle = p2Angle;
          }

          // Redraw the game with updated values
          this.drawGame();
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

<!-- // Image canvas
imageCanvas: null,

created() {
  this.imageCanvas = document.createElement('canvas');
  this.imageCanvas.width = this.canvasWidth;
  this.imageCanvas.height = this.canvasHeight;
},

fillImageCanvas(wind) {
  const ctx = this.imageCanvas.getContext('2d');
  ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
  this.drawPlayerHealth(ctx);
  this.drawPlayerNames(ctx);
  this.drawWind(ctx, wind);
  this.drawTank(ctx, this.nextPlayer, this.nextPlayerCircle);
},

addItemsToImageCanvas(currentTank, activeAimCircle, terrain, anglePower) {
  const ctx = this.imageCanvas.getContext('2d');
  if(currentTank){
    this.drawTank(ctx, this.currentPlayer, this.currentAimCircle);
  }
  if(terrain){
    this.drawTerrain(ctx);
  }
  if(anglePower){
    this.drawAnglePower(ctx, this.currentAimCircle, this.currentPlayer);
  }
  if(activeAimCircle){
    this.drawAimCircle(ctx,this. currentAimCircle, this.currentPlayer);
  }
},

const canvas = this.$refs.gameCanvas;
const ctx = canvas.getContext('2d');
ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

ctx.drawImage(this.imageCanvas, 0, 0); -->
